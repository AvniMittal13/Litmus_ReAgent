#!/usr/bin/env python3
"""
Interactive script to generate questions for a selected task across all scenarios.

This script allows you to:
1. Select a specific task from available tasks
2. Generate questions for that task across all 5 scenarios
3. Maintain the same saving conventions as the original scripts

Usage:
    python generate_questions_by_task.py
"""

import sys
import os
import json
import importlib.util
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response
from pydantic import BaseModel

class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str
        languages: str

    questions: list[Question]

# Configuration
BASE_DATA_PATH = r"./all_final_csvs_finall"
OUTPUT_DIR = "generated_questions"
SCENARIOS_DIR = os.path.dirname(os.path.abspath(__file__))

# Question counts per scenario (you can modify these)
QUESTION_COUNTS = {
    1: 10,  # Scenario 1: GT available
    2: 10,  # Scenario 2: Different model performance  
    3: 10,  # Scenario 3: Different language performance
    4: 10,  # Scenario 4: Cross-lingual with gap data
    5: 10,  # Scenario 5: Cross-lingual without gap data
}

# Scenario descriptions for user information
SCENARIO_DESCRIPTIONS = {
    1: "GT_available - Questions when ground truth data is available",
    2: "model_comparison - Questions comparing different model performances",
    3: "language_comparison - Questions comparing performance across languages", 
    4: "cross_lingual_gap - Questions about cross-lingual performance with gap data",
    5: "cross_lingual_no_gap - Questions about cross-lingual performance without gap data"
}

def get_available_tasks() -> List[str]:
    """Get list of available task folders."""
    if not os.path.exists(BASE_DATA_PATH):
        print(f"Error: Base data path not found: {BASE_DATA_PATH}")
        return []
    
    task_folders = [f for f in os.listdir(BASE_DATA_PATH) 
                   if os.path.isdir(os.path.join(BASE_DATA_PATH, f)) and f.startswith(('01_', '02_', '03_', '04_', '05_', '06_'))]
    return sorted(task_folders)

def display_task_menu(tasks: List[str]) -> None:
    """Display the task selection menu."""
    print("\n" + "="*60)
    print("AVAILABLE TASKS")
    print("="*60)
    for i, task in enumerate(tasks, 1):
        # Clean up task name for display
        clean_name = task.replace("_", " ")
        print(f"{i:2d}. {clean_name}")
    print(f"{len(tasks)+1:2d}. Exit")
    print("="*60)

def select_task(tasks: List[str]) -> Optional[str]:
    """Allow user to select a task interactively."""
    while True:
        display_task_menu(tasks)
        try:
            choice = input(f"\nSelect a task (1-{len(tasks)+1}): ").strip()
            
            if choice.lower() in ['exit', 'quit', 'q']:
                return None
                
            choice_num = int(choice)
            
            if choice_num == len(tasks) + 1:
                return None
            elif 1 <= choice_num <= len(tasks):
                selected_task = tasks[choice_num - 1]
                print(f"\nSelected: {selected_task}")
                return selected_task
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(tasks)+1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            return None

def load_task_mapping(task_folder_path: str) -> Tuple[Optional[str], Optional[Dict]]:
    """Load the language-models mapping from a task folder."""
    task_name = os.path.basename(task_folder_path).lower()
    mapping_file = os.path.join(task_folder_path, f"reduced_{task_name}_language_models_mapping.py")

    if not os.path.exists(mapping_file):
        print(f"Warning: Mapping file not found: {mapping_file}")
        return None, None
    
    try:
        # Load the mapping file as a module
        spec = importlib.util.spec_from_file_location("mapping_module", mapping_file)
        mapping_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mapping_module)
        
        # Extract the mapping and task name
        if hasattr(mapping_module, 'LANGUAGE_MODELS_MAPPING'):
            mapping = mapping_module.LANGUAGE_MODELS_MAPPING
            return task_name, mapping
        else:
            print(f"Warning: LANGUAGE_MODELS_MAPPING not found in {mapping_file}")
            return None, None
    except Exception as e:
        print(f"Error loading mapping file {mapping_file}: {e}")
        return None, None

