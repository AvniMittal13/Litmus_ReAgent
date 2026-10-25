"""
Direct ground truth generation - generates web search queries using GPT only.
Does NOT use response directories or intermediates files.
"""
import json
import argparse
from pathlib import Path
from .config import OUTPUT_DIR, TASKS, NUM_SCENARIOS
from .query_loader import load_questions
from .cache_retriever import get_all_responses_with_active_search
from .ground_truth_generator import generate_ground_truths_for_questions
from .query_generator import generate_queries_for_questions


def process_task_scenario(task_name: str, scenario_num: int, all_questions: dict) -> bool:
    """
    Process a single task-scenario combination and generate ground truth JSON.
    Uses GPT to generate web search queries directly (no response directories).
    Skips questions that are already completed in the output file.
    
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
    
    # Check for existing output file and load completed questions
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{key}_ground_truths.json"
    
    existing_ground_truths = []
    completed_ids = set()  # IDs with successful answers (is_answer_present: True)
    failed_ids = set()     # IDs that were processed but have no answer
    
    if output_file.exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            # Handle both list and dict formats
            if isinstance(existing_data, list):
                for gt in existing_data:
                    uid = gt.get('unique_id')
                    if uid:
                        # Only consider "completed" if answer was actually found
                        if gt.get('is_answer_present', False):
                            completed_ids.add(uid)
                            existing_ground_truths.append(gt)  # Only keep successful ones
                        else:
                            failed_ids.add(uid)
            elif isinstance(existing_data, dict):
                for uid, gt in existing_data.items():
                    if gt.get('is_answer_present', False):
                        completed_ids.add(uid)
                    else:
                        failed_ids.add(uid)
                existing_ground_truths = [gt for gt in existing_data.values() if gt.get('is_answer_present', False)]
            print(f"Found {len(completed_ids)} with answers, {len(failed_ids)} without answers (will retry)")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load existing file: {e}")
            existing_ground_truths = []
            completed_ids = set()
    
    # Filter out only questions that have successful answers
    pending_questions = [q for q in questions if q.get('unique_id') not in completed_ids]
    
    if not pending_questions:
        print("All questions already have answers! Skipping...")
        return True
    
    print(f"Processing {len(pending_questions)} pending questions ({len(failed_ids)} retries, skipping {len(completed_ids)} with answers)")
    
    # Extract unique_ids for pending questions only
    query_ids = [q.get('unique_id') for q in pending_questions]
    
    # Step 1: Generate web search queries using GPT for PENDING questions only
    print("\nStep 1: Generating web search queries using GPT...")
    questions_dict = {q.get('unique_id'): q for q in pending_questions}
    
    # Generate queries for pending query_ids only
    generated_queries = generate_queries_for_questions(questions_dict, query_ids)
    
    total_queries = sum(len(queries) for queries in generated_queries.values())
    print(f"Generated {total_queries} total web search queries for {len(query_ids)} questions")
    
    # Step 2: Get cached responses (with active DB search fallback)
    print("\nStep 2: Retrieving responses (cache + active DB search fallback)...")
    cached_responses = get_all_responses_with_active_search(generated_queries, task_name)
    cached_count = sum(
        1 for responses in cached_responses.values()
        for response in responses.values()
        if response is not None
    )
    print(f"Retrieved {cached_count} responses")
    
    # Step 3: Generate ground truths
    print("\nStep 3: Generating ground truths using LLM...")
    new_ground_truths = generate_ground_truths_for_questions(pending_questions, cached_responses)
    print(f"Generated ground truths for {len(new_ground_truths)} questions")
    
    # Step 4: Merge with existing and save to JSON (as list)
    # Handle new_ground_truths being dict or list
    if isinstance(new_ground_truths, dict):
        new_ground_truths_list = list(new_ground_truths.values())
    else:
        new_ground_truths_list = new_ground_truths if isinstance(new_ground_truths, list) else [new_ground_truths]
    
    # Report which questions got answers vs not
    success_questions = []
    failed_questions = []
    for gt in new_ground_truths_list:
        q_text = gt.get('question', gt.get('unique_id', 'Unknown'))[:80]
        uid = gt.get('unique_id', 'Unknown')
        if gt.get('is_answer_present', False):
            success_questions.append((uid, q_text))
        else:
            failed_questions.append((uid, q_text))
    
    print(f"\n--- RESULTS FOR THIS RUN ---")
    print(f"✅ GOT ANSWERS: {len(success_questions)}")
    for uid, q in success_questions:
        print(f"   ✅ {uid}: {q}...")
    print(f"\n❌ NO ANSWERS: {len(failed_questions)}")
    for uid, q in failed_questions:
        print(f"   ❌ {uid}: {q}...")
    print(f"\nSUMMARY: {len(success_questions)}/{len(new_ground_truths_list)} succeeded ({100*len(success_questions)/max(1,len(new_ground_truths_list)):.1f}%)")
    print(f"----------------------------\n")
    
    merged_ground_truths = existing_ground_truths + new_ground_truths_list
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_ground_truths, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved: {output_file}")
    print(f"Total questions in file: {len(merged_ground_truths)} ({len(new_ground_truths_list)} new + {len(existing_ground_truths)} existing)")
    print(f"{'='*60}\n")
    
    return True


def main():
    """
    Main function to orchestrate direct ground truth generation.
    """
    parser = argparse.ArgumentParser(description='Generate ground truths directly using GPT (no response directories)')
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
