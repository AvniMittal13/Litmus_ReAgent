import sys
import os
import json
import glob
from datetime import datetime
from statistics import mean
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response
from pydantic import BaseModel

class AccuracyMetricEvaluation(BaseModel):
    user_query : str
    report1_final_value : str
    report2_final_value : str
    is_similar: str



prompt = """
You are an **information extraction agent**.
Your task is to extract the **single final predicted value** from two research reports, given a user query.
The extracted values from **Report1** and **Report2** must be **directly comparable**.

---

* **User Query (Q):**

{user_query}

---

* **Report 1:**

{report_generated}

---

* **Report 2:**

{ground_truth_report}

---

### Instructions

1. Read the **user query** carefully — this specifies the prediction/value required.
2. From each report, extract the **final predicted value** that directly answers the query.
3. Ensure values are **directly comparable**:

   * If both are numeric, return them in the **same numeric scale**.

     * Example: *“83%” → `83`* (do not convert to `0.83`).
     * Example: *“0.72” and “72%”* → normalize both to `72`.
   * If both are strings (labels/categories), output the exact string as it appears (trimmed).
   * If one is numeric and the other is string, set both to `"null"` (not comparable).
4. Extract **only one final value** per report:

   * If multiple are given, choose the **definitive final answer**, not intermediate values.
   * If none is found, return `"null"`.
5. Do not include explanations, reasoning, or extra text.

If a number is present then definitely give that number as answer instead of answers like yes no etc.
Dont give range, give exact number only. if range is answer then give middle number of the range.

If the answers match to some extent then give is_similar as true, else false.
for numerics, if the answers are close in an acceptable range then true
for strings, if they mathc then true. For example if one ans is "a and b" and one is "a" then it should be true. Give this much liniency for deciding if they are similar or not.
---

### Output Format

Return **only** the following JSON object:

```json
{{
  "user_query": "<repeat the user query here>",
  "report1_final_value": "<single extracted value or null>",
  "report2_final_value": "<single extracted value or null>",
  "is_similar" : "<boolean>"
}}
```
"""


def evaluate_accuracy_comparison(report_text, ground_truth_text, user_query, query_id=None, task=None, scenario=None, folder_name=""):
    """Compare two reports and extract final values for accuracy calculation."""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = get_structured_response(
                prompt=prompt.format(
                    user_query=user_query,
                    report_generated=report_text,
                    ground_truth_report=ground_truth_text
                ),
                structuredClass=AccuracyMetricEvaluation,
                # model_name="o3-mini"
            )
            evaluation = AccuracyMetricEvaluation(**json.loads(response))
            
            # Store individual result if query_id is provided
            if query_id and task and scenario:
                store_individual_accuracy_result(evaluation, query_id, task, scenario, folder_name, report_text, ground_truth_text, user_query)
            
            return evaluation
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"API call failed for {query_id} (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"API call failed for {query_id} after {max_retries} attempts: {str(e)}")
                raise


