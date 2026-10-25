"""
Main orchestration script for prediction generation from evaluation reports.
"""
import json
import argparse
from pathlib import Path
from .config import OUTPUT_DIR, TASKS, NUM_SCENARIOS
from .query_loader import load_questions
from .report_finder import find_all_reports
from .report_extractor import extract_all_reports
from .prediction_generator import generate_predictions_for_questions


def process_task_scenario(task_name: str, scenario_num: int, all_questions: dict) -> bool:
    """
    Process a single task-scenario combination and generate predictions JSON.
    Skips questions that already have predictions in the output file.
    
    Args:
        task_name: Name of the task
        scenario_num: Scenario number
        all_questions: Pre-loaded questions dict
    
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Processing: {task_name} - Scenario {scenario_num}")
    print(f"{'='*60}")
    
    # Get questions for this task-scenario
    key = f"{task_name}_scenario_{scenario_num}"
    
    if key not in all_questions:
        print(f"Error: No questions found for {key}")
        return False
    
    questions = all_questions[key]
    print(f"Found {len(questions)} questions")
    
    # Load existing predictions to skip already-done questions
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{key}_predictions.json"
    
    existing_predictions = {}  # uid -> prediction dict
    if output_file.exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_list = json.load(f)
            for item in existing_list:
                uid = item.get('unique_id', '')
                has_pred = bool(item.get('predicted_metrics_and_values_for_predictive'))
                has_ans = bool(item.get('answer_text_for_qna'))
                if has_pred or has_ans:
                    existing_predictions[uid] = item
            print(f"Found {len(existing_predictions)} existing predictions (with data)")
        except Exception as e:
            print(f"Warning: Could not load existing predictions: {e}")
    
    # Split questions into already-done and needs-processing
    questions_to_process = []
    for q in questions:
        uid = q.get('unique_id', '')
        if uid not in existing_predictions:
            questions_to_process.append(q)
    
    print(f"Questions needing predictions: {len(questions_to_process)} (skipping {len(questions) - len(questions_to_process)} already done)")
    
    if not questions_to_process:
        print("All questions already have predictions, skipping.")
        return True
    
    # Step 1: Find response.md files (only for questions needing processing)
    print("\nStep 1: Finding response.md files...")
    report_files = find_all_reports(task_name, scenario_num, questions_to_process)
    
    # Step 2: Extract report text
    print("\nStep 2: Extracting report text from response.md files...")
    reports = extract_all_reports(report_files)
    
    # Step 3: Generate predictions using LLM (only for new questions)
    print("\nStep 3: Generating predictions from agent reports...")
    new_predictions = generate_predictions_for_questions(questions_to_process, reports)
    
    # Merge: build new_predictions lookup
    new_pred_map = {p['unique_id']: p for p in new_predictions}
    
    # Build final list preserving original question order
    final_predictions = []
    for q in questions:
        uid = q.get('unique_id', '')
        if uid in existing_predictions:
            final_predictions.append(existing_predictions[uid])
        elif uid in new_pred_map:
            final_predictions.append(new_pred_map[uid])
        else:
            # Shouldn't happen, but handle gracefully
            final_predictions.append({
                "unique_id": uid,
                "complete_question": q.get('complete_question', ''),
                "atleast_one_successful_execution": False,
                "is_answer_present": False,
                "predictive_or_qna": q.get('question_type', 'qna').lower(),
                "predicted_metrics_and_values_for_predictive": [],
                "answer_text_for_qna": ""
            })
    
    # Step 4: Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_predictions, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved: {output_file} ({len(new_predictions)} new + {len(existing_predictions)} existing)")
    print(f"{'='*60}\n")
    
    return True


def main():
    """
    Main function to orchestrate prediction generation.
    """
    parser = argparse.ArgumentParser(description='Generate predictions from evaluation reports for all task-scenario combinations')
    parser.add_argument('--task', type=str, help='Process only a specific task (optional)')
    parser.add_argument('--scenario', type=int, help='Process only a specific scenario (1-5, optional)')
    
    args = parser.parse_args()
    
    # Load all questions once
    print("Loading all questions...")
    all_questions = load_questions()
    print(f"Loaded {len(all_questions)} task-scenario combinations\n")
    
    # Determine which tasks to process
    tasks_to_process = [args.task] if args.task else TASKS
    
    # Determine which scenarios to process
    scenarios_to_process = [args.scenario] if args.scenario else range(1, NUM_SCENARIOS + 1)
    
    # Process each task-scenario combination
    success_count = 0
    failure_count = 0
    
    for task in tasks_to_process:
        for scenario in scenarios_to_process:
            success = process_task_scenario(task, scenario, all_questions)
            
            if success:
                success_count += 1
            else:
                failure_count += 1
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Total: {success_count + failure_count}")
    print("="*60)


if __name__ == "__main__":
    main()
