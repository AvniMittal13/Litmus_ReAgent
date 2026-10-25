"""
Scenario 5: Different Language, Different Model (Both NOT in Lav)
Languages from Lgap with models that are NOT available in Lav for ANY language.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_utils import load_mapping_file, get_mapping_paths
from typing import Dict, List, Optional, Tuple


def compute_scenario5_mapping(task_folder_path: str) -> Tuple[Optional[str], Optional[Dict[str, List[str]]]]:
    """
    Compute scenario 5 mapping: different language AND different model (both unavailable).
    
    CORRECTED Logic:
    1. Lgap = Lgt - Lav (languages in ground truth but not available)
    2. Get ALL models available in Lav (across ALL languages)
    3. For each language in Lgap:
       - Get models for that language from Lgt (ground truth)
       - EXCLUDE models that are available in Lav (for ANY language)
       - The remaining models are truly "different" - not available in Lav at all
    
    This ensures both the language AND the model are NOT in Lav.
    """
    task_name, combined_file, reduced_file = get_mapping_paths(task_folder_path)
    
    # Load both mappings
    combined_mapping = load_mapping_file(combined_file)  # Ground truth (Lgt)
    reduced_mapping = load_mapping_file(reduced_file)    # Available (Lav)
    
    if not combined_mapping or not reduced_mapping:
        return None, None
    
    # Step 1: Compute Lgap = Lgt - Lav
    lgt_languages = set(combined_mapping.keys())
    lav_languages = set(reduced_mapping.keys())
    lgap_languages = lgt_languages - lav_languages
    
    # Step 2: Get ALL models available in Lav (across ALL languages)
    all_lav_models = set()
    for lang in lav_languages:
        all_lav_models.update(reduced_mapping[lang])
    
    print(f"Task: {task_name}")
    print(f"Ground truth languages (Lgt): {len(lgt_languages)}")
    print(f"Available languages (Lav): {len(lav_languages)}")
    print(f"Gap languages (Lgap): {len(lgap_languages)}")
    print(f"All models in Lav (across all languages): {len(all_lav_models)}")
    
    # Step 3: For each language in Lgap, find models that are NOT in Lav (for any language)
    scenario5_mapping = {}
    
    for gap_language in lgap_languages:
        # Get models that exist for this gap language in ground truth
        gap_language_models = set(combined_mapping[gap_language])
        
        # CRITICAL: Find models that are in Lgt for this language but NOT in Lav at all
        # This ensures BOTH language AND model are unavailable in Lav
        different_models = gap_language_models - all_lav_models
        
        if different_models:
            scenario5_mapping[gap_language] = sorted(list(different_models))
            print(f"  {gap_language}: {len(different_models)} models (both lang and model not in Lav)")
    
    print(f"Gap languages with different models: {len(scenario5_mapping)}")
    
    return task_name, scenario5_mapping
