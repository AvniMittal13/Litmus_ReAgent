"""
Module to find judge_result.json files in evaluation results directories.
"""
import json
from pathlib import Path
from typing import Dict, Optional
from .config import EVALUATION_RESULTS_DIRECTORIES, REPORT_FILE_NAME, SCENARIO_TO_PAIR_MAPPING


def find_report_file(task: str, scenario_num: int, unique_id: str) -> Optional[Path]:
    """
    Find response.md file for a specific question.
    File structure: task/ScenarioPair_{pair_num}/{unique_id}/response.md
    
    Uses SCENARIO_TO_PAIR_MAPPING from config to determine which ScenarioPair folder
    contains the specified scenario number.
    
    Args:
        task: Task name (e.g., "01_Code_Generation")
        scenario_num: Scenario number (1-5)
        unique_id: Question unique ID
    
    Returns:
        Path to response.md file if found, None otherwise
    """
    # Map scenario number to ScenarioPair folder using config
    if scenario_num not in SCENARIO_TO_PAIR_MAPPING:
        raise ValueError(f"Invalid scenario number: {scenario_num}. Must be in {list(SCENARIO_TO_PAIR_MAPPING.keys())}.")
    
    scenario_pair = SCENARIO_TO_PAIR_MAPPING[scenario_num]
    scenario_folder = f"ScenarioPair_{scenario_pair}"
    
    # Search through all evaluation results directories
    for eval_dir in EVALUATION_RESULTS_DIRECTORIES:
        if not eval_dir.exists():
            continue
        
        # Check if task directory exists
        task_dir = eval_dir / task
        if not task_dir.exists():
            continue
        
        # Check if scenario folder exists
        scenario_dir = task_dir / scenario_folder
        if not scenario_dir.exists():
            continue
        
        # Check if unique_id subdirectory exists
        unique_id_dir = scenario_dir / unique_id
        if not unique_id_dir.exists():
            continue
        
        # Check if report file exists
        report_file = unique_id_dir / REPORT_FILE_NAME
        if report_file.exists():
            return report_file
    
    return None


def find_all_reports(task: str, scenario_num: int, questions: list) -> Dict[str, Optional[Path]]:
    """
    Find judge_result.json files for all questions in a task-scenario.
    
    Args:
        task: Task name (e.g., "01_Code_Generation")
        scenario_num: Scenario number (1-5)
        questions: List of question dicts with 'unique_id' field
    
    Returns:
        Dict mapping {unique_id: report_file_path} (path is None if not found)
    """
    report_files = {}
    
    for question in questions:
        unique_id = question.get('unique_id')
        if not unique_id:
            print(f"Warning: Question missing unique_id: {question}")
            continue
        
        report_file = find_report_file(task, scenario_num, unique_id)
        report_files[unique_id] = report_file
        
        if report_file is None:
            print(f"Warning: No report file found for query_id: {unique_id}")
    
    # Print summary
    found_count = sum(1 for path in report_files.values() if path is not None)
    total_count = len(report_files)
    print(f"Found reports for {found_count}/{total_count} questions")
    
    return report_files
