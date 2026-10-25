"""
Scenario 1: Same Language, Same Model (GT Available)
Uses ONLY the reduced mapping - questions target language-model pairs where GT data IS available.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_utils import load_mapping_file, get_mapping_paths
from typing import Dict, List, Optional, Tuple


def compute_scenario1_mapping(task_folder_path: str) -> Tuple[Optional[str], Optional[Dict[str, List[str]]]]:
    """
    Compute scenario 1 mapping: same language, same model (GT available).
    
    Logic:
    - Uses ONLY the reduced mapping (Lav)
    - Questions target language-model pairs where ground truth data IS available
    """
    task_name, _, reduced_file = get_mapping_paths(task_folder_path)
    
    # Load reduced mapping only (available data)
    reduced_mapping = load_mapping_file(reduced_file)
    
    if not reduced_mapping:
        return None, None
    
    print(f"Task: {task_name}")
    print(f"Available languages (Lav): {len(reduced_mapping)}")
    total_pairs = sum(len(models) for models in reduced_mapping.values())
    print(f"Total language-model pairs: {total_pairs}")
    
    return task_name, reduced_mapping
