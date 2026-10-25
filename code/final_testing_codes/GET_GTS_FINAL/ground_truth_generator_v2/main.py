"""
Main orchestration script for ground truth generation.
"""
import json
import argparse
from pathlib import Path
from .config import OUTPUT_DIR, TASKS, NUM_SCENARIOS
from .query_loader import load_questions
from .query_finder import find_all_query_folders
from .intermediate_extractor import extract_all_queries
from .cache_retriever import get_all_cached_responses_for_questions
from .ground_truth_generator import generate_ground_truths_for_questions
from .query_generator import generate_queries_for_questions


def process_task_scenario(task_name: str, scenario_num: int, all_questions: dict) -> bool:
    """
    Process a single task-scenario combination and generate ground truth JSON.
    
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
    
    # Extract unique_ids
    query_ids = [q.get('unique_id') for q in questions]
    
    # Step 1: Find query_id folders
    print("\nStep 1: Finding query_id folders...")
    query_folders = find_all_query_folders(query_ids, task_name, scenario_num)
    found_count = sum(1 for folder in query_folders.values() if folder is not None)
    print(f"Found folders for {found_count}/{len(query_ids)} queries")
    
    # Step 2: Extract web search queries from intermediates
    print("\nStep 2: Extracting web search queries from intermediates...")
    extracted_queries = extract_all_queries(query_folders)
    total_queries = sum(len(queries) for queries in extracted_queries.values())
    print(f"Extracted {total_queries} total web search queries")
    
    # Step 2.5: Generate queries using GPT for questions with no intermediates
    empty_query_ids = [qid for qid, queries in extracted_queries.items() if not queries]
    if empty_query_ids:
        print(f"\nStep 2.5: Generating web search queries using GPT for {len(empty_query_ids)} questions with no intermediates...")
        
        # Create mapping of query_id to question object
        questions_dict = {q.get('unique_id'): q for q in questions}
        
        # Generate queries using GPT
        generated_queries = generate_queries_for_questions(questions_dict, empty_query_ids)
        
        # Update extracted_queries with generated queries
        for query_id, queries in generated_queries.items():
            extracted_queries[query_id] = queries
        
        # Update statistics
        generated_count = sum(len(queries) for queries in generated_queries.values())
        total_queries += generated_count
        print(f"Generated {generated_count} queries using GPT")
        print(f"Total queries (extracted + generated): {total_queries}")
    
    # Step 3: Get cached responses
    print("\nStep 3: Retrieving cached responses...")
    cached_responses = get_all_cached_responses_for_questions(extracted_queries)
    cached_count = sum(
        1 for responses in cached_responses.values()
        for response in responses.values()
        if response is not None
    )
    print(f"Retrieved {cached_count} cached responses")
    
    # Step 4: Generate ground truths
    print("\nStep 4: Generating ground truths using LLM...")
    ground_truths = generate_ground_truths_for_questions(questions, cached_responses)
    print(f"Generated ground truths for {len(ground_truths)} questions")
    
    # Step 5: Save to JSON
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{key}_ground_truths.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ground_truths, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved: {output_file}")
    print(f"{'='*60}\n")
    
    return True


def main():
    """
    Main function to orchestrate ground truth generation.
    """
    parser = argparse.ArgumentParser(description='Generate ground truths for all task-scenario combinations')
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
