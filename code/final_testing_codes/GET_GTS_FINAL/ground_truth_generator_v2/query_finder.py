"""
Module to find query_id folders across response directories.
"""
from pathlib import Path
from typing import List, Optional
from .config import RESPONSE_DIRECTORIES


def find_query_id_folder(query_id: str, task_name: str, scenario_num: int) -> Optional[Path]:
    """
    Search for a query_id folder across all response directories.
    The structure is: response_dir / task_name / ScenarioPair_X / query_id
    
    Args:
        query_id: The unique_id to search for
        task_name: Name of the task (e.g., "01_Code_Generation")
        scenario_num: Scenario number (1-5)
    
    Returns:
        Path object if found, None if not found in any directory
    """
    # Map scenario number to ScenarioPair folder
    scenario_folder = f"ScenarioPair_{scenario_num}"
    
    for response_dir in RESPONSE_DIRECTORIES:
        response_path = Path(response_dir)
        
        if not response_path.exists():
            print(f"Warning: Response directory does not exist: {response_dir}")
            continue
        
        # Build path: response_dir / task_name / ScenarioPair_X / query_id
        query_folder = response_path / task_name / scenario_folder / query_id
        
        if query_folder.exists() and query_folder.is_dir():
            return query_folder
    
    return None


def find_all_query_folders(query_ids: List[str], task_name: str, scenario_num: int) -> dict:
    """
    Find folders for multiple query_ids.
    
    Args:
        query_ids: List of unique_ids to search for
        task_name: Name of the task
        scenario_num: Scenario number
    
    Returns:
        dict: {
            query_id: Path or None
        }
    """
    results = {}
    
    for query_id in query_ids:
        folder = find_query_id_folder(query_id, task_name, scenario_num)
        results[query_id] = folder
        
        if folder is None:
            print(f"Warning: No folder found for query_id: {query_id}")
    
    return results
