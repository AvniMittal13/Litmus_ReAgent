"""
Module to load questions from generated_questions folder and group them by task-scenario.
"""
import json
from pathlib import Path
from typing import Dict, List
from .config import GENERATED_QUESTIONS_DIR


def parse_filename(filename: str) -> tuple:
    """
    Parse task name and scenario number from filename.
    Format: {task}_questions_scenario{num}.json
    Example: 01_Code_Generation_questions_scenario1.json
    
    Returns:
        tuple: (task_name, scenario_number)
    """
    # Remove .json extension
    name = filename.replace('.json', '')
    
    # Split by underscore
    parts = name.split('_')
    
    # Find 'questions' keyword
    try:
        questions_idx = parts.index('questions')
    except ValueError:
        raise ValueError(f"Cannot parse filename: {filename} - 'questions' not found")
    
    # Task name is everything before 'questions'
    task_name = '_'.join(parts[:questions_idx])
    
    # After 'questions' should be 'scenarioX'
    if questions_idx + 1 >= len(parts):
        raise ValueError(f"Cannot parse filename: {filename} - scenario part missing")
    
    scenario_part = parts[questions_idx + 1]
    
    # Extract number from 'scenarioX'
    if not scenario_part.startswith('scenario'):
        raise ValueError(f"Cannot parse filename: {filename} - invalid scenario format")
    
    scenario_num = int(scenario_part.replace('scenario', ''))
    
    return task_name, scenario_num


def load_questions() -> Dict[str, List[Dict]]:
    """
    Load all question files from generated_questions folder.
    Group questions by task-scenario combination.
    
    Returns:
        Dict[str, List[Dict]]: {
            "task_scenario_X": [
                {
                    "unique_id": "...",
                    "query": "...",
                    "question_type": "..."
                },
                ...
            ]
        }
    """
    questions_dir = Path(GENERATED_QUESTIONS_DIR)
    
    if not questions_dir.exists():
        raise FileNotFoundError(f"Generated questions directory not found: {questions_dir}")
    
    # Group questions by task-scenario
    grouped_questions = {}
    
    # Iterate through all JSON files
    json_files = list(questions_dir.glob('*.json'))
    
    if not json_files:
        raise ValueError(f"No JSON files found in {questions_dir}")
    
    for json_file in json_files:
        try:
            # Parse task and scenario from filename
            task_name, scenario_num = parse_filename(json_file.name)
            
            # Create key for grouping
            key = f"{task_name}_scenario_{scenario_num}"
            
            # Load questions from file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract questions array from the data
            if isinstance(data, dict) and 'questions' in data:
                questions = data['questions']
            elif isinstance(data, list):
                questions = data
            else:
                raise ValueError(f"Unexpected JSON structure in {json_file.name}")
            
            # Store in grouped dict
            grouped_questions[key] = questions
            
        except Exception as e:
            print(f"Warning: Failed to process {json_file.name}: {e}")
            continue
    
    return grouped_questions


def get_task_scenario_questions(task_name: str, scenario_num: int) -> List[Dict]:
    """
    Get questions for a specific task-scenario combination.
    
    Args:
        task_name: Name of the task
        scenario_num: Scenario number (1-5)
    
    Returns:
        List[Dict]: List of questions with unique_id, query, question_type
    """
    all_questions = load_questions()
    key = f"{task_name}_scenario_{scenario_num}"
    
    if key not in all_questions:
        raise KeyError(f"No questions found for {key}")
    
    return all_questions[key]
