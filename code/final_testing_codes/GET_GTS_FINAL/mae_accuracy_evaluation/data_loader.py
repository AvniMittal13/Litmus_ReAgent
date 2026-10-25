"""Data loader for ground truths and predictions"""
import json
from pathlib import Path
from typing import Dict


def load_ground_truths(gt_dir: Path) -> Dict[str, dict]:
    """Load all ground truth files.
    
    Args:
        gt_dir: Ground truth directory path
        
    Returns:
        Dictionary mapping unique_id to ground truth data
    """
    ground_truths = {}
    
    for gt_file in gt_dir.glob("*.json"):
        try:
            with open(gt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract task and scenario from filename
            # Format: 01_Code_Generation_scenario_1_ground_truths.json
            filename = gt_file.stem
            parts = filename.split('_')
            task_num = parts[0]
            scenario_num = filename.split('_scenario_')[1].split('_')[0]
            
            for item in data:
                unique_id = item.get('unique_id')
                if unique_id:
                    item['task_num'] = task_num
                    item['scenario_num'] = scenario_num
                    ground_truths[unique_id] = item
                    
        except Exception as e:
            print(f"Error loading {gt_file}: {e}")
    
    return ground_truths


def load_predictions(pred_dir: Path) -> Dict[str, dict]:
    """Load all prediction files.
    
    Args:
        pred_dir: Predictions directory path
        
    Returns:
        Dictionary mapping unique_id to prediction data
    """
    predictions = {}
    
    for pred_file in pred_dir.glob("*.json"):
        try:
            with open(pred_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract task and scenario from filename
            filename = pred_file.stem
            parts = filename.split('_')
            task_num = parts[0]
            scenario_num = filename.split('_scenario_')[1].split('_')[0]
            
            for item in data:
                unique_id = item.get('unique_id')
                if unique_id:
                    item['task_num'] = task_num
                    item['scenario_num'] = scenario_num
                    predictions[unique_id] = item
                    
        except Exception as e:
            print(f"Error loading {pred_file}: {e}")
    
    return predictions
