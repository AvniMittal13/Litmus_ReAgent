#!/usr/bin/env python3
"""
Unified Question Generation Script

Generates questions for all tasks across all scenarios with configurable options.

Usage:
    python run_all.py                           # Run all scenarios, all tasks
    python run_all.py --scenario 1              # Run only scenario 1
    python run_all.py --scenario 1,3,5          # Run scenarios 1, 3, and 5
    python run_all.py --task "01_Code_Generation"  # Run specific task
    python run_all.py --use-scenario-prompts    # Use scenario-specific prompts instead of common
    python run_all.py --questions 30            # Generate 30 questions per scenario
    python run_all.py --dry-run                 # Show what would be generated without running
"""

import os
import sys
import argparse
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mapping_computers import (
    compute_scenario1_mapping,
    compute_scenario2_mapping,
    compute_scenario3_mapping,
    compute_scenario4_mapping,
    compute_scenario5_mapping,
)
from prompts import get_prompt, get_scenario_name, SCENARIO_NAMES
from generator import generate_questions, generate_questions_validated, save_questions
from gen_utils import get_task_folders


# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Configuration for question generation."""
    
    # Base path for task data
    BASE_DATA_PATH = r"./all_final_csvs_finall"
    
    # Output directory
    OUTPUT_DIR = "generated_questions"
    
    # Default number of questions per scenario
    DEFAULT_QUESTIONS = 50
    
    # Question distribution for common prompt
    PREDICTIVE_RATIO = 0.5  # 50% predictive, 50% QnA
    
    # Available scenarios
    ALL_SCENARIOS = [1, 2, 3, 4, 5]
    
    # Scenario descriptions
    SCENARIO_DESCRIPTIONS = {
        1: "Same Language, Same Model (GT Available)",
        2: "Same Language, Different Model (GT NOT Available)",
        3: "Different Language (Similar), Same Model",
        4: "Different Language (Distant), Same Model",
        5: "Different Language, Different Model (Both NOT in Lav)",
    }


# Mapping computers registry
MAPPING_COMPUTERS = {
    1: compute_scenario1_mapping,
    2: compute_scenario2_mapping,
    3: compute_scenario3_mapping,
    4: compute_scenario4_mapping,
    5: compute_scenario5_mapping,
}


# =============================================================================
# MAIN GENERATION LOGIC
# =============================================================================

def generate_for_task_scenario(
    task_folder_path: str,
    scenario: int,
    use_common_prompt: bool = True,
    num_predictive: int = 30,
    num_qna: int = 30,
    output_dir: str = "generated_questions"
) -> Optional[int]:
    """
    Generate questions for a specific task and scenario.
    
    Args:
        task_folder_path: Full path to the task folder
        scenario: Scenario number (1-5)
        use_common_prompt: Whether to use common prompt or scenario-specific
        num_predictive: Number of predictive questions
        num_qna: Number of QnA questions
        output_dir: Output directory path
    
    Returns:
        Number of questions generated, or None if failed
    """
    task_name = os.path.basename(task_folder_path)
    num_questions = num_predictive + num_qna
    
    print(f"\n{'='*60}")
    print(f"Task: {task_name} | Scenario {scenario}: {Config.SCENARIO_DESCRIPTIONS[scenario]}")
    print('='*60)
    
    # Get the appropriate mapping computer
    compute_mapping = MAPPING_COMPUTERS.get(scenario)
    if not compute_mapping:
        print(f"Unknown scenario: {scenario}")
        return None
    
    # Compute the mapping for this scenario
    _, mapping = compute_mapping(task_folder_path)
    
    if not mapping:
        print(f"No data available for scenario {scenario}")
        return None
    
    # Get the prompt
    prompt = get_prompt(scenario, use_common_prompt)
    
    prompt_type = "common" if use_common_prompt else "scenario-specific"
    print(f"Using {prompt_type} prompt")
    print(f"Generating {num_questions} questions ({num_predictive} predictive, {num_qna} QnA)")
    
    # Generate questions with validation (filters out hallucinated languages/models)
    questions = generate_questions_validated(
        task_name=task_name,
        mapping=mapping,
        prompt_template=prompt,
        num_questions=num_questions,
        num_predictive=num_predictive,
        num_qna=num_qna,
        max_retries=3
    )
    
    if not questions:
        print(f"Failed to generate questions")
        return None
    
    # Save questions
    scenario_name = get_scenario_name(scenario)
    save_questions(questions, task_name, scenario, scenario_name, output_dir)
    
    return len(questions.questions)


