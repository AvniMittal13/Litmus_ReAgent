"""
Validate questions against language-models mapping and regenerate deleted ones.

Usage:
    python validate_and_regenerate.py --task 01_Code_Generation
    python validate_and_regenerate.py --task 01_Code_Generation --dry-run
"""

import os
import sys
import json
import argparse
import importlib.util
from typing import Dict, List, Tuple, Set
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generator import generate_questions_validated
from prompts import COMMON_PROMPT

# Paths
ROOT_DIR = r"./"
MAPPINGS_DIR = os.path.join(ROOT_DIR, "all_final_csvs_finall")
QUESTIONS_DIR = os.path.join(ROOT_DIR, "generated_questions")


def load_mapping_from_file(task_folder: str) -> Dict[str, List[str]]:
    """
    Load the LANGUAGE_MODELS_MAPPING from the task's mapping file.
    e.g., 01_Code_Generation_language_models_mapping.py
    """
    mapping_file = os.path.join(
        MAPPINGS_DIR, task_folder, 
        f"{task_folder}_language_models_mapping.py"
    )
    
    if not os.path.exists(mapping_file):
        print(f"Mapping file not found: {mapping_file}")
        return {}
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("mapping_module", mapping_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return getattr(module, 'LANGUAGE_MODELS_MAPPING', {})


def normalize_model_name(model: str) -> str:
    """Normalize model name for comparison."""
    return model.strip().lower().replace(" ", "").replace("-", "").replace("_", "")


def is_model_match(q_model: str, mapping_models: List[str]) -> bool:
    """Check if question model matches any model in mapping (fuzzy match)."""
    q_norm = normalize_model_name(q_model)
    for m in mapping_models:
        m_norm = normalize_model_name(m)
        # Exact match or one contains the other
        if q_norm == m_norm or q_norm in m_norm or m_norm in q_norm:
            return True
    return False


def validate_question_against_mapping(
    question: Dict, 
    mapping: Dict[str, List[str]]
) -> Tuple[bool, str]:
    """
    Validate a single question against the language-models mapping.
    Returns (is_valid, reason_if_invalid)
    """
    lang = question.get('languages', '').strip()
    model = question.get('models', '').strip()
    
    if not lang and not model:
        return True, ""  # No specific constraints
    
    # Get all valid models across all languages
    all_valid_models = set()
    for models in mapping.values():
        all_valid_models.update(models)
    
    # Check if language exists
    if lang and lang not in mapping:
        return False, f"Language '{lang}' not in mapping"
    
    # Check if model exists for this specific language
    if lang and model:
        lang_models = mapping.get(lang, [])
        if not is_model_match(model, lang_models):
            return False, f"Model '{model}' not available for language '{lang}'"
    
    # Check if model exists at all
    if model and not lang:
        if not is_model_match(model, list(all_valid_models)):
            return False, f"Model '{model}' not in any mapping"
    
    return True, ""


def validate_questions_file(
    filepath: str, 
    mapping: Dict[str, List[str]]
) -> Dict:
    """
    Validate all questions in a file against the mapping.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    
    valid_questions = []
    invalid_questions = []
    
    predictive_deleted = 0
    qna_deleted = 0
    
    for q in questions:
        is_valid, reason = validate_question_against_mapping(q, mapping)
        
        if is_valid:
            valid_questions.append(q)
        else:
            q_type = q.get('question_type', 'Unknown')
            if q_type.lower() == 'predictive':
                predictive_deleted += 1
            else:
                qna_deleted += 1
            invalid_questions.append({**q, 'rejection_reason': reason})
    
    return {
        'original_data': data,
        'valid_questions': valid_questions,
        'invalid_questions': invalid_questions,
        'predictive_deleted': predictive_deleted,
        'qna_deleted': qna_deleted,
        'total_deleted': len(invalid_questions)
    }


def regenerate_questions(
    task_name: str,
    mapping: Dict[str, List[str]],
    num_predictive: int,
    num_qna: int
) -> List[Dict]:
    """
    Generate replacement questions.
    """
    total = num_predictive + num_qna
    if total == 0:
        return []
    
    print(f"\n  Generating {num_predictive} predictive + {num_qna} QnA questions...")
    
    result = generate_questions_validated(
        task_name=task_name,
        mapping=mapping,
        prompt_template=COMMON_PROMPT,
        num_questions=total,
        num_predictive=num_predictive,
        num_qna=num_qna,
        max_retries=3
    )
    
    if not result:
        print("  ❌ Failed to generate replacement questions")
        return []
    
    # Convert to dict format with unique_ids
    import uuid
    new_questions = []
    for q in result.questions:
        new_questions.append({
            'complete_question': q.complete_question,
            'task': q.task,
            'models': q.models,
            'languages': q.languages,
            'question_type': q.question_type,
            'unique_id': str(uuid.uuid4())
        })
    
    return new_questions


def process_task(task_folder: str, dry_run: bool = False):
    """
    Process all scenario files for a task.
    """
    print(f"\n{'='*60}")
    print(f"Processing: {task_folder}")
    print(f"{'='*60}")
    
    # Load the mapping
    mapping = load_mapping_from_file(task_folder)
    if not mapping:
        print(f"❌ Failed to load mapping for {task_folder}")
        return
    
    print(f"Loaded mapping with {len(mapping)} languages")
    
    # Find all scenario files for this task
    scenario_files = []
    for f in os.listdir(QUESTIONS_DIR):
        if f.startswith(task_folder) and f.endswith('.json'):
            scenario_files.append(f)
    
    scenario_files.sort()
    
    total_stats = {
        'files_processed': 0,
        'total_deleted': 0,
        'total_generated': 0,
        'predictive_deleted': 0,
        'qna_deleted': 0
    }
    
    for filename in scenario_files:
        filepath = os.path.join(QUESTIONS_DIR, filename)
        print(f"\n--- {filename} ---")
        
        # Validate
        result = validate_questions_file(filepath, mapping)
        
        print(f"  Original: {len(result['valid_questions']) + len(result['invalid_questions'])} questions")
        print(f"  Valid: {len(result['valid_questions'])}")
        print(f"  Invalid: {len(result['invalid_questions'])} (Predictive: {result['predictive_deleted']}, QnA: {result['qna_deleted']})")
        
        if result['invalid_questions']:
            print(f"  Deleted questions:")
            for iq in result['invalid_questions'][:5]:
                print(f"    ❌ [{iq.get('question_type', '?')}] {iq.get('complete_question', '')[:60]}...")
                print(f"       Reason: {iq.get('rejection_reason', 'Unknown')}")
            if len(result['invalid_questions']) > 5:
                print(f"    ... and {len(result['invalid_questions']) - 5} more")
        
        total_stats['files_processed'] += 1
        total_stats['total_deleted'] += result['total_deleted']
        total_stats['predictive_deleted'] += result['predictive_deleted']
        total_stats['qna_deleted'] += result['qna_deleted']
        
        if dry_run:
            print(f"  [DRY RUN] Would regenerate and update file")
            continue
        
        if result['total_deleted'] == 0:
            print(f"  ✅ No invalid questions, skipping")
            continue
        
        # Generate replacements
        new_questions = regenerate_questions(
            task_name=task_folder,
            mapping=mapping,
            num_predictive=result['predictive_deleted'],
            num_qna=result['qna_deleted']
        )
        
        total_stats['total_generated'] += len(new_questions)
        
        # Update the file
        updated_data = result['original_data'].copy()
        updated_data['questions'] = result['valid_questions'] + new_questions
        updated_data['validation_stats'] = {
            'original_count': len(result['valid_questions']) + len(result['invalid_questions']),
            'deleted_count': result['total_deleted'],
            'deleted_predictive': result['predictive_deleted'],
            'deleted_qna': result['qna_deleted'],
            'regenerated_count': len(new_questions)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Updated file: {len(updated_data['questions'])} questions ({len(new_questions)} new)")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY for {task_folder}")
    print(f"{'='*60}")
    print(f"Files processed: {total_stats['files_processed']}")
    print(f"Total deleted: {total_stats['total_deleted']}")
    print(f"  - Predictive: {total_stats['predictive_deleted']}")
    print(f"  - QnA: {total_stats['qna_deleted']}")
    print(f"Total regenerated: {total_stats['total_generated']}")
    
    return total_stats


def main():
    parser = argparse.ArgumentParser(description="Validate and regenerate questions")
    parser.add_argument('--task', type=str, required=True, 
                       help="Task folder name (e.g., 01_Code_Generation)")
    parser.add_argument('--dry-run', action='store_true',
                       help="Only show what would be deleted, don't modify files")
    
    args = parser.parse_args()
    
    process_task(args.task, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
