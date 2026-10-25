"""
Module to load failed questions from Ground_truths_1 (is_answer_present=false).
"""
import json
from pathlib import Path
from typing import Dict, List
from .config import EXISTING_OUTPUT_DIR


def load_failed_questions() -> Dict[str, List[Dict]]:
    """
    Load questions from Ground_truths_1 where is_answer_present=false.
    
    Returns:
        Dict of {task_scenario_key: [question_dicts]}
        Same format as query_loader.load_questions() for compatibility
    """
    output_dir = Path(EXISTING_OUTPUT_DIR)
    
    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}")
        return {}
    
    all_failed = {}
    total_failed = 0
    
    for json_file in output_dir.glob("*_ground_truths.json"):
        # Extract task_scenario key from filename
        # e.g., "01_Code_Generation_scenario_1_ground_truths.json" -> "01_Code_Generation_scenario_1"
        key = json_file.stem.replace("_ground_truths", "")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Filter questions where is_answer_present=false
            failed = [
                q for q in data 
                if not q.get('is_answer_present', False)
            ]
            
            if failed:
                all_failed[key] = failed
                total_failed += len(failed)
                print(f"  {key}: {len(failed)} failed questions")
        
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    print(f"\nTotal failed questions to reprocess: {total_failed}")
    return all_failed


def get_task_from_key(key: str) -> str:
    """
    Extract task name from task_scenario key.
    e.g., "01_Code_Generation_scenario_1" -> "01_Code_Generation"
    """
    parts = key.rsplit("_scenario_", 1)
    return parts[0] if parts else key
