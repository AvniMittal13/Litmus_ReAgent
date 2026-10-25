"""
Scenario 3: Different Language (Similar), Same Model
For gap languages, find similar languages available in reduced mapping.
Use common models between gap language (GT) and similar languages (available).
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_utils import load_mapping_file, get_mapping_paths
from language_mapping import SIMILAR_LANGUAGES_MAPPING
from typing import Dict, List, Optional, Tuple, Set


def get_similar_languages(language: str) -> List[str]:
    """Get similar languages for a given language."""
    return SIMILAR_LANGUAGES_MAPPING.get(language, [])


def get_all_similar_and_related_languages(language: str) -> Set[str]:
    """Get all languages that are similar to or related to the given language."""
    similar_langs = set(get_similar_languages(language))
    
    # Also check if the language appears as a similar language for others
    for lang, similar_list in SIMILAR_LANGUAGES_MAPPING.items():
        if language in similar_list:
            similar_langs.add(lang)
            similar_langs.update(similar_list)
    
    # Remove the original language itself
    similar_langs.discard(language)
    return similar_langs


def compute_scenario3_mapping(task_folder_path: str) -> Tuple[Optional[str], Optional[Dict[str, List[str]]]]:
    """
    Compute scenario 3 mapping: different language (similar), same model.
    
    Logic:
    1. Lgap = Lgt - Lav (languages in ground truth but not available)
    2. For each language in Lgap:
       - Find similar languages that ARE available in Lav
       - Find common models between gap language (GT) and similar languages (available)
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
    
    print(f"Task: {task_name}")
    print(f"Ground truth languages (Lgt): {len(lgt_languages)}")
    print(f"Available languages (Lav): {len(lav_languages)}")
    print(f"Gap languages (Lgap): {len(lgap_languages)}")
    
    # Step 2: For each gap language, find similar language + same model combinations
    scenario3_mapping = {}
    
    for gap_language in lgap_languages:
        # Get similar languages for this gap language
        similar_languages = get_all_similar_and_related_languages(gap_language)
        
        # Find which similar languages are available in reduced mapping
        available_similar = [lang for lang in similar_languages if lang in reduced_mapping]
        
        if not available_similar:
            continue  # No similar language available - skip (this goes to scenario 4)
        
        # Get models from gap language (GT)
        gap_models = set(combined_mapping[gap_language])
        
        # Get models from similar languages (available)
        similar_models = set()
        for sim_lang in available_similar:
            similar_models.update(reduced_mapping[sim_lang])
        
        # Intersection: same models available via similar language
        common_models = gap_models & similar_models
        
        if common_models:
            scenario3_mapping[gap_language] = sorted(list(common_models))
            print(f"  {gap_language}: {len(common_models)} models via similar languages {available_similar[:3]}")
    
    print(f"Gap languages with similar language transfer: {len(scenario3_mapping)}")
    
    return task_name, scenario3_mapping