def process_single_report_parallel(report_info, question_mapping, folder_name):
    """Process a single report pair for parallel execution."""
    question_id = report_info['question_id']
    task = report_info['task']
    scenario = report_info['scenario']
    
    try:
        # Validate files exist
        if not os.path.exists(report_info['report_file']):
            raise FileNotFoundError(f"Report file not found: {report_info['report_file']}")
        if not os.path.exists(report_info['ground_truth_file']):
            raise FileNotFoundError(f"Ground truth file not found: {report_info['ground_truth_file']}")
        
        # Read both report contents with error handling
        try:
            with open(report_info['report_file'], 'r', encoding='utf-8') as f:
                report_content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding if utf-8 fails
            with open(report_info['report_file'], 'r', encoding='latin-1') as f:
                report_content = f.read()
        
        try:
            with open(report_info['ground_truth_file'], 'r', encoding='utf-8') as f:
                ground_truth_content = f.read()
        except UnicodeDecodeError:
            with open(report_info['ground_truth_file'], 'r', encoding='latin-1') as f:
                ground_truth_content = f.read()
        
        # Validate content is not empty
        if not report_content or not report_content.strip():
            raise ValueError(f"Report file is empty: {report_info['report_file']}")
        if not ground_truth_content or not ground_truth_content.strip():
            raise ValueError(f"Ground truth file is empty: {report_info['ground_truth_file']}")
        
        # Validate content length (avoid extremely large files)
        max_content_length = 500000  # 500KB
        if len(report_content) > max_content_length:
            print(f"Warning: Report file is very large ({len(report_content)} chars): {report_info['report_file']}")
        if len(ground_truth_content) > max_content_length:
            print(f"Warning: Ground truth file is very large ({len(ground_truth_content)} chars): {report_info['ground_truth_file']}")
        
        # Get question details from mapping with validation
        if question_id not in question_mapping:
            raise KeyError(f"Question ID {question_id} not found in question mapping")
        
        question_details = question_mapping.get(question_id, {})
        user_query = question_details.get('complete_question', '')
        
        if not user_query or not user_query.strip():
            raise ValueError(f"Empty or missing user query for question {question_id}")
        
        # Evaluate the accuracy comparison
        evaluation = evaluate_accuracy_comparison(
            report_content, 
            ground_truth_content, 
            user_query,
            query_id=question_id,
            task=task,
            scenario=scenario,
            folder_name=folder_name
        )
        
        # Calculate accuracy score
        accuracy_score = calculate_accuracy(evaluation.report1_final_value, evaluation.report2_final_value)
        
        # Return detailed result
        result = {
            'question_id': question_id,
            'task': task,
            'scenario': scenario,
            'question_details': question_details,
            'evaluation': evaluation.__dict__,
            'accuracy_score': accuracy_score,
            'is_comparable': accuracy_score is not None,
            'success': True,
            'error': None,
            'report_file': report_info['report_file'],
            'ground_truth_file': report_info['ground_truth_file']
        }
        
        print(f"✓ Completed: {task}/{scenario}/{question_id} - Accuracy: {accuracy_score}")
        return result
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"✗ Error processing {task}/{scenario}/{question_id}: [{error_type}] {error_msg}")
        return {
            'question_id': question_id,
            'task': task,
            'scenario': scenario,
            'success': False,
            'error': error_msg,
            'error_type': error_type,
            'accuracy_score': None,
            'is_comparable': False,
            'report_file': report_info.get('report_file', 'unknown'),
            'ground_truth_file': report_info.get('ground_truth_file', 'unknown')
        }


