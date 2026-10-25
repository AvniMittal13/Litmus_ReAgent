import sys
import os
import json
import glob
from datetime import datetime
from statistics import mean
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_chat_response
from pydantic import BaseModel

class ToolRelevanceEvaluation(BaseModel):
    query: str
    thought_name: str
    is_relevant: bool
    reasoning: str


def evaluate_tool_call_relevance(tool_query, thought_name, thought_context, max_retries=3):
    """Evaluate if a tool call query is relevant for answering the thought."""
    
    prompt = f"""You are evaluating whether a web search/crawl tool call query is relevant for answering a specific research thought/hypothesis.

**Thought Name:** {thought_name}

**Thought Context:**
{thought_context}

**Tool Call Query:**
{tool_query}

**Task:**
Determine if this tool call query is relevant and useful for answering or investigating the thought/hypothesis above.

A query is **RELEVANT (1)** if:
- It directly searches for information needed to test the hypothesis
- It seeks data, benchmarks, or evidence mentioned in the thought's method
- It looks for papers, documentation, or results that would help answer the thought
- It searches for related concepts, models, or comparisons needed for analysis

A query is **NOT RELEVANT (0)** if:
- It searches for completely unrelated topics
- It duplicates information already available in the thought context
- It's too vague or generic to be useful
- It searches for information not needed for this specific thought

Provide your evaluation as:
- is_relevant: true or false
- reasoning: Brief explanation (1-2 sentences)

Return your response in this JSON format:
{{
    "query": "{tool_query}",
    "thought_name": "{thought_name}",
    "is_relevant": true/false,
    "reasoning": "your explanation here"
}}
"""

    retry_delay = 2
    for attempt in range(max_retries):
        try:
            response = get_chat_response(
                messages=[{"role": "user", "content": prompt}],
                output_dir=None
            )
            
            # Try to parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                evaluation_data = json.loads(json_str)
                evaluation = ToolRelevanceEvaluation(**evaluation_data)
                return evaluation
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"API call failed (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"API call failed after {max_retries} attempts: {str(e)}")
                # Return a default failed evaluation
                return ToolRelevanceEvaluation(
                    query=tool_query,
                    thought_name=thought_name,
                    is_relevant=False,
                    reasoning=f"Evaluation failed: {str(e)}"
                )


def extract_tool_calls_from_conversation(conversation_hierarchy_file):
    """Extract all tool invocations from conversation hierarchy."""
    
    if not os.path.exists(conversation_hierarchy_file):
        return None
    
    try:
        with open(conversation_hierarchy_file, 'r', encoding='utf-8') as f:
            hierarchy = json.load(f)
    except Exception as e:
        print(f"Error reading {conversation_hierarchy_file}: {e}")
        return None
    
    # Extract tool calls from each thought agent
    thought_agents = hierarchy.get('thought_agents', {})
    
    results = []
    
    for thought_name, thought_data in thought_agents.items():
        thought_info = thought_data.get('thought', {})
        intermediates = thought_data.get('intermediates', {})
        tool_invocations = intermediates.get('tool_invocations', [])
        
        # Build thought context from thought info
        thought_context = f"""
Hypothesis: {thought_info.get('hypothesis', 'N/A')}
Method: {thought_info.get('method', 'N/A')}
Background: {thought_info.get('background', 'N/A')}
"""
        
        # Extract each tool call
        for tool_call in tool_invocations:
            query = tool_call.get('query', '')
            if query:  # Only process non-empty queries
                results.append({
                    'thought_name': thought_name,
                    'thought_context': thought_context,
                    'tool_query': query,
                    'tool_call_data': tool_call
                })
    
    return results