def run_generation(
    scenarios: List[int] = None,
    tasks: List[str] = None,
    use_common_prompt: bool = True,
    num_predictive: int = 30,
    num_qna: int = 30,
    output_dir: str = None,
    dry_run: bool = False
):
    """
    Run question generation for specified scenarios and tasks.
    
    Args:
        scenarios: List of scenario numbers (default: all)
        tasks: List of task names (default: all)
        use_common_prompt: Whether to use common prompt
        num_predictive: Number of predictive questions
        num_qna: Number of QnA questions
        output_dir: Output directory (default: generated_questions)
        dry_run: If True, just show what would be generated
    """
    # Defaults
    scenarios = scenarios or Config.ALL_SCENARIOS
    output_dir = output_dir or Config.OUTPUT_DIR
    num_questions = num_predictive + num_qna
    
    # Get all task folders
    all_tasks = get_task_folders(Config.BASE_DATA_PATH)
    
    if not all_tasks:
        print(f"No tasks found in {Config.BASE_DATA_PATH}")
        return
    
    # Filter tasks if specified
    if tasks:
        all_tasks = [t for t in all_tasks if t in tasks or any(task in t for task in tasks)]
    
    print("\n" + "="*70)
    print("QUESTION GENERATION CONFIGURATION")
    print("="*70)
    print(f"Base path: {Config.BASE_DATA_PATH}")
    print(f"Output directory: {output_dir}")
    print(f"Prompt type: {'Common' if use_common_prompt else 'Scenario-specific'}")
    print(f"Questions per scenario: {num_questions}")
    print(f"Tasks: {len(all_tasks)}")
    for t in all_tasks:
        print(f"  - {t}")
    print(f"Scenarios: {scenarios}")
    for s in scenarios:
        print(f"  - {s}: {Config.SCENARIO_DESCRIPTIONS[s]}")
    print("="*70)
    
    if dry_run:
        print("\n[DRY RUN] Would generate questions for:")
        for task in all_tasks:
            for scenario in scenarios:
                print(f"  - {task} / Scenario {scenario}")
        print(f"\nTotal: {len(all_tasks) * len(scenarios)} task-scenario combinations")
        return
    
    # Track results
    results = {}
    start_time = datetime.now()
    
    # Generate for each task and scenario
    for task in all_tasks:
        task_path = os.path.join(Config.BASE_DATA_PATH, task)
        results[task] = {}
        
        for scenario in scenarios:
            count = generate_for_task_scenario(
                task_folder_path=task_path,
                scenario=scenario,
                use_common_prompt=use_common_prompt,
                num_predictive=num_predictive,
                num_qna=num_qna,
                output_dir=output_dir
            )
            results[task][scenario] = count or 0
    
    # Print summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*70)
    print("GENERATION SUMMARY")
    print("="*70)
    print(f"Duration: {duration:.1f} seconds")
    print(f"Output directory: {output_dir}")
    print()
    
    total_questions = 0
    for task, scenario_results in results.items():
        task_total = sum(scenario_results.values())
        total_questions += task_total
        print(f"{task}:")
        for scenario, count in scenario_results.items():
            status = "✓" if count > 0 else "✗"
            print(f"  {status} Scenario {scenario}: {count} questions")
    
    print()
    print(f"Total questions generated: {total_questions}")
    print("="*70)


# =============================================================================
# CLI
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate benchmark questions for all tasks and scenarios.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all.py                           # Run all scenarios, all tasks
  python run_all.py --scenario 1              # Run only scenario 1
  python run_all.py --scenario 1,3,5          # Run scenarios 1, 3, and 5
  python run_all.py --task 01_Code_Generation # Run specific task
  python run_all.py --use-scenario-prompts    # Use scenario-specific prompts
  python run_all.py --questions 30            # Generate 30 questions per scenario
  python run_all.py --output my_questions     # Custom output directory
  python run_all.py --dry-run                 # Preview without generating
        """
    )
    
    parser.add_argument(
        '--scenario', '-s',
        type=str,
        default=None,
        help='Scenario(s) to run. Comma-separated for multiple (e.g., "1,3,5")'
    )
    
    parser.add_argument(
        '--task', '-t',
        type=str,
        default=None,
        help='Task name(s) to process. Comma-separated for multiple.'
    )
    
    parser.add_argument(
        '--use-scenario-prompts',
        action='store_true',
        help='Use scenario-specific prompts instead of common prompt'
    )
    
    parser.add_argument(
        '--questions', '-q',
        type=int,
        default=None,
        help='Total number of questions per scenario (default: 60). Overrides --predictive and --qna.'
    )
    
    parser.add_argument(
        '--predictive',
        type=int,
        default=30,
        help='Number of predictive questions (default: 30)'
    )
    
    parser.add_argument(
        '--qna',
        type=int,
        default=30,
        help='Number of QnA questions (default: 30)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output directory for generated questions'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without actually running'
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Parse scenarios
    scenarios = None
    if args.scenario:
        scenarios = [int(s.strip()) for s in args.scenario.split(',')]
    
    # Parse tasks
    tasks = None
    if args.task:
        tasks = [t.strip() for t in args.task.split(',')]
    
    # Handle question counts
    if args.questions is not None:
        num_predictive = args.questions // 2
        num_qna = args.questions - num_predictive
    else:
        num_predictive = args.predictive
        num_qna = args.qna
    
    # Run generation
    run_generation(
        scenarios=scenarios,
        tasks=tasks,
        use_common_prompt=not args.use_scenario_prompts,
        num_predictive=num_predictive,
        num_qna=num_qna,
        output_dir=args.output,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