def store_individual_accuracy_result(evaluation, query_id, task, scenario, folder_name, report_text, ground_truth_text, user_query):
    """Store individual LLM judge result for a query."""
    # Create directory structure: llm_evals_accuracy_thought/folder_name/task/scenario/
    results_dir = os.path.join("llm_evals_accuracy_thought", folder_name, task, scenario)
    os.makedirs(results_dir, exist_ok=True)
    
    result_data = {
        "query_id": query_id,
        "task": task,
        "scenario": scenario,
        "folder_source": folder_name,
        "user_query": user_query,
        "original_report": report_text,
        "ground_truth_report": ground_truth_text,
        "evaluation": {
            "user_query": evaluation.user_query,
            "report1_final_value": evaluation.report1_final_value,
            "report2_final_value": evaluation.report2_final_value,
            "is_similar": evaluation.is_similar
        }
    }
    
    result_file = os.path.join(results_dir, f"{query_id}_accuracy_result.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)


def calculate_accuracy(report1_value, report2_value):
    """Calculate accuracy between two extracted values."""
    # Handle null values
    if report1_value == "null" or report2_value == "null":
        return None
    
    # Try to convert to numeric for comparison
    try:
        val1 = float(report1_value)
        val2 = float(report2_value)
        # Return 1 if values are equal (within small tolerance), 0 otherwise
        return 1.0 if abs(val1 - val2) < 1e-6 else 0.0
    except (ValueError, TypeError):
        # String comparison
        return 1.0 if str(report1_value).strip().lower() == str(report2_value).strip().lower() else 0.0


def load_question_mapping(questions_folder):
    """Load question mapping from generated questions folder."""
    question_mapping = {}
    failed_files = []
    
    # Load all question files
    question_files = glob.glob(os.path.join(questions_folder, "*.json"))
    
    if not question_files:
        print(f"Warning: No question files found in {questions_folder}")
        return question_mapping
    
    for question_file in question_files:
        try:
            with open(question_file, 'r', encoding='utf-8') as f:
                question_data = json.load(f)
            
            # Validate required fields
            if 'task' not in question_data:
                print(f"Warning: Missing 'task' field in {question_file}")
                failed_files.append(question_file)
                continue
            if 'scenario' not in question_data:
                print(f"Warning: Missing 'scenario' field in {question_file}")
                failed_files.append(question_file)
                continue
            if 'questions' not in question_data:
                print(f"Warning: Missing 'questions' field in {question_file}")
                failed_files.append(question_file)
                continue
                
            task_name = question_data['task']
            scenario = question_data['scenario']
            
            for question in question_data['questions']:
                if 'unique_id' not in question:
                    print(f"Warning: Question missing 'unique_id' in {question_file}")
                    continue
                if 'complete_question' not in question:
                    print(f"Warning: Question {question.get('unique_id', 'unknown')} missing 'complete_question' in {question_file}")
                    continue
                    
                question_id = question['unique_id']
                question_mapping[question_id] = {
                    'task': task_name,
                    'scenario': scenario,
                    'complete_question': question['complete_question'],
                    'models': question.get('models', ''),
                    'languages': question.get('languages', ''),
                    'source_file': question_file
                }
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON in {question_file}: {e}")
            failed_files.append(question_file)
        except Exception as e:
            print(f"Error: Failed to load {question_file}: {e}")
            failed_files.append(question_file)
    
    if failed_files:
        print(f"Warning: Failed to load {len(failed_files)} question file(s)")
    
    print(f"Successfully loaded {len(question_mapping)} questions from {len(question_files) - len(failed_files)}/{len(question_files)} files")
    
    return question_mapping


def find_matching_reports(reports_folder, ground_truth_folder):
    """Find matching reports between the two folders."""
    matching_reports = []
    
    # Find all response.md files in both folders
    for task_folder in os.listdir(reports_folder):
        task_path = os.path.join(reports_folder, task_folder)
        gt_task_path = os.path.join(ground_truth_folder, task_folder)
        
        if not os.path.isdir(task_path) or not os.path.isdir(gt_task_path):
            continue
            
        for scenario_folder in os.listdir(task_path):
            scenario_path = os.path.join(task_path, scenario_folder)
            gt_scenario_path = os.path.join(gt_task_path, scenario_folder)
            
            if not os.path.isdir(scenario_path) or not os.path.isdir(gt_scenario_path):
                continue
                
            for question_id in os.listdir(scenario_path):
                question_path = os.path.join(scenario_path, question_id)
                gt_question_path = os.path.join(gt_scenario_path, question_id)
                
                if not os.path.isdir(question_path) or not os.path.isdir(gt_question_path):
                    continue
                    
                response_file = os.path.join(question_path, "response.md")
                gt_response_file = os.path.join(gt_question_path, "response.md")
                
                if os.path.exists(response_file) and os.path.exists(gt_response_file):
                    matching_reports.append({
                        'report_file': response_file,
                        'ground_truth_file': gt_response_file,
                        'task': task_folder,
                        'scenario': scenario_folder,
                        'question_id': question_id
                    })
    
    return matching_reports


def save_intermediate_results(results, output_folder, timestamp):
    """Save intermediate results with timestamp."""
    checkpoint_file = os.path.join(output_folder, f"accuracy_checkpoint_{timestamp}.json")
    
    # Convert evaluation objects to dict for JSON serialization
    serializable_results = json.loads(json.dumps(results, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x)))
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    print(f"Intermediate results saved to: {checkpoint_file}")
    
    # Save failed results separately for easy debugging
    failed_results = [r for r in results.get('detailed_results', []) if not r.get('success', True)]
    if failed_results:
        failed_file = os.path.join(output_folder, f"failed_evaluations_{timestamp}.json")
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed_results, f, indent=2, ensure_ascii=False)
        print(f"Failed evaluations saved to: {failed_file}")
    
    return checkpoint_file