def run_scenario_script(scenario_num: int, task_name: str) -> bool:
    """Run the specific scenario script for the given task."""
    script_path = os.path.join(SCENARIOS_DIR, f"generate_que_scenario{scenario_num}.py")
    
    if not os.path.exists(script_path):
        print(f"Warning: Scenario script not found: {script_path}")
        return False
    
    try:
        print(f"  Running scenario {scenario_num} script...")
        # Run the scenario script - it should process all tasks by default
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=SCENARIOS_DIR)
        
        if result.returncode == 0:
            print(f"  ✓ Scenario {scenario_num} completed successfully")
            return True
        else:
            print(f"  ✗ Scenario {scenario_num} failed:")
            print(f"    stdout: {result.stdout}")
            print(f"    stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error running scenario {scenario_num}: {e}")
        return False

def verify_generated_files(task_name: str) -> Dict[int, bool]:
    """Verify that question files were generated for each scenario."""
    results = {}
    
    for scenario_num in range(1, 6):
        filename = f"{task_name}_questions_scenario{scenario_num}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        results[scenario_num] = os.path.exists(filepath)
        
        if results[scenario_num]:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    question_count = len(data.get('questions', []))
                    print(f"  ✓ Scenario {scenario_num}: {filename} ({question_count} questions)")
            except Exception as e:
                print(f"  ⚠ Scenario {scenario_num}: {filename} (error reading: {e})")
                results[scenario_num] = False
        else:
            print(f"  ✗ Scenario {scenario_num}: {filename} (not found)")
    
    return results

def generate_questions_for_selected_task(task_name: str) -> bool:
    """Generate questions for the selected task across all scenarios."""
    print(f"\n" + "="*60)
    print(f"GENERATING QUESTIONS FOR: {task_name}")
    print("="*60)
    
    # Verify task exists and has mapping
    task_path = os.path.join(BASE_DATA_PATH, task_name)
    if not os.path.exists(task_path):
        print(f"Error: Task folder not found: {task_path}")
        return False
    
    task_name_clean, mapping = load_task_mapping(task_path)
    if not task_name_clean or not mapping:
        print(f"Error: Could not load mapping for task {task_name}")
        return False
    
    print(f"Task mapping loaded successfully.")
    print(f"Languages available: {len(mapping)}")
    total_models = sum(len(models) for models in mapping.values())
    print(f"Total model-language combinations: {total_models}")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Display scenarios that will be run
    print(f"\nScenarios to generate:")
    for scenario_num in range(1, 6):
        desc = SCENARIO_DESCRIPTIONS.get(scenario_num, f"Scenario {scenario_num}")
        questions_count = QUESTION_COUNTS.get(scenario_num, 10)
        print(f"  {scenario_num}. {desc} ({questions_count} questions)")
    
    # Ask for confirmation
    print(f"\nThis will generate questions for {task_name} across all 5 scenarios.")
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled.")
        return False
    
    # Run each scenario
    success_count = 0
    for scenario_num in range(1, 6):
        print(f"\n--- Scenario {scenario_num}: {SCENARIO_DESCRIPTIONS.get(scenario_num, '')} ---")
        if run_scenario_script(scenario_num, task_name):
            success_count += 1
        else:
            print(f"Failed to generate questions for scenario {scenario_num}")
    
    # Verify results
    print(f"\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    
    verification_results = verify_generated_files(task_name)
    successful_scenarios = sum(verification_results.values())
    
    print(f"\nSummary:")
    print(f"  Scenarios attempted: 5")
    print(f"  Scenarios successful: {successful_scenarios}")
    print(f"  Scripts executed successfully: {success_count}")
    
    if successful_scenarios == 5:
        print(f"  ✓ All question files generated successfully for {task_name}!")
        return True
    else:
        print(f"  ⚠ Some question files may be missing or incomplete.")
        return False

def main():
    """Main function to run the interactive task selection and question generation."""
    print("Question Generator for Selected Task")
    print("This script generates questions for a selected task across all scenarios.")
    
    # Get available tasks
    tasks = get_available_tasks()
    if not tasks:
        print("No tasks found. Please check the base data path.")
        return
    
    print(f"\nFound {len(tasks)} available tasks.")
    
    # Interactive task selection
    while True:
        selected_task = select_task(tasks)
        
        if selected_task is None:
            print("Goodbye!")
            break
        
        # Generate questions for selected task
        success = generate_questions_for_selected_task(selected_task)
        
        if success:
            print(f"\n✓ Question generation completed successfully for {selected_task}!")
        else:
            print(f"\n⚠ Question generation completed with some issues for {selected_task}.")
        
        # Ask if user wants to generate for another task
        print(f"\n" + "="*60)
        again = input("Generate questions for another task? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
