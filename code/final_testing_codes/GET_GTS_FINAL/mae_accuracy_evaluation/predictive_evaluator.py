"""Predictive question evaluator (MAE calculation)"""
from typing import Dict, List, Tuple
from .metric_matcher import find_matching_metric
from .normalizer import normalize_metric_name_v2


def calculate_mae_for_question(gt_data: dict, pred_data: dict) -> dict:
    """Calculate MAE for a predictive question.
    
    Algorithm:
    1. For each GT metric, find matching predicted metric
    2. Use max GT value as reference
    3. Calculate MAE against all GT values
    4. Select minimum MAE
    
    Args:
        gt_data: Ground truth data for question
        pred_data: Prediction data for question
        
    Returns:
        Dictionary with MAE results per metric
    """
    gt_metrics = gt_data.get('ground_truth_metrics_and_values_for_predictive', [])
    pred_metrics = pred_data.get('predicted_metrics_and_values_for_predictive', [])
    
    if not gt_metrics or not pred_metrics:
        return None
    
    # Group GT metrics by normalized name, keep original names
    gt_by_metric = {}
    for metric in gt_metrics:
        metric_name = metric.get('metric_name', '')
        value = metric.get('value_in_100_range')
        
        if metric_name and value is not None:
            normalized_name = normalize_metric_name_v2(metric_name)
            
            if normalized_name not in gt_by_metric:
                gt_by_metric[normalized_name] = {
                    'values': [],
                    'original_names': []
                }
            gt_by_metric[normalized_name]['values'].append(value)
            gt_by_metric[normalized_name]['original_names'].append(metric_name)
    
    # Build dict of predicted metrics with normalized names (store ALL values)
    pred_by_metric = {}
    for pred_metric in pred_metrics:
        metric_name = pred_metric.get('metric_name', '')
        value = pred_metric.get('value_in_100_range')
        
        if metric_name and value is not None:
            normalized_name = normalize_metric_name_v2(metric_name)
            
            if normalized_name not in pred_by_metric:
                pred_by_metric[normalized_name] = {
                    'values': [],
                    'original_names': []
                }
            pred_by_metric[normalized_name]['values'].append(value)
            pred_by_metric[normalized_name]['original_names'].append(metric_name)
    
    results = {}
    
    # For each GT metric, find match and calculate MAE
    for normalized_gt_name, gt_info in gt_by_metric.items():
        gt_values = gt_info['values']
        gt_original_names = gt_info['original_names']
        
        # Find matching predicted metric by normalized name
        if normalized_gt_name not in pred_by_metric:
            continue
        
        pred_info = pred_by_metric[normalized_gt_name]
        pred_values = pred_info['values']
        pred_original_names = pred_info['original_names']
        
        # Calculate MAE: compare ALL GT values × ALL Pred values
        # Find the pair (gt_val, pred_val) that gives minimum MAE
        min_mae = float('inf')
        best_gt_value = None
        best_pred_value = None
        all_mae_pairs = []
        
        for gt_val in gt_values:
            for pred_val in pred_values:
                mae = abs(pred_val - gt_val)
                all_mae_pairs.append({
                    'gt_value': gt_val,
                    'pred_value': pred_val,
                    'mae': mae
                })
                if mae < min_mae:
                    min_mae = mae
                    best_gt_value = gt_val
                    best_pred_value = pred_val
        
        results[normalized_gt_name] = {
            'normalized_metric_name': normalized_gt_name,
            'gt_original_names': gt_original_names,
            'pred_original_names': pred_original_names,
            'gt_values': gt_values,
            'pred_values': pred_values,
            'best_matching_gt_value': best_gt_value,
            'best_matching_pred_value': best_pred_value,
            'mae': min_mae,
            'all_mae_pairs': all_mae_pairs
        }
    
    return results if results else None


def evaluate_predictive_questions(ground_truths: dict, predictions: dict) -> list:
    """Evaluate all predictive questions.
    
    Args:
        ground_truths: Dictionary of ground truth data
        predictions: Dictionary of prediction data
        
    Returns:
        List of detailed results
    """
    results = []
    
    for unique_id, gt_data in ground_truths.items():
        if gt_data.get('predictive_or_qna') != 'predictive':
            continue
        
        # Skip if GT has no answer
        if not gt_data.get('is_answer_present'):
            continue
        
        if not gt_data.get('ground_truth_metrics_and_values_for_predictive'):
            continue
        
        # Find matching prediction
        pred_data = predictions.get(unique_id)
        if not pred_data:
            continue
        
        # Skip if prediction has no answer
        if not pred_data.get('is_answer_present'):
            continue
        
        # Calculate MAE
        mae_results = calculate_mae_for_question(gt_data, pred_data)
        
        if mae_results:
            result = {
                'unique_id': unique_id,
                'task_num': gt_data.get('task_num'),
                'scenario_num': gt_data.get('scenario_num'),
                'question': gt_data.get('complete_question', ''),
                'mae_by_metric': mae_results
            }
            results.append(result)
    
    return results
