"""
Shared utility functions for question generation.
"""
import os
import importlib.util
from typing import Dict, List, Optional, Tuple


def load_mapping_file(file_path: str) -> Optional[Dict[str, List[str]]]:
    """Load a mapping file and return the LANGUAGE_MODELS_MAPPING."""
    if not os.path.exists(file_path):
        print(f"Warning: Mapping file not found: {file_path}")
        return None
    
    # Load the mapping file as a module
    spec = importlib.util.spec_from_file_location("mapping_module", file_path)
    mapping_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mapping_module)
    
    # Extract the mapping
    if hasattr(mapping_module, 'LANGUAGE_MODELS_MAPPING'):
        return mapping_module.LANGUAGE_MODELS_MAPPING
    else:
        print(f"Warning: LANGUAGE_MODELS_MAPPING not found in {file_path}")
        return None


def get_mapping_paths(task_folder_path: str) -> Tuple[str, str, str]:
    """Get paths for combined and reduced mapping files."""
    task_name = os.path.basename(task_folder_path).lower()
    combined_file = os.path.join(task_folder_path, f"{task_name}_language_models_mapping.py")
    reduced_file = os.path.join(task_folder_path, f"reduced_{task_name}_language_models_mapping.py")
    return task_name, combined_file, reduced_file


def format_mapping_for_prompt(mapping: Dict[str, List[str]]) -> str:
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in sorted(mapping.items()):
        models_str = ", ".join(models)
        formatted_lines.append(f"  {lang}: [{models_str}]")
    return "\n".join(formatted_lines)


def clean_task_name(task_name: str) -> str:
    """Clean up task name for better readability in prompts."""
    clean_name = task_name.replace("_", " ")
    # Remove leading numbers like "01 ", "02 ", etc.
    for i in range(10):
        clean_name = clean_name.replace(f"0{i} ", "")
    return clean_name.strip()


def get_task_folders(base_path: str) -> List[str]:
    """Get all task folders from the base path."""
    if not os.path.exists(base_path):
        print(f"Base path not found: {base_path}")
        return []
    
    # Folders to exclude
    exclude_folders = {'__pycache__', 'statistics_output', '.git', 'node_modules'}
    
    task_folders = [
        f for f in os.listdir(base_path) 
        if os.path.isdir(os.path.join(base_path, f)) and f not in exclude_folders
    ]
    return sorted(task_folders)