def process_single_conversation_parallel(conversation_file, question_id, task, scenario):
    """Process a single conversation hierarchy file for tool relevance evaluation."""
    
    try:
        # Extract tool calls
        tool_calls = extract_tool_calls_from_conversation(conversation_file)
        
        if not tool_calls:
            return {
                'question_id': question_id,
                'task': task,
                'scenario': scenario,
                'success': True,
                'total_tool_calls': 0,
                'relevant_tool_calls': 0,
                'relevance_percentage': None,
                'tool_evaluations': [],
                'error': None
            }
        
        # Evaluate each tool call
        evaluations = []
        relevant_count = 0
        
        for tool_call_info in tool_calls:
            evaluation = evaluate_tool_call_relevance(
                tool_query=tool_call_info['tool_query'],
                thought_name=tool_call_info['thought_name'],
                thought_context=tool_call_info['thought_context']
            )
            
            evaluations.append({
                'thought_name': tool_call_info['thought_name'],
                'query': tool_call_info['tool_query'],
                'is_relevant': evaluation.is_relevant,
                'reasoning': evaluation.reasoning
            })
            
            if evaluation.is_relevant:
                relevant_count += 1
        
        total_calls = len(evaluations)
        relevance_percentage = (relevant_count / total_calls * 100) if total_calls > 0 else 0
        
        result = {
            'question_id': question_id,
            'task': task,
            'scenario': scenario,
            'success': True,
            'total_tool_calls': total_calls,
            'relevant_tool_calls': relevant_count,
            'relevance_percentage': relevance_percentage,
            'tool_evaluations': evaluations,
            'error': None
        }
        
        print(f"✓ Completed: {task}/{scenario}/{question_id} - {relevant_count}/{total_calls} relevant ({relevance_percentage:.1f}%)")
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
            'total_tool_calls': 0,
            'relevant_tool_calls': 0,
            'relevance_percentage': None,
            'tool_evaluations': []
        }


def find_conversation_hierarchy_files(responses_folder):
    """Find all conversation_hierarchy.json files in the responses folder."""
    
    matching_files = []
    
    for task_folder in os.listdir(responses_folder):
        task_path = os.path.join(responses_folder, task_folder)
        
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
                    
                conversation_file = os.path.join(question_path, "conversation_hierarchy.json")
                
                if os.path.exists(conversation_file):
                    matching_files.append({
                        'conversation_file': conversation_file,
                        'task': task_folder,
                        'scenario': scenario_folder,
                        'question_id': question_id
                    })
    
    return matching_files


def save_intermediate_results(results, output_folder, timestamp):
    """Save intermediate results with timestamp."""
    checkpoint_file = os.path.join(output_folder, f"tool_relevance_checkpoint_{timestamp}.json")
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Intermediate results saved to: {checkpoint_file}")
    
    # Save failed results separately
    failed_results = [r for r in results.get('detailed_results', []) if not r.get('success', True)]
    if failed_results:
        failed_file = os.path.join(output_folder, f"failed_tool_evaluations_{timestamp}.json")
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed_results, f, indent=2, ensure_ascii=False)
        print(f"Failed evaluations saved to: {failed_file}")
    
    return checkpoint_file


