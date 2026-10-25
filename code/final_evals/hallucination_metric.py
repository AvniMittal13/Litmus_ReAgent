import sys
import os
import json
import glob
import pandas as pd
import pickle
from datetime import datetime
from statistics import mean
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response
from pydantic import BaseModel

class CitationVerificationMetric(BaseModel):
    Hallucinated_papers_cited : int
    Total_number_of_papers_cited: int
    Hallucinated_citation_urls: list[str]


prompt = """
You are an **expert bibliometrics and NLP evaluation agent**.
Your task is to verify whether the citations in a research report are real or hallucinated, using **only the provided list of available paper links and descriptions**.

### Input

1. **Research report text** containing citations.
2. **Available papers list** (a set of links and/or descriptions of real papers).

### Instructions

* Identify every paper cited in the report.
* Check if each cited paper exactly matches one from the provided available papers list (by url match or strong descriptive match).
* If a cited paper is **not found** in the provided list, mark it as hallucinated.
* Do not rely on outside knowledge or the web.
* Only use the provided available papers list for verification.

### Output format

Return **only** a JSON object with the following fields:

```json
{{
  "Hallucinated_papers_cited": <integer>,
  "Total_number_of_papers_cited": <integer>,
  "Hallucinated_citation_urls": [<string>, <string>, ...]
}}
```

* `Hallucinated_papers_cited`: Count of citations in the report that do not appear in the provided available papers list.
* `Total_number_of_papers_cited`: Total number of citations in the report (including both real and hallucinated).

### Notes

* If no citations are found in the report, return both values as `0`.
* Do not include extra commentary, explanations, or text outside the JSON.

---

# User Query
{user_query}

---

# Report Generated
{report_generated}

---

# Available list of papers
{available_list_of_papers}

---

Now check the available list of papers and match with citations provided in the report generated to answer the user query
"""


def load_available_papers(task_name, csvs_folder):
    """Load available papers for a specific task."""
    # Map task names to folder names
    task_folder_map = {
        "01_Code_Generation": "01_Code_Generation",
        "02_Math_Reasoning": "02_Math_Reasoning", 
        "03_QA_VQA": "03_QA_VQA",
        "04_Classification_NLI": "04_Classification_NLI",
        "05_Text_Summarization": "05_Text_Summarization",
        "06_Machine_Translation": "06_Machine_Translation"
    }
    
    task_folder = task_folder_map.get(task_name, task_name)
    csv_path = os.path.join(csvs_folder, task_folder, f"reduced_combined_{task_folder.lower().replace('_', '_')}.csv")
    
    try:
        df = pd.read_csv(csv_path)
        papers_list = []
        
        for _, row in df.iterrows():
            # paper_info = f"URL: {row['URL']}\nDescription: {row['Description']}\nTask: {row['Task']}\nLanguages: {row['Languages']}\nModels: {row['Models']}"
            paper_info = f"{{URL: {row['URL']}\nDescription: {row['Description']}}}"
            papers_list.append(paper_info)
        
        return "\n\n".join(papers_list)
    
    except Exception as e:
        print(f"Error loading papers for task {task_name}: {e}")
        return ""


def evaluate_single_report(report_text, user_query, available_papers, query_id=None, task=None, scenario=None, folder_name=""):
    """Evaluate a single report for citation hallucinations."""
    response = get_structured_response(
        prompt=prompt.format(
            user_query=user_query,
            report_generated=report_text,
            available_list_of_papers=available_papers
        ),
        structuredClass=CitationVerificationMetric,
        # model_name="o3-mini"
    )
    evaluation = CitationVerificationMetric(**json.loads(response))
    
    # Store individual result if query_id is provided
    if query_id and task and scenario:
        store_individual_hallucination_result(evaluation, query_id, task, scenario, folder_name, report_text)
    
    return evaluation