def load_intermediate_results(output_folder):
    """Load the most recent checkpoint file."""
    checkpoint_files = glob.glob(os.path.join(output_folder, "accuracy_checkpoint_*.json"))
    
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
    checkpoint_files = glob.glob(os.path.join(output_folder, "accuracy_checkpoint_*.json"))
    
    for checkpoint_file in checkpoint_files:
        # Don't delete the current timestamp file (it becomes the final results)
        if current_timestamp not in checkpoint_file:
            try:
                os.remove(checkpoint_file)
                print(f"Cleaned up checkpoint file: {checkpoint_file}")
            except Exception as e:
                print(f"Error cleaning up {checkpoint_file}: {e}")


def process_task_scenario_accuracy_reports(reports_folder, ground_truth_folder, questions_folder, output_folder, folder_name="task_scenario_responses"):
    """Process all reports and calculate task and scenario-wise accuracy metrics."""
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Load question mapping
    print("Loading question mapping...")
    question_mapping = load_question_mapping(questions_folder)
    print(f"Loaded {len(question_mapping)} questions")
    
    if not question_mapping:
        print("Error: No questions loaded from question mapping. Cannot proceed.")
        return
    
    # Find matching reports
    print("Finding matching reports...")
    matching_reports = find_matching_reports(reports_folder, ground_truth_folder)
    print(f"Found {len(matching_reports)} matching report pairs")
    
    if not matching_reports:
        print("No matching reports found.")
        return
    
    # Validate that report question IDs exist in mapping
    missing_questions = []
    for report in matching_reports:
        if report['question_id'] not in question_mapping:
            missing_questions.append(report['question_id'])
    
    if missing_questions:
        print(f"Warning: {len(missing_questions)} report(s) have question IDs not found in question mapping")
        print(f"First 5 missing IDs: {missing_questions[:5]}")
        print(f"These reports will fail during processing. Consider checking your question files.")
    
    # Try to load previous results
    existing_results, processed_ids = load_intermediate_results(output_folder)
    
    if existing_results:
        results = existing_results
        detailed_results = results.get('detailed_results', [])
        print(f"Resuming from previous checkpoint with {len(detailed_results)} completed evaluations")
    else:
        results = {
            'summary': {
                'total_report_pairs': 0,
                'processed_successfully': 0,
                'failed': 0,
                'comparable_pairs': 0,
                'non_comparable_pairs': 0
            },
            'task_metrics': {},
            'scenario_metrics': {},
            'task_scenario_metrics': {},
            'detailed_results': []
        }
        detailed_results = []
        processed_ids = set()
    
    # Update total reports count
    results['summary']['total_report_pairs'] = len(matching_reports)
    
    # Filter out already processed reports
    remaining_reports = [r for r in matching_reports if r['question_id'] not in processed_ids]
    
    print(f"Total report pairs found: {len(matching_reports)}")
    print(f"Already processed: {len(processed_ids)}")
    print(f"Remaining to process: {len(remaining_reports)}")
    
    if not remaining_reports:
        print("All reports have been processed. Generating final results...")
        generate_final_accuracy_results(results, output_folder)
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
        
        if result.get('accuracy_score') is not None:
            task_metrics[task]['accuracy'].append(result['accuracy_score'])
            scenario_metrics[scenario]['accuracy'].append(result['accuracy_score'])
            task_scenario_metrics[task_scenario_key]['accuracy'].append(result['accuracy_score'])
    
    processed_count = len(detailed_results)
    failed_count = results['summary']['failed']
    comparable_pairs = results['summary'].get('comparable_pairs', 0)
    non_comparable_pairs = results['summary'].get('non_comparable_pairs', 0)
    
    # Process reports in parallel batches
    batch_size = 5  # Process 5 reports in parallel
    total_batches = (len(remaining_reports) + batch_size - 1) // batch_size
    
    print(f"Processing {len(remaining_reports)} reports in {total_batches} batches of {batch_size}")
    
    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(remaining_reports))
        batch_reports = remaining_reports[start_idx:end_idx]
        
        print(f"Processing batch {batch_idx + 1}/{total_batches} ({len(batch_reports)} reports)")
        
        # Process batch in parallel
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            # Submit all tasks in the batch
            future_to_report = {
                executor.submit(process_single_report_parallel, report_info, question_mapping, folder_name): report_info
                for report_info in batch_reports
            }
            
            # Collect results as they complete
            batch_results = []
            for future in as_completed(future_to_report):
                report_info = future_to_report[future]
                try:
                    result = future.result()
                    batch_results.append(result)
                    
                    if result['success']:
                        # Track comparable vs non-comparable pairs
                        if result['accuracy_score'] is not None:
                            comparable_pairs += 1
                        else:
                            non_comparable_pairs += 1
                        
                        # Extract metrics for aggregation (only for comparable pairs)
                        if result['accuracy_score'] is not None:
                            task = result['task']
                            scenario = result['scenario']
                            task_scenario_key = f"{task}_{scenario}"
                            
                            # Store by task
                            task_metrics[task]['accuracy'].append(result['accuracy_score'])
                            # Store by scenario
                            scenario_metrics[scenario]['accuracy'].append(result['accuracy_score'])
                            # Store by task-scenario combination
                            task_scenario_metrics[task_scenario_key]['accuracy'].append(result['accuracy_score'])
                        
                        processed_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Error getting result for {report_info['question_id']}: {str(e)}")
                    failed_count += 1
            
            # Add successful results to detailed_results
            for result in batch_results:
                if result['success']:
                    detailed_results.append(result)
        
        # Save intermediate results after each batch
        results['detailed_results'] = detailed_results
        results['summary']['processed_successfully'] = processed_count
        results['summary']['failed'] = failed_count
        results['summary']['comparable_pairs'] = comparable_pairs
        results['summary']['non_comparable_pairs'] = non_comparable_pairs
        save_intermediate_results(results, output_folder, timestamp)
        
        print(f"Batch {batch_idx + 1} completed. Processed: {processed_count}, Failed: {failed_count}")
    
    # Update results with final counts
    results['detailed_results'] = detailed_results
    results['summary']['processed_successfully'] = processed_count
    results['summary']['failed'] = failed_count
    results['summary']['comparable_pairs'] = comparable_pairs
    results['summary']['non_comparable_pairs'] = non_comparable_pairs
    
    # Calculate final aggregated metrics
    calculate_aggregated_accuracy_metrics(results, task_metrics, scenario_metrics, task_scenario_metrics)
    
    # Generate and save final results
    generate_final_accuracy_results(results, output_folder)
    
    # Clean up intermediate checkpoint files
    cleanup_checkpoint_files(output_folder, timestamp)
    
    print(f"\n{'='*80}")
    print(f"PROCESSING COMPLETE")
    print(f"{'='*80}")
    print(f"Total report pairs: {results['summary']['total_report_pairs']}")
    print(f"Successfully processed: {processed_count}")
    print(f"Failed: {failed_count}")
    if failed_count > 0:
        print(f"  → Check failed_evaluations_{timestamp}.json for error details")
    print(f"Comparable pairs: {comparable_pairs}")
    print(f"Non-comparable pairs: {non_comparable_pairs}")
    print(f"\nResults saved to: {output_folder}")
    print(f"{'='*80}")
    
    return results