def load_intermediate_results(output_folder):
    """Load the most recent checkpoint file."""
    checkpoint_files = glob.glob(os.path.join(output_folder, "tool_relevance_checkpoint_*.json"))
    
    if not checkpoint_files:
        return None, None
    
    latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
    
    try:
        with open(latest_checkpoint, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
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
    checkpoint_files = glob.glob(os.path.join(output_folder, "tool_relevance_checkpoint_*.json"))
    
    for checkpoint_file in checkpoint_files:
        if current_timestamp not in checkpoint_file:
            try:
                os.remove(checkpoint_file)
                print(f"Cleaned up checkpoint file: {checkpoint_file}")
            except Exception as e:
                print(f"Error cleaning up {checkpoint_file}: {e}")


def process_tool_relevance_evaluation(responses_folder, output_folder):
    """Process all conversation hierarchies and evaluate tool call relevance."""
    
    os.makedirs(output_folder, exist_ok=True)
    
    print("Finding conversation hierarchy files...")
    conversation_files = find_conversation_hierarchy_files(responses_folder)
    print(f"Found {len(conversation_files)} conversation files")
    
    if not conversation_files:
        print("No conversation files found.")
        return
    
    # Try to load previous results
    existing_results, processed_ids = load_intermediate_results(output_folder)
    
    if existing_results:
        results = existing_results
        detailed_results = results.get('detailed_results', [])
        print(f"Resuming from previous checkpoint with {len(detailed_results)} completed evaluations")
    else:
        results = {
            'summary': {
                'total_conversations': 0,
                'processed_successfully': 0,
                'failed': 0,
                'total_tool_calls': 0,
                'total_relevant_calls': 0,
                'overall_relevance_percentage': 0
            },
            'task_metrics': {},
            'scenario_metrics': {},
            'task_scenario_metrics': {},
            'detailed_results': []
        }
        detailed_results = []
        processed_ids = set()
    
    results['summary']['total_conversations'] = len(conversation_files)
    
    # Filter out already processed
    remaining_files = [f for f in conversation_files if f['question_id'] not in processed_ids]
    
    print(f"Total conversations: {len(conversation_files)}")
    print(f"Already processed: {len(processed_ids)}")
    print(f"Remaining to process: {len(remaining_files)}")
    
    if not remaining_files:
        print("All conversations have been processed. Generating final results...")
        generate_final_tool_relevance_results(results, output_folder)
        return results
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Store metrics by task and scenario
    task_metrics = defaultdict(lambda: defaultdict(list))
    scenario_metrics = defaultdict(lambda: defaultdict(list))
    task_scenario_metrics = defaultdict(lambda: defaultdict(list))
    
    # Load existing metrics
    for result in detailed_results:
        if result.get('relevance_percentage') is not None:
            task = result['task']
            scenario = result['scenario']
            task_scenario_key = f"{task}_{scenario}"
            
            task_metrics[task]['relevance'].append(result['relevance_percentage'])
            scenario_metrics[scenario]['relevance'].append(result['relevance_percentage'])
            task_scenario_metrics[task_scenario_key]['relevance'].append(result['relevance_percentage'])
    
    processed_count = len(detailed_results)
    failed_count = results['summary']['failed']
    total_tool_calls = results['summary'].get('total_tool_calls', 0)
    total_relevant_calls = results['summary'].get('total_relevant_calls', 0)
    
    # Process in parallel batches
    batch_size = 3  # Smaller batch for LLM evaluation
    total_batches = (len(remaining_files) + batch_size - 1) // batch_size
    
    print(f"Processing {len(remaining_files)} conversations in {total_batches} batches of {batch_size}")
    
    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(remaining_files))
        batch_files = remaining_files[start_idx:end_idx]
        
        print(f"Processing batch {batch_idx + 1}/{total_batches} ({len(batch_files)} conversations)")
        
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_file = {
                executor.submit(
                    process_single_conversation_parallel,
                    file_info['conversation_file'],
                    file_info['question_id'],
                    file_info['task'],
                    file_info['scenario']
                ): file_info
                for file_info in batch_files
            }
            
            batch_results = []
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                try:
                    result = future.result()
                    batch_results.append(result)
                    
                    if result['success']:
                        total_tool_calls += result['total_tool_calls']
                        total_relevant_calls += result['relevant_tool_calls']
                        
                        if result['relevance_percentage'] is not None:
                            task = result['task']
                            scenario = result['scenario']
                            task_scenario_key = f"{task}_{scenario}"
                            
                            task_metrics[task]['relevance'].append(result['relevance_percentage'])
                            scenario_metrics[scenario]['relevance'].append(result['relevance_percentage'])
                            task_scenario_metrics[task_scenario_key]['relevance'].append(result['relevance_percentage'])
                        
                        processed_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Error getting result for {file_info['question_id']}: {str(e)}")
                    failed_count += 1
            
            for result in batch_results:
                if result['success']:
                    detailed_results.append(result)
        
        # Save intermediate results
        results['detailed_results'] = detailed_results
        results['summary']['processed_successfully'] = processed_count
        results['summary']['failed'] = failed_count
        results['summary']['total_tool_calls'] = total_tool_calls
        results['summary']['total_relevant_calls'] = total_relevant_calls
        results['summary']['overall_relevance_percentage'] = (
            (total_relevant_calls / total_tool_calls * 100) if total_tool_calls > 0 else 0
        )
        save_intermediate_results(results, output_folder, timestamp)
        
        print(f"Batch {batch_idx + 1} completed. Processed: {processed_count}, Failed: {failed_count}")
    
    # Calculate final metrics
    calculate_aggregated_tool_metrics(results, task_metrics, scenario_metrics, task_scenario_metrics)
    
    # Generate final results
    generate_final_tool_relevance_results(results, output_folder)
    
    # Cleanup
    cleanup_checkpoint_files(output_folder, timestamp)
    
    print(f"\n{'='*80}")
    print(f"PROCESSING COMPLETE")
    print(f"{'='*80}")
    print(f"Total conversations: {results['summary']['total_conversations']}")
    print(f"Successfully processed: {processed_count}")
    print(f"Failed: {failed_count}")
    if failed_count > 0:
        print(f"  → Check failed_tool_evaluations_{timestamp}.json for error details")
    print(f"Total tool calls evaluated: {total_tool_calls}")
    print(f"Relevant tool calls: {total_relevant_calls}")
    print(f"Overall relevance: {results['summary']['overall_relevance_percentage']:.2f}%")
    print(f"\nResults saved to: {output_folder}")
    print(f"{'='*80}")
    
    return results