def store_individual_hallucination_result(evaluation, query_id, task, scenario, folder_name, report_text):
    """Store individual LLM judge result for a query."""
    # Create directory structure: llm_evals_hallucination_thought/folder_name/task/scenario/
    results_dir = os.path.join("llm_evals_hallucination_thought", folder_name, task, scenario)
    os.makedirs(results_dir, exist_ok=True)
    
    result_data = {
        "query_id": query_id,
        "task": task,
        "scenario": scenario,
        "folder_source": folder_name,
        "original_report": report_text,
        "evaluation": {
            "Hallucinated_papers_cited": evaluation.Hallucinated_papers_cited,
            "Total_number_of_papers_cited": evaluation.Total_number_of_papers_cited,
            "Hallucinated_citation_urls": evaluation.Hallucinated_citation_urls
        }
    }
    
    result_file = os.path.join(results_dir, f"{query_id}_hallucination_result.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)


def process_single_hallucination_report(report_info, question_mapping, csvs_folder, folder_name=""):
    """Process a single report file for hallucination evaluation."""
    try:
        # Read the report content
        with open(report_info['file_path'], 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        question_id = report_info['question_id']
        task = report_info['task']
        scenario = report_info['scenario']
        
        print(f"Processing hallucination: {task}/{scenario}/{question_id}")
        
        # Get question details from mapping
        question_details = question_mapping.get(question_id, {})
        user_query = question_details.get('complete_question', '')
        
        # Load available papers for this task
        available_papers = load_available_papers(task, csvs_folder)
        
        if not available_papers:
            print(f"Warning: No available papers found for task {task}")
            available_papers = "No papers available for this task."
        
        # Evaluate the report
        evaluation = evaluate_single_report(report_content, user_query, available_papers, question_id, task, scenario, folder_name)
        
        return {
            'question_id': question_id,
            'task': task,
            'scenario': scenario,
            'question_details': question_details,
            'evaluation': evaluation.__dict__
        }
        
    except Exception as e:
        print(f"Error processing hallucination {report_info['file_path']}: {str(e)}")
        return None


def save_hallucination_summary_report(results, output_folder, folder_name=""):
    """Save the summary report as a txt file."""
    if folder_name:
        summary_file = os.path.join(output_folder, f"hallucination_metrics_summary_{folder_name}.txt")
    else:
        summary_file = os.path.join(output_folder, "hallucination_metrics_summary.txt")
    
    # Generate summary report content
    report_lines = []
    report_lines.append("="*80)
    report_lines.append(f"HALLUCINATION METRICS ANALYSIS - {folder_name}" if folder_name else "HALLUCINATION METRICS ANALYSIS")
    report_lines.append("="*80)
    
    # Summary
    summary = results['summary']
    report_lines.append(f"\nSUMMARY:")
    report_lines.append(f"  Total reports: {summary['total_reports']}")
    report_lines.append(f"  Processed successfully: {summary['processed_successfully']}")
    report_lines.append(f"  Failed: {summary['failed']}")
    
    # Task-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-WISE HALLUCINATION METRICS")
    report_lines.append("="*80)
    
    for task, metrics in results['task_metrics'].items():
        report_lines.append(f"\n{task}:")
        
        for metric_name, stats in metrics.items():
            if metric_name == 'hallucination_rate':
                report_lines.append(f"  Average Hallucination Ratio (hallucinated/total): {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            elif metric_name == 'hallucinated_papers':
                report_lines.append(f"  Hallucinated Papers: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
            elif metric_name == 'total_papers':
                report_lines.append(f"  Total Papers Cited: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
    
    # Scenario-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("SCENARIO-WISE HALLUCINATION METRICS")
    report_lines.append("="*80)
    
    for scenario, metrics in results['scenario_metrics'].items():
        report_lines.append(f"\n{scenario}:")
        
        for metric_name, stats in metrics.items():
            if metric_name == 'hallucination_rate':
                report_lines.append(f"  Average Hallucination Ratio (hallucinated/total): {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            elif metric_name == 'hallucinated_papers':
                report_lines.append(f"  Hallucinated Papers: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
            elif metric_name == 'total_papers':
                report_lines.append(f"  Total Papers Cited: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
    
    # Task-Scenario combination metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-SCENARIO COMBINATION HALLUCINATION METRICS")
    report_lines.append("="*80)
    
    for task_scenario, metrics in results['task_scenario_metrics'].items():
        report_lines.append(f"\n{task_scenario.replace('_', ' / ')}:")
        
        for metric_name, stats in metrics.items():
            if metric_name == 'hallucination_rate':
                report_lines.append(f"  Average Hallucination Ratio (hallucinated/total): {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            elif metric_name == 'hallucinated_papers':
                report_lines.append(f"  Hallucinated Papers: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
            elif metric_name == 'total_papers':
                report_lines.append(f"  Total Papers Cited: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
    
    # Write summary report
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Summary report saved to: {summary_file}")
    return summary_file


def load_question_mapping(questions_folder):
    """Load question mapping from generated questions folder."""
    question_mapping = {}
    
    # Load all question files
    for question_file in glob.glob(os.path.join(questions_folder, "*.json")):
        with open(question_file, 'r', encoding='utf-8') as f:
            question_data = json.load(f)
            
        task_name = question_data['task']
        scenario = question_data['scenario']
        
        for question in question_data['questions']:
            question_id = question['unique_id']
            question_mapping[question_id] = {
                'task': task_name,
                'scenario': scenario,
                'complete_question': question['complete_question'],
                'models': question.get('models', ''),
                'languages': question.get('languages', '')
            }
    
    return question_mapping


def save_intermediate_results(results, output_folder, timestamp):
    """Save intermediate results with timestamp."""
    checkpoint_file = os.path.join(output_folder, f"hallucination_checkpoint_{timestamp}.json")
    
    # Convert evaluation objects to dict for JSON serialization
    serializable_results = json.loads(json.dumps(results, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x)))
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    print(f"Intermediate results saved to: {checkpoint_file}")
    return checkpoint_file


def load_intermediate_results(output_folder):
    """Load the most recent checkpoint file."""
    checkpoint_files = glob.glob(os.path.join(output_folder, "hallucination_checkpoint_*.json"))
    
    if not checkpoint_files:
        return None, None
    
    # Get the most recent checkpoint
    latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
    
    try:
        with open(latest_checkpoint, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Extract processed question IDs
        processed_ids = set()
        for result in results.get('detailed_results', []):
            processed_ids.add(result['question_id'])
        
        print(f"Loaded checkpoint from: {latest_checkpoint}")
        print(f"Found {len(processed_ids)} previously processed questions")
        
        return results, processed_ids
    
    except Exception as e:
        print(f"Error loading checkpoint {latest_checkpoint}: {e}")
        return None, None


def cleanup_checkpoint_files(output_folder, current_timestamp):
    """Remove checkpoint files after successful completion."""
    checkpoint_files = glob.glob(os.path.join(output_folder, "hallucination_checkpoint_*.json"))
    
    for checkpoint_file in checkpoint_files:
        # Don't delete the current timestamp file (it becomes the final results)
        if current_timestamp not in checkpoint_file:
            try:
                os.remove(checkpoint_file)
                print(f"Cleaned up checkpoint file: {checkpoint_file}")
            except Exception as e:
                print(f"Error cleaning up {checkpoint_file}: {e}")


def process_task_scenario_hallucination_reports(reports_folder, questions_folder, csvs_folder, output_folder, folder_name=""):
    """Process all reports and calculate task and scenario-wise hallucination metrics."""
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Load question mapping
    print("Loading question mapping...")
    question_mapping = load_question_mapping(questions_folder)
    print(f"Loaded {len(question_mapping)} questions")
    
    # Try to load previous results
    existing_results, processed_ids = load_intermediate_results(output_folder)
    
    if existing_results:
        results = existing_results
        detailed_results = results.get('detailed_results', [])
        print(f"Resuming from previous checkpoint with {len(detailed_results)} completed evaluations")
    else:
        results = {
            'summary': {
                'total_reports': 0,
                'processed_successfully': 0,
                'failed': 0
            },
            'task_metrics': {},
            'scenario_metrics': {},
            'task_scenario_metrics': {},
            'detailed_results': []
        }
        detailed_results = []
        processed_ids = set()
    
    # Find all response.md files in the task/scenario structure
    report_files = []
    for task_folder in os.listdir(reports_folder):
        task_path = os.path.join(reports_folder, task_folder)
        if not os.path.isdir(task_path):
            continue
            
        for scenario_folder in os.listdir(task_path):
            scenario_path = os.path.join(task_path, scenario_folder)
            if not os.path.isdir(scenario_path):
                continue
                
            for question_id in os.listdir(scenario_path):
                question_path = os.path.join(scenario_path, question_id)
                if not os.path.isdir(question_path):
                    continue
                    
                response_file = os.path.join(question_path, "response.md")
                if os.path.exists(response_file):
                    report_files.append({
                        'file_path': response_file,
                        'task': task_folder,
                        'scenario': scenario_folder,
                        'question_id': question_id
                    })
    
    if not report_files:
        print(f"No response.md files found in {reports_folder}")
        return
    
    # Update total reports count
    results['summary']['total_reports'] = len(report_files)
    
    # Filter out already processed reports
    remaining_reports = [r for r in report_files if r['question_id'] not in processed_ids]
    
    print(f"Total reports found: {len(report_files)}")
    print(f"Already processed: {len(processed_ids)}")
    print(f"Remaining to process: {len(remaining_reports)}")
    
    if not remaining_reports:
        print("All reports have been processed. Generating final results...")
        generate_final_hallucination_results(results, output_folder, folder_name)
        return results
    
    # Create timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Store metrics by task and scenario
    task_metrics = defaultdict(lambda: defaultdict(list))
    scenario_metrics = defaultdict(lambda: defaultdict(list))
    task_scenario_metrics = defaultdict(lambda: defaultdict(list))
    
    # Load existing metrics from detailed results
    for result in detailed_results:
        task = result['task']
        scenario = result['scenario'] 
        task_scenario_key = f"{task}_{scenario}"
        evaluation = result['evaluation']
        
        if evaluation['Hallucinated_papers_cited'] is not None and evaluation['Total_number_of_papers_cited'] is not None:
            hallucination_rate = evaluation['Hallucinated_papers_cited'] / max(evaluation['Total_number_of_papers_cited'], 1)
            
            task_metrics[task]['hallucination_rate'].append(hallucination_rate)
            task_metrics[task]['hallucinated_papers'].append(evaluation['Hallucinated_papers_cited'])
            task_metrics[task]['total_papers'].append(evaluation['Total_number_of_papers_cited'])
            
            scenario_metrics[scenario]['hallucination_rate'].append(hallucination_rate)
            scenario_metrics[scenario]['hallucinated_papers'].append(evaluation['Hallucinated_papers_cited'])
            scenario_metrics[scenario]['total_papers'].append(evaluation['Total_number_of_papers_cited'])
            
            task_scenario_metrics[task_scenario_key]['hallucination_rate'].append(hallucination_rate)
            task_scenario_metrics[task_scenario_key]['hallucinated_papers'].append(evaluation['Hallucinated_papers_cited'])
            task_scenario_metrics[task_scenario_key]['total_papers'].append(evaluation['Total_number_of_papers_cited'])
    
    processed_count = len(detailed_results)
    failed_count = results['summary']['failed']
    
    # Process remaining reports with max 3 concurrent threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit processing tasks
        future_to_report = {}
        for report_info in remaining_reports:
            future = executor.submit(process_single_hallucination_report, report_info, question_mapping, csvs_folder, folder_name)
            future_to_report[future] = report_info
        
        # Process completed tasks
        for i, future in enumerate(as_completed(future_to_report.keys())):
            result = future.result()
            
            if result is None:
                failed_count += 1
                continue
            
            detailed_results.append(result)
            
            # Extract metrics for aggregation
            task = result['task']
            scenario = result['scenario']
            task_scenario_key = f"{task}_{scenario}"
            evaluation = result['evaluation']
            
            if evaluation['Total_number_of_papers_cited'] > 0:
                hallucination_rate = evaluation['Hallucinated_papers_cited'] / evaluation['Total_number_of_papers_cited']
            else:
                hallucination_rate = 0.0
            
            # Store by task
            task_metrics[task]['hallucination_rate'].append(hallucination_rate)
            task_metrics[task]['hallucinated_papers'].append(evaluation['Hallucinated_papers_cited'])
            task_metrics[task]['total_papers'].append(evaluation['Total_number_of_papers_cited'])
            
            # Store by scenario
            scenario_metrics[scenario]['hallucination_rate'].append(hallucination_rate)
            scenario_metrics[scenario]['hallucinated_papers'].append(evaluation['Hallucinated_papers_cited'])
            scenario_metrics[scenario]['total_papers'].append(evaluation['Total_number_of_papers_cited'])
            
            # Store by task-scenario combination
            task_scenario_metrics[task_scenario_key]['hallucination_rate'].append(hallucination_rate)
            task_scenario_metrics[task_scenario_key]['hallucinated_papers'].append(evaluation['Hallucinated_papers_cited'])
            task_scenario_metrics[task_scenario_key]['total_papers'].append(evaluation['Total_number_of_papers_cited'])
            
            processed_count += 1
            
            # Save intermediate results every 10 reports
            if (i + 1) % 10 == 0:
                results['detailed_results'] = detailed_results
                results['summary']['processed_successfully'] = processed_count
                results['summary']['failed'] = failed_count
                save_intermediate_results(results, output_folder, timestamp)
    
    # Update results with final counts
    results['detailed_results'] = detailed_results
    results['summary']['processed_successfully'] = processed_count
    results['summary']['failed'] = failed_count
    
    # Calculate final aggregated metrics
    calculate_aggregated_hallucination_metrics(results, task_metrics, scenario_metrics, task_scenario_metrics)
    
    # Generate and save final results
    generate_final_hallucination_results(results, output_folder, folder_name)
    
    # Clean up intermediate checkpoint files
    cleanup_checkpoint_files(output_folder, timestamp)
    
    print(f"\nResults saved to: {output_folder}")
    
    return results


def calculate_aggregated_hallucination_metrics(results, task_metrics, scenario_metrics, task_scenario_metrics):
    """Calculate aggregated metrics for tasks, scenarios, and task-scenario combinations."""
    
    # Calculate task-wise means
    for task, metrics in task_metrics.items():
        task_means = {}
        for metric_name, values in metrics.items():
            if values:
                task_means[metric_name] = {
                    'mean': mean(values),
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'sum': sum(values) if metric_name in ['hallucinated_papers', 'total_papers'] else None
                }
        results['task_metrics'][task] = task_means
    
    # Calculate scenario-wise means  
    for scenario, metrics in scenario_metrics.items():
        scenario_means = {}
        for metric_name, values in metrics.items():
            if values:
                scenario_means[metric_name] = {
                    'mean': mean(values),
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'sum': sum(values) if metric_name in ['hallucinated_papers', 'total_papers'] else None
                }
        results['scenario_metrics'][scenario] = scenario_means
    
    # Calculate task-scenario combination means
    for task_scenario, metrics in task_scenario_metrics.items():
        ts_means = {}
        for metric_name, values in metrics.items():
            if values:
                ts_means[metric_name] = {
                    'mean': mean(values),
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'sum': sum(values) if metric_name in ['hallucinated_papers', 'total_papers'] else None
                }
        results['task_scenario_metrics'][task_scenario] = ts_means


def generate_final_hallucination_results(results, output_folder, folder_name=""):
    """Generate final results files."""
    
    # Save detailed results to JSON
    if folder_name:
        results_file = os.path.join(output_folder, f"hallucination_metrics_analysis_{folder_name}.json")
    else:
        results_file = os.path.join(output_folder, "hallucination_metrics_analysis.json")
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate and save summary report
    summary_file = save_hallucination_summary_report(results, output_folder, folder_name)
    
    print(f"Final results saved:")
    print(f"  Detailed results: {results_file}")
    print(f"  Summary report: {summary_file}")


def process_multiple_folders_hallucination_parallel(reports_folders, questions_folder, csvs_folder, output_base_folder):
    """Process multiple report folders in parallel for hallucination analysis."""
    results = {}
    
    with ThreadPoolExecutor(max_workers=min(len(reports_folders), 3)) as executor:
        # Submit all folder processing tasks
        future_to_folder = {}
        for folder_path in reports_folders:
            folder_name = os.path.basename(folder_path)
            # Create separate output folder for each source folder
            output_folder = os.path.join(output_base_folder, folder_name)
            future = executor.submit(
                process_task_scenario_hallucination_reports, 
                folder_path, 
                questions_folder, 
                csvs_folder, 
                output_folder, 
                folder_name
            )
            future_to_folder[future] = folder_name
        
        # Collect results
        for future in as_completed(future_to_folder.keys()):
            folder_name = future_to_folder[future]
            try:
                folder_results = future.result()
                results[folder_name] = folder_results
                print(f"Completed processing folder: {folder_name}")
            except Exception as e:
                print(f"Error processing folder {folder_name}: {str(e)}")
                results[folder_name] = None
    
    return results


def generate_hallucination_summary_report(results, output_folder):
    """Generate a human-readable summary report for hallucination metrics."""
    
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("HALLUCINATION METRICS ANALYSIS - TASK AND SCENARIO-WISE")
    report_lines.append("="*80)
    
    # Summary
    summary = results['summary']
    report_lines.append(f"\nSUMMARY:")
    report_lines.append(f"  Total reports: {summary['total_reports']}")
    report_lines.append(f"  Processed successfully: {summary['processed_successfully']}")
    report_lines.append(f"  Failed: {summary['failed']}")
    
    # Task-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-WISE HALLUCINATION METRICS")
    report_lines.append("="*80)
    
    for task, metrics in results['task_metrics'].items():
        report_lines.append(f"\n{task}:")
        
        for metric_name, stats in metrics.items():
            if metric_name == 'hallucination_rate':
                report_lines.append(f"  Hallucination Rate: {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            elif metric_name == 'hallucinated_papers':
                report_lines.append(f"  Hallucinated Papers: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
            elif metric_name == 'total_papers':
                report_lines.append(f"  Total Papers Cited: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
    
    # Scenario-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("SCENARIO-WISE HALLUCINATION METRICS")
    report_lines.append("="*80)
    
    for scenario, metrics in results['scenario_metrics'].items():
        report_lines.append(f"\n{scenario}:")
        
        for metric_name, stats in metrics.items():
            if metric_name == 'hallucination_rate':
                report_lines.append(f"  Hallucination Rate: {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            elif metric_name == 'hallucinated_papers':
                report_lines.append(f"  Hallucinated Papers: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
            elif metric_name == 'total_papers':
                report_lines.append(f"  Total Papers Cited: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
    
    # Task-Scenario combination metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-SCENARIO COMBINATION HALLUCINATION METRICS")
    report_lines.append("="*80)
    
    for task_scenario, metrics in results['task_scenario_metrics'].items():
        report_lines.append(f"\n{task_scenario.replace('_', ' / ')}:")
        
        for metric_name, stats in metrics.items():
            if metric_name == 'hallucination_rate':
                report_lines.append(f"  Hallucination Rate: {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            elif metric_name == 'hallucinated_papers':
                report_lines.append(f"  Hallucinated Papers: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
            elif metric_name == 'total_papers':
                report_lines.append(f"  Total Papers Cited: {stats['mean']:.2f} avg, {stats['sum']} total (n={stats['count']})")
    
    # Save summary report
    summary_file = os.path.join(output_folder, "hallucination_metrics_summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # Print summary to console
    for line in report_lines:
        print(line)


if __name__ == "__main__":
    # Default folder paths - matching common_metrics_per_scenario_per_task.py
    default_reports_folders = [
        r"./final_testing_codes\task_scenario_responses_thought"
    ]
    default_questions_folder = r"./generate_questions\generated_questions"
    default_csvs_folder = r"./all_final_csvs_finall"
    default_output_folder = r"./final_evals\hallucination_analysis"
    
    # Allow command line arguments for folder paths
    if len(sys.argv) > 1:
        # Parse multiple reports folders
        reports_folders = []
        questions_folder = default_questions_folder
        csvs_folder = default_csvs_folder
        output_folder = default_output_folder
        
        # First argument could be reports folder(s)
        if len(sys.argv) > 1:
            # Check if it's a single folder or multiple folders (comma-separated)
            folders_arg = sys.argv[1]
            if ',' in folders_arg:
                reports_folders = [f.strip() for f in folders_arg.split(',')]
            else:
                reports_folders = [folders_arg]
        
        if len(sys.argv) > 2:
            questions_folder = sys.argv[2]
        
        if len(sys.argv) > 3:
            csvs_folder = sys.argv[3]
            
        if len(sys.argv) > 4:
            output_folder = sys.argv[4]
            
    else:
        reports_folders = default_reports_folders
        questions_folder = default_questions_folder
        csvs_folder = default_csvs_folder
        output_folder = default_output_folder
    
    # Verify folders exist
    valid_reports_folders = []
    for folder in reports_folders:
        if os.path.exists(folder):
            valid_reports_folders.append(folder)
        else:
            print(f"Warning: Reports folder does not exist: {folder}")
    
    if not valid_reports_folders:
        print("Error: No valid reports folders found")
        sys.exit(1)
    
    if not os.path.exists(questions_folder):
        print(f"Error: Questions folder does not exist: {questions_folder}")
        sys.exit(1)
        
    if not os.path.exists(csvs_folder):
        print(f"Error: CSVs folder does not exist: {csvs_folder}")
        sys.exit(1)
    
    print(f"Processing {len(valid_reports_folders)} report folders:")
    for folder in valid_reports_folders:
        print(f"  - {folder}")
    print(f"Using question mapping from: {questions_folder}")
    print(f"Using available papers from: {csvs_folder}")
    print(f"Saving results to: {output_folder}")
    
    if len(valid_reports_folders) == 1:
        # Single folder processing
        folder_name = os.path.basename(valid_reports_folders[0])
        folder_output = os.path.join(output_folder, folder_name)
        
        process_task_scenario_hallucination_reports(valid_reports_folders[0], questions_folder, csvs_folder, folder_output, folder_name)
        
    else:
        # Multiple folders processing
        print(f"\nProcessing multiple folders in parallel...")
        results = process_multiple_folders_hallucination_parallel(valid_reports_folders, questions_folder, csvs_folder, output_folder)
        
        # Generate a combined summary report
        print(f"\n{'='*80}")
        print("CROSS-FOLDER COMPARISON SUMMARY")
        print(f"{'='*80}")
        
        combined_summary = []
        combined_summary.append("="*80)
        combined_summary.append("CROSS-FOLDER COMPARISON SUMMARY")
        combined_summary.append("="*80)
        
        for folder_name, result in results.items():
            if result:
                combined_summary.append(f"\n{folder_name}:")
                combined_summary.append(f"  Total reports: {result['summary']['total_reports']}")
                combined_summary.append(f"  Processed successfully: {result['summary']['processed_successfully']}")
                combined_summary.append(f"  Failed: {result['summary']['failed']}")
                
                # Add task-wise hallucination rates
                if result['task_metrics']:
                    combined_summary.append("  Task-wise hallucination rates:")
                    for task, metrics in result['task_metrics'].items():
                        if 'hallucination_rate' in metrics:
                            combined_summary.append(f"    {task}: {metrics['hallucination_rate']['mean']:.3f}")
        
        # Save combined summary
        combined_summary_file = os.path.join(output_folder, "combined_hallucination_summary_report.txt")
        with open(combined_summary_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(combined_summary))
        
        # Print combined summary
        for line in combined_summary:
            print(line)
        
        print(f"\nCombined summary saved to: {combined_summary_file}")
        print(f"Individual LLM judge results stored in: llm_evals_hallucination_thought/")
        print("Processing complete!")