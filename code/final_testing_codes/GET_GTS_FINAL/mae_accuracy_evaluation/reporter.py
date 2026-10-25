"""Report generator for evaluation results"""
import json
from pathlib import Path
from collections import defaultdict
from statistics import mean
from .config import TASK_NAMES, SCENARIO_NAMES


def calculate_mae_statistics(mae_results: list) -> dict:
    """Calculate MAE statistics.
    
    Args:
        mae_results: List of MAE evaluation results
        
    Returns:
        Dictionary with overall and per-metric MAE statistics
    """
    if not mae_results:
        return {
            'mean_mae': 0,
            'total_questions': 0,
            'total_metrics': 0,
            'per_metric': {}
        }
    
    # Collect all MAE values
    all_mae_values = []
    mae_by_metric = defaultdict(list)
    mae_by_task = defaultdict(list)
    mae_by_scenario = defaultdict(list)
    mae_by_task_scenario = defaultdict(list)
    
    for result in mae_results:
        task_num = result['task_num']
        scenario_num = result['scenario_num']
        task_scenario_key = f"{task_num}_scenario_{scenario_num}"
        
        for metric_name, metric_data in result['mae_by_metric'].items():
            mae_value = metric_data['mae']
            all_mae_values.append(mae_value)
            mae_by_metric[metric_name].append(mae_value)
            mae_by_task[task_num].append(mae_value)
            mae_by_scenario[scenario_num].append(mae_value)
            mae_by_task_scenario[task_scenario_key].append(mae_value)
    
    # Calculate per-metric statistics
    per_metric_stats = {}
    for metric_name, values in mae_by_metric.items():
        per_metric_stats[metric_name] = {
            'mean_mae': mean(values),
            'min_mae': min(values),
            'max_mae': max(values),
            'count': len(values)
        }
    
    # Calculate per-task statistics
    per_task_stats = {}
    for task_num, values in mae_by_task.items():
        task_name = TASK_NAMES.get(task_num, task_num)
        per_task_stats[task_name] = {
            'mean_mae': mean(values),
            'count_metrics': len(values),
            'count_questions': len([r for r in mae_results if r['task_num'] == task_num])
        }
    
    # Calculate per-scenario statistics
    per_scenario_stats = {}
    for scenario_num, values in mae_by_scenario.items():
        scenario_name = SCENARIO_NAMES.get(scenario_num, scenario_num)
        per_scenario_stats[scenario_name] = {
            'mean_mae': mean(values),
            'count_metrics': len(values),
            'count_questions': len([r for r in mae_results if r['scenario_num'] == scenario_num])
        }
    
    # Calculate per-task-scenario statistics
    per_task_scenario_stats = {}
    for key, values in mae_by_task_scenario.items():
        task_num, _, scenario_num = key.split('_')
        task_name = TASK_NAMES.get(task_num, task_num)
        scenario_name = SCENARIO_NAMES.get(scenario_num, scenario_num)
        display_key = f"{task_name}_{scenario_name}"
        
        per_task_scenario_stats[display_key] = {
            'mean_mae': mean(values),
            'count_metrics': len(values),
            'count_questions': len([r for r in mae_results if r['task_num'] == task_num and r['scenario_num'] == scenario_num])
        }
    
    return {
        'mean_mae': mean(all_mae_values) if all_mae_values else 0,
        'total_questions': len(mae_results),
        'total_metrics': len(all_mae_values),
        'per_metric': per_metric_stats,
        'per_task': per_task_stats,
        'per_scenario': per_scenario_stats,
        'per_task_scenario': per_task_scenario_stats
    }