def calculate_aggregated_tool_metrics(results, task_metrics, scenario_metrics, task_scenario_metrics):
    """Calculate aggregated tool relevance metrics."""
    
    for task, metrics in task_metrics.items():
        task_means = {}
        for metric_name, values in metrics.items():
            if values:
                task_means[metric_name] = {
                    'mean': mean(values),
                    'count': len(values),
                    'min': min(values),
                    'max': max(values)
                }
        results['task_metrics'][task] = task_means
    
    for scenario, metrics in scenario_metrics.items():
        scenario_means = {}
        for metric_name, values in metrics.items():
            if values:
                scenario_means[metric_name] = {
                    'mean': mean(values),
                    'count': len(values),
                    'min': min(values),
                    'max': max(values)
                }
        results['scenario_metrics'][scenario] = scenario_means
    
    for task_scenario, metrics in task_scenario_metrics.items():
        ts_means = {}
        for metric_name, values in metrics.items():
            if values:
                ts_means[metric_name] = {
                    'mean': mean(values),
                    'count': len(values),
                    'min': min(values),
                    'max': max(values)
                }
        results['task_scenario_metrics'][task_scenario] = ts_means


def generate_final_tool_relevance_results(results, output_folder):
    """Generate final results files."""
    
    results_file = os.path.join(output_folder, "tool_relevance_analysis.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    generate_tool_relevance_summary_report(results, output_folder)
    
    print(f"Final results saved:")
    print(f"  Detailed results: {results_file}")
    print(f"  Summary report: {os.path.join(output_folder, 'tool_relevance_summary.txt')}")


def generate_tool_relevance_summary_report(results, output_folder):
    """Generate human-readable summary report."""
    
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("TOOL CALL RELEVANCE ANALYSIS - WEB SEARCH AND CRAWL")
    report_lines.append("="*80)
    
    summary = results['summary']
    report_lines.append(f"\nSUMMARY:")
    report_lines.append(f"  Total conversations: {summary['total_conversations']}")
    report_lines.append(f"  Processed successfully: {summary['processed_successfully']}")
    report_lines.append(f"  Failed: {summary['failed']}")
    report_lines.append(f"  Total tool calls evaluated: {summary['total_tool_calls']}")
    report_lines.append(f"  Relevant tool calls: {summary['total_relevant_calls']}")
    report_lines.append(f"  Overall relevance: {summary['overall_relevance_percentage']:.2f}%")
    
    # Task-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-WISE TOOL RELEVANCE METRICS")
    report_lines.append("="*80)
    
    for task, metrics in results['task_metrics'].items():
        report_lines.append(f"\n{task}:")
        if 'relevance' in metrics:
            stats = metrics['relevance']
            report_lines.append(f"  Relevance: {stats['mean']:.2f}% (n={stats['count']}, range: {stats['min']:.1f}%-{stats['max']:.1f}%)")
    
    # Scenario-wise metrics
    report_lines.append(f"\n{'='*80}")
    report_lines.append("SCENARIO-WISE TOOL RELEVANCE METRICS")
    report_lines.append("="*80)
    
    for scenario, metrics in results['scenario_metrics'].items():
        report_lines.append(f"\n{scenario}:")
        if 'relevance' in metrics:
            stats = metrics['relevance']
            report_lines.append(f"  Relevance: {stats['mean']:.2f}% (n={stats['count']}, range: {stats['min']:.1f}%-{stats['max']:.1f}%)")
    
    # Task-Scenario combination
    report_lines.append(f"\n{'='*80}")
    report_lines.append("TASK-SCENARIO COMBINATION TOOL RELEVANCE METRICS")
    report_lines.append("="*80)
    
    for task_scenario, metrics in results['task_scenario_metrics'].items():
        report_lines.append(f"\n{task_scenario.replace('_', ' / ')}:")
        if 'relevance' in metrics:
            stats = metrics['relevance']
            report_lines.append(f"  Relevance: {stats['mean']:.2f}% (n={stats['count']}, range: {stats['min']:.1f}%-{stats['max']:.1f}%)")
    
    summary_file = os.path.join(output_folder, "tool_relevance_summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    for line in report_lines:
        print(line)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate Tool Call Relevance for Web Search and Crawl")
    parser.add_argument(
        "--input-dir",
        type=str,
        default=r"./final_testing_codes\task_scenario_new_final_1_responses",
        help="Base directory containing conversation_hierarchy.json files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=r"./final_evals\FINAL_OUTCOMES\WEB_TOOLS\tool_relevance_analysis_new_final_1",
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    responses_folder = args.input_dir
    output_folder = args.output_dir
    
    if not os.path.exists(responses_folder):
        print(f"Error: Responses folder does not exist: {responses_folder}")
        sys.exit(1)
    
    print(f"Processing conversations in: {responses_folder}")
    print(f"Saving results to: {output_folder}")
    
    process_tool_relevance_evaluation(responses_folder, output_folder)
