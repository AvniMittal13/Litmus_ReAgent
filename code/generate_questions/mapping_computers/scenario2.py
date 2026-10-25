"""
Scenario 2: Same Language, Different Model (GT NOT Available for specific models)
Computes difference between combined and reduced mappings.
For each language, finds models that exist in combined but NOT in reduced.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_utils import load_mapping_file, get_mapping_paths
from typing import Dict, List, Optional, Tuple


def compute_scenario2_mapping(task_folder_path: str) -> Tuple[Optional[str], Optional[Dict[str, List[str]]]]:
    """
    Compute scenario 2 mapping: same language, different model (GT NOT available).
    
    Logic:
    1. For each language in BOTH combined and reduced:
       - Find models in combined but NOT in reduced
       - These are the "missing model benchmarks"
    """
    task_name, combined_file, reduced_file = get_mapping_paths(task_folder_path)
    
    # Load both mappings
    combined_mapping = load_mapping_file(combined_file)  # Ground truth (Lgt)
    reduced_mapping = load_mapping_file(reduced_file)    # Available (Lav)
    
    if not combined_mapping or not reduced_mapping:
        return None, None
    
    # Compute difference: models in combined but not in reduced for each language
    difference_mapping = {}
    
    for language in combined_mapping:
        combined_models = set(combined_mapping[language])
        reduced_models = set(reduced_mapping.get(language, []))
        
        # Models that are in combined but not in reduced (missing evaluations)
        missing_models = combined_models - reduced_models
        
        if missing_models:
            difference_mapping[language] = sorted(list(missing_models))
    
    print(f"Task: {task_name}")
    print(f"Languages with missing models: {len(difference_mapping)}")
    total_missing = sum(len(models) for models in difference_mapping.values())
    print(f"Total missing model evaluations: {total_missing}")
    
    return task_name, difference_mapping
