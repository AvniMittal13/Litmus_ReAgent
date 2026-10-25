"""
Scenario 4: Different Language (Distant), Same Model
For gap languages where NO similar languages are available.
Must use distant (non-similar) languages for transfer.
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


def compute_scenario4_mapping(task_folder_path: str) -> Tuple[Optional[str], Optional[Dict[str, List[str]]]]:
    """
    Compute scenario 4 mapping: different language (distant), same model.
    
    Logic:
    1. Lgap = Lgt - Lav (languages in ground truth but not available)
    2. For each language in Lgap:
       - Check if ANY similar language is available → if yes, skip (that's scenario 3)
       - Find distant languages (all Lav languages minus similar ones)
       - Find common models between gap language (GT) and distant languages (available)
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
    
    # Step 2: For each gap language, check if NO similar languages are available
    scenario4_mapping = {}
    
    for gap_language in lgap_languages:
        # Get all similar/related languages
        similar_and_related = get_all_similar_and_related_languages(gap_language)
        
        # Check if ANY similar language is available
        available_similar = [lang for lang in similar_and_related if lang in reduced_mapping]
        
        # KEY CONSTRAINT: Skip if similar languages ARE available (that's scenario 3)
        if available_similar:
            continue
        
        # Find distant languages (all available minus similar)
        distant_langs = [lang for lang in lav_languages if lang not in similar_and_related]
        
        if not distant_langs:
            continue
        
        # Get models from gap language (GT)
        gap_models = set(combined_mapping[gap_language])
        
        # Get models from distant languages (available)
        distant_models = set()
        for dist_lang in distant_langs:
            distant_models.update(reduced_mapping[dist_lang])
        
        # Intersection: same models available via distant language
        common_models = gap_models & distant_models
        
        if common_models:
            scenario4_mapping[gap_language] = sorted(list(common_models))
            print(f"  {gap_language}: {len(common_models)} models via distant languages")
    
    print(f"Gap languages requiring distant transfer: {len(scenario4_mapping)}")
    
    return task_name, scenario4_mapping