def calculate_aggregated_accuracy_metrics(results, task_metrics, scenario_metrics, task_scenario_metrics):
    """Calculate aggregated accuracy metrics for tasks, scenarios, and task-scenario combinations."""
    
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
                    'sum': sum(values)
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
                    'sum': sum(values)
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
                    'sum': sum(values)
                }
        results['task_scenario_metrics'][task_scenario] = ts_means


def generate_final_accuracy_results(results, output_folder):
    """Generate final results files."""
    
    # Save detailed results to JSON
    results_file = os.path.join(output_folder, "accuracy_metrics_analysis.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate and save summary report
    generate_accuracy_summary_report(results, output_folder)
    
    print(f"Final results saved:")
    print(f"  Detailed results: {results_file}")
    print(f"  Summary report: {os.path.join(output_folder, 'accuracy_metrics_summary.txt')}")


def generate_accuracy_summary_report(results, output_folder):
    """Generate a human-readable summary report for accuracy metrics."""
    
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("ACCURACY METRICS ANALYSIS - TASK AND SCENARIO-WISE")
    report_lines.append("="*80)
    
    # Summary
    summary = results['summary']
    report_lines.append(f"\nSUMMARY:")
    report_lines.append(f"  Total report pairs: {summary['total_report_pairs']}")
    report_lines.append(f"  Processed successfully: {summary['processed_successfully']}")
    report_lines.append(f"  Failed: {summary['failed']}")
    report_lines.append(f"  Comparable pairs: {summary['comparable_pairs']}")
    report_lines.append(f"  Non-comparable pairs: {summary['non_comparable_pairs']}")
    
    if summary['comparable_pairs'] > 0:
        comparability_rate = summary['comparable_pairs'] / (summary['comparable_pairs'] + summary['non_comparable_pairs'])
        report_lines.append(f"  Comparability rate: {comparability_rate:.3f}")
    
    # Task-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-WISE ACCURACY METRICS")
    report_lines.append("="*80)
    
    for task, metrics in results['task_metrics'].items():
        report_lines.append(f"\n{task}:")
        
        if 'accuracy' in metrics:
            stats = metrics['accuracy']
            report_lines.append(f"  Accuracy: {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            report_lines.append(f"  Correct predictions: {int(stats['sum'])}/{stats['count']}")
    
    # Scenario-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("SCENARIO-WISE ACCURACY METRICS")
    report_lines.append("="*80)
    
    for scenario, metrics in results['scenario_metrics'].items():
        report_lines.append(f"\n{scenario}:")
        
        if 'accuracy' in metrics:
            stats = metrics['accuracy']
            report_lines.append(f"  Accuracy: {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            report_lines.append(f"  Correct predictions: {int(stats['sum'])}/{stats['count']}")
    
    # Task-Scenario combination metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-SCENARIO COMBINATION ACCURACY METRICS")
    report_lines.append("="*80)
    
    for task_scenario, metrics in results['task_scenario_metrics'].items():
        report_lines.append(f"\n{task_scenario.replace('_', ' / ')}:")
        
        if 'accuracy' in metrics:
            stats = metrics['accuracy']
            report_lines.append(f"  Accuracy: {stats['mean']:.3f} (n={stats['count']}, range: {stats['min']:.3f}-{stats['max']:.3f})")
            report_lines.append(f"  Correct predictions: {int(stats['sum'])}/{stats['count']}")
    
    # Save summary report
    summary_file = os.path.join(output_folder, "accuracy_metrics_summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # Print summary to console
    for line in report_lines:
        print(line)


if __name__ == "__main__":
    # Default folder paths
    default_reports_folder = r"./final_testing_codes\task_scenario_new_final_1_responses"
    default_ground_truth_folder = r"./final_testing_codes\task_scenario_new_final_1_responses_combined"
    default_questions_folder = r"./generated_questions"
    default_output_folder = r"./final_evals\accuracy_analysis_new_final_1"
    
    # Allow command line arguments for folder paths
    if len(sys.argv) > 1:
        reports_folder = sys.argv[1]
        ground_truth_folder = sys.argv[2] if len(sys.argv) > 2 else default_ground_truth_folder
        questions_folder = sys.argv[3] if len(sys.argv) > 3 else default_questions_folder
        output_folder = sys.argv[4] if len(sys.argv) > 4 else default_output_folder
    else:
        reports_folder = default_reports_folder
        ground_truth_folder = default_ground_truth_folder
        questions_folder = default_questions_folder
        output_folder = default_output_folder
    
    # Verify folders exist
    if not os.path.exists(reports_folder):
        print(f"Error: Reports folder does not exist: {reports_folder}")
        sys.exit(1)
    
    if not os.path.exists(ground_truth_folder):
        print(f"Error: Ground truth folder does not exist: {ground_truth_folder}")
        sys.exit(1)
    
    if not os.path.exists(questions_folder):
        print(f"Error: Questions folder does not exist: {questions_folder}")
        sys.exit(1)
    
    print(f"Processing reports in: {reports_folder}")
    print(f"Using ground truth from: {ground_truth_folder}")
    print(f"Using question mapping from: {questions_folder}")
    print(f"Saving results to: {output_folder}")
    
    # Extract folder name from reports_folder path for individual result storage
    folder_name = os.path.basename(reports_folder.rstrip(os.sep))
    
    process_task_scenario_accuracy_reports(reports_folder, ground_truth_folder, questions_folder, output_folder, folder_name)