def calculate_accuracy_statistics(qna_results: list) -> dict:
    """Calculate accuracy statistics.
    
    Args:
        qna_results: List of QnA evaluation results
        
    Returns:
        Dictionary with overall and per-category accuracy statistics
    """
    if not qna_results:
        return {
            'correct': 0,
            'total': 0,
            'percentage': 0.0,
            'per_task': {},
            'per_scenario': {},
            'per_task_scenario': {}
        }
    
    total = len(qna_results)
    correct = sum(1 for r in qna_results if r['is_correct'])
    
    # Per-task statistics
    task_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for result in qna_results:
        task_num = result['task_num']
        task_name = TASK_NAMES.get(task_num, task_num)
        task_stats[task_name]['total'] += 1
        if result['is_correct']:
            task_stats[task_name]['correct'] += 1
    
    per_task_stats = {}
    for task_name, stats in task_stats.items():
        per_task_stats[task_name] = {
            'correct': stats['correct'],
            'total': stats['total'],
            'percentage': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        }
    
    # Per-scenario statistics
    scenario_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for result in qna_results:
        scenario_num = result['scenario_num']
        scenario_name = SCENARIO_NAMES.get(scenario_num, scenario_num)
        scenario_stats[scenario_name]['total'] += 1
        if result['is_correct']:
            scenario_stats[scenario_name]['correct'] += 1
    
    per_scenario_stats = {}
    for scenario_name, stats in scenario_stats.items():
        per_scenario_stats[scenario_name] = {
            'correct': stats['correct'],
            'total': stats['total'],
            'percentage': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        }
    
    # Per-task-scenario statistics
    task_scenario_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for result in qna_results:
        task_num = result['task_num']
        scenario_num = result['scenario_num']
        task_name = TASK_NAMES.get(task_num, task_num)
        scenario_name = SCENARIO_NAMES.get(scenario_num, scenario_num)
        key = f"{task_name}_{scenario_name}"
        
        task_scenario_stats[key]['total'] += 1
        if result['is_correct']:
            task_scenario_stats[key]['correct'] += 1
    
    per_task_scenario_stats = {}
    for key, stats in task_scenario_stats.items():
        per_task_scenario_stats[key] = {
            'correct': stats['correct'],
            'total': stats['total'],
            'percentage': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        }
    
    return {
        'correct': correct,
        'total': total,
        'percentage': (correct / total * 100) if total > 0 else 0,
        'per_task': per_task_stats,
        'per_scenario': per_scenario_stats,
        'per_task_scenario': per_task_scenario_stats
    }


def generate_report(mae_results: list, qna_results: list, output_dir: Path):
    """Generate evaluation report.
    
    Args:
        mae_results: List of MAE results
        qna_results: List of QnA results
        output_dir: Output directory for reports
    """
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Calculate statistics
    mae_stats = calculate_mae_statistics(mae_results)
    accuracy_stats = calculate_accuracy_statistics(qna_results)
    
    # Prepare final report
    report = {
        'overall_metrics': {
            'mae': mae_stats,
            'accuracy': accuracy_stats
        },
        'detailed_mae_results': mae_results,
        'detailed_qna_results': qna_results
    }
    
    # Save full report as JSON
    with open(output_dir / 'evaluation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generate readable summary
    summary_lines = []
    summary_lines.append("=" * 80)
    summary_lines.append("MAE AND ACCURACY EVALUATION REPORT")
    summary_lines.append("=" * 80)
    summary_lines.append("")
    
    # MAE Summary
    summary_lines.append("📊 MAE (Mean Absolute Error) - Predictive Questions")
    summary_lines.append("-" * 80)
    
    if mae_stats.get('total_questions', 0) > 0:
        summary_lines.append(f"Overall Mean MAE: {mae_stats['mean_mae']:.2f}")
        summary_lines.append(f"Total Questions Evaluated: {mae_stats['total_questions']}")
        summary_lines.append(f"Total Metrics Compared: {mae_stats['total_metrics']}")
        summary_lines.append("")
        
        if 'per_task' in mae_stats:
            summary_lines.append("Per-Task MAE:")
            for task_name, stats in mae_stats['per_task'].items():
                summary_lines.append(f"  {task_name}:")
                summary_lines.append(f"    Mean MAE: {stats['mean_mae']:.2f}")
                summary_lines.append(f"    Questions: {stats['count_questions']}")
                summary_lines.append(f"    Metrics: {stats['count_metrics']}")
            summary_lines.append("")
        
        if 'per_scenario' in mae_stats:
            summary_lines.append("Per-Scenario MAE:")
            for scenario_name, stats in mae_stats['per_scenario'].items():
                summary_lines.append(f"  {scenario_name}:")
                summary_lines.append(f"    Mean MAE: {stats['mean_mae']:.2f}")
                summary_lines.append(f"    Questions: {stats['count_questions']}")
                summary_lines.append(f"    Metrics: {stats['count_metrics']}")
            summary_lines.append("")
    else:
        summary_lines.append("No predictive questions evaluated (no MAE data)")
        summary_lines.append("")
    
    summary_lines.append("Per-Task-Scenario MAE:")
    for key, stats in sorted(mae_stats['per_task_scenario'].items()):
        summary_lines.append(f"  {key}:")
        summary_lines.append(f"    Mean MAE: {stats['mean_mae']:.2f}")
        summary_lines.append(f"    Questions: {stats['count_questions']}")
        summary_lines.append(f"    Metrics: {stats['count_metrics']}")
    summary_lines.append("")
    
    summary_lines.append("Per-Metric MAE:")
    for metric_name, stats in mae_stats['per_metric'].items():
        summary_lines.append(f"  {metric_name}:")
        summary_lines.append(f"    Mean MAE: {stats['mean_mae']:.2f}")
        summary_lines.append(f"    Min MAE: {stats['min_mae']:.2f}")
        summary_lines.append(f"    Max MAE: {stats['max_mae']:.2f}")
        summary_lines.append(f"    Count: {stats['count']}")
    summary_lines.append("")
    
    # Accuracy Summary
    summary_lines.append("=" * 80)
    summary_lines.append("✓ ACCURACY - QnA Questions")
    summary_lines.append("-" * 80)
    summary_lines.append(f"Overall Accuracy: {accuracy_stats['percentage']:.2f}%")
    summary_lines.append(f"Correct: {accuracy_stats['correct']}/{accuracy_stats['total']}")
    summary_lines.append("")
    
    summary_lines.append("Per-Task Accuracy:")
    for task_name, stats in accuracy_stats['per_task'].items():
        summary_lines.append(f"  {task_name}:")
        summary_lines.append(f"    Accuracy: {stats['percentage']:.2f}%")
        summary_lines.append(f"    Correct: {stats['correct']}/{stats['total']}")
    summary_lines.append("")
    
    summary_lines.append("Per-Scenario Accuracy:")
    for scenario_name, stats in accuracy_stats['per_scenario'].items():
        summary_lines.append(f"  {scenario_name}:")
        summary_lines.append(f"    Accuracy: {stats['percentage']:.2f}%")
        summary_lines.append(f"    Correct: {stats['correct']}/{stats['total']}")
    summary_lines.append("")
    
    summary_lines.append("Per-Task-Scenario Accuracy:")
    for key, stats in sorted(accuracy_stats['per_task_scenario'].items()):
        summary_lines.append(f"  {key}:")
        summary_lines.append(f"    Accuracy: {stats['percentage']:.2f}%")
        summary_lines.append(f"    Correct: {stats['correct']}/{stats['total']}")
    summary_lines.append("")
    
    summary_lines.append("=" * 80)
    
    # Save summary
    with open(output_dir / 'evaluation_summary.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))
    
    # Print summary
    print('\n'.join(summary_lines))
    
    print(f"\n✅ Reports saved to: {output_dir.absolute()}")
    print(f"   - evaluation_report.json (full report)")
    print(f"   - evaluation_summary.txt (readable summary)")
