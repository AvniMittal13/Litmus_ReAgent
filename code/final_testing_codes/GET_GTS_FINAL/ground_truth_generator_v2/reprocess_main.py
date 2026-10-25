"""
Reprocess failed ground truths (is_answer_present=false) using active DB search.
This script reuses existing V2 modules without modifying original main.py
"""
import json
import argparse
from pathlib import Path

from .config import EXISTING_OUTPUT_DIR, TASKS
from .failed_loader import load_failed_questions, get_task_from_key
from .query_generator import generate_web_search_queries
from .cache_retriever import get_all_responses_with_active_search
from .ground_truth_generator import generate_ground_truth


def reprocess_failed_questions():
    """
    Main function to reprocess failed questions.
    """
    print("=" * 60)
    print("REPROCESSING FAILED GROUND TRUTHS")
    print("=" * 60)
    
    # Step 1: Load failed questions
    print("\nStep 1: Loading failed questions from Ground_truths_1...")
    failed_questions = load_failed_questions()
    
    if not failed_questions:
        print("No failed questions found!")
        return
    
    total_reprocessed = 0
    total_fixed = 0
    
    # Process each task-scenario
    for key, questions in failed_questions.items():
        print(f"\n{'='*60}")
        print(f"Processing: {key} ({len(questions)} questions)")
        print(f"{'='*60}")
        
        task = get_task_from_key(key)
        
        # Step 2: Generate search queries for each question
        print("\nStep 2: Generating search queries...")
        extracted_queries = {}
        for q in questions:
            unique_id = q.get('unique_id')
            complete_question = q.get('complete_question')
            
            # Generate 5 search queries
            queries = generate_web_search_queries(complete_question)
            extracted_queries[unique_id] = queries
            
            if queries:
                print(f"  Generated {len(queries)} queries for: {complete_question[:50]}...")
        
        # Step 3: Get responses (cache + active search)
        print("\nStep 3: Getting responses (cache + active DB search)...")
        all_responses = get_all_responses_with_active_search(extracted_queries, task)
        
        # Step 4: Generate new ground truths
        print("\nStep 4: Generating ground truths...")
        updated_questions = []
        
        for q in questions:
            unique_id = q.get('unique_id')
            complete_question = q.get('complete_question')
            question_type = q.get('predictive_or_qna', 'qna')
            
            # Get responses for this question
            responses = all_responses.get(unique_id, {})
            
            # Check if we have any responses
            has_responses = any(r is not None for r in responses.values())
            
            if has_responses:
                # Generate new ground truth
                result = generate_ground_truth(complete_question, responses, question_type)
                
                # Update question with new result
                q['is_answer_present'] = result.get('is_answer_present', False)
                q['ground_truth_metrics_and_values_for_predictive'] = result.get('ground_truth_metrics_and_values_for_predictive', [])
                q['answer_text_for_qna'] = result.get('answer_text_for_qna', '')
                q['atleast_one_successful_execution'] = True
                
                if result.get('is_answer_present'):
                    total_fixed += 1
                    print(f"  ✅ Fixed: {complete_question[:60]}...")
                else:
                    print(f"  ⚠️  Still no answer: {complete_question[:60]}...")
            else:
                print(f"  ❌ No responses: {complete_question[:60]}...")
            
            updated_questions.append(q)
            total_reprocessed += 1
        
        # Step 5: Update original JSON file
        output_file = Path(EXISTING_OUTPUT_DIR) / f"{key}_ground_truths.json"
        
        # Load full original file (includes questions that weren't failed)
        with open(output_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Create map of updated questions by unique_id
        updated_map = {q['unique_id']: q for q in updated_questions}
        
        # Update only the failed questions in original data
        for i, item in enumerate(original_data):
            if item['unique_id'] in updated_map:
                original_data[i] = updated_map[item['unique_id']]
        
        # Save updated file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(original_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nUpdated: {output_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total reprocessed: {total_reprocessed}")
    print(f"Fixed (now have answers): {total_fixed}")
    print(f"Still failed: {total_reprocessed - total_fixed}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Reprocess failed ground truths')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without saving')
    args = parser.parse_args()
    
    reprocess_failed_questions()


if __name__ == "__main__":
    main()
