"""
Validate and filter existing generated questions.
Removes questions with hallucinated languages/models.

Usage:
    python validate_existing_questions.py
    python validate_existing_questions.py --task "01_Code_Generation"
    python validate_existing_questions.py --scenario 2
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mapping_computers import (
    compute_scenario1_mapping,
    compute_scenario2_mapping,
    compute_scenario3_mapping,
    compute_scenario4_mapping,
    compute_scenario5_mapping,
)

BASE_DATA_PATH = r"./all_final_csvs_finall"
INPUT_DIR = "generated_questions"
OUTPUT_DIR = "validated_questions"

MAPPING_COMPUTERS = {
    1: compute_scenario1_mapping,
    2: compute_scenario2_mapping,
    3: compute_scenario3_mapping,
    4: compute_scenario4_mapping,
    5: compute_scenario5_mapping,
}


def validate_question(q: Dict, mapping: Dict[str, List[str]]) -> Tuple[bool, str]:
    """
    Validate a question against the mapping.
    Returns (is_valid, reason_if_invalid).
    """
    valid_langs = set(mapping.keys())
    valid_models = set()
    for models in mapping.values():
        valid_models.update(models)
    
    # Check languages
    if q.get('languages'):
        for lang in [l.strip() for l in q['languages'].split(',')]:
            if lang and lang not in valid_langs:
                return False, f"Invalid language: {lang}"
    
    # Check models
    if q.get('models'):
        for model in [m.strip() for m in q['models'].split(',')]:
            if model and model not in valid_models:
                return False, f"Invalid model: {model}"
    
    return True, ""


def validate_file(filepath: str, scenario: int, task_folder: str) -> Dict:
    """Validate a single questions file."""
    
    # Compute the mapping for this scenario
    compute_mapping = MAPPING_COMPUTERS.get(scenario)
    if not compute_mapping:
        return {"error": f"Unknown scenario: {scenario}"}
    
    task_path = os.path.join(BASE_DATA_PATH, task_folder)
    _, mapping = compute_mapping(task_path)
    
    if not mapping:
        return {"error": f"No mapping data for {task_folder} scenario {scenario}"}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    valid_questions = []
    invalid_questions = []
    
    for q in questions:
        is_valid, reason = validate_question(q, mapping)
        if is_valid:
            valid_questions.append(q)
        else:
            invalid_questions.append({**q, 'rejection_reason': reason})
    
    return {
        'total': len(questions),
        'valid': len(valid_questions),
        'invalid': len(invalid_questions),
        'valid_questions': valid_questions,
        'invalid_questions': invalid_questions
    }


def main():
    parser = argparse.ArgumentParser(description="Validate generated questions")
    parser.add_argument('--task', type=str, help="Filter by task name")
    parser.add_argument('--scenario', type=int, help="Filter by scenario (1-5)")
    parser.add_argument('--output', type=str, default=OUTPUT_DIR, help="Output directory")
    parser.add_argument('--report-only', action='store_true', help="Only show report, don't save")
    args = parser.parse_args()
    
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return
    
    os.makedirs(args.output, exist_ok=True)
    
    total_valid = 0
    total_invalid = 0
    results = []
    
    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.endswith('.json'):
            continue
        
        # Parse filename: {task}_questions_scenario{N}.json
        parts = filename.replace('_questions_scenario', '_SPLIT_').replace('.json', '').split('_SPLIT_')
        if len(parts) != 2:
            continue
        
        task_folder = parts[0]
        try:
            scenario = int(parts[1])
        except:
            continue
        
        # Apply filters
        if args.task and args.task not in task_folder:
            continue
        if args.scenario and scenario != args.scenario:
            continue
        
        filepath = os.path.join(INPUT_DIR, filename)
        result = validate_file(filepath, scenario, task_folder)
        
        if 'error' in result:
            print(f"  ⚠️  {filename}: {result['error']}")
            continue
        
        total_valid += result['valid']
        total_invalid += result['invalid']
        
        status = "✅" if result['invalid'] == 0 else "⚠️"
        print(f"{status} {filename}: {result['valid']}/{result['total']} valid ({result['invalid']} rejected)")
        
        if result['invalid_questions']:
            for iq in result['invalid_questions'][:3]:
                print(f"    - {iq['rejection_reason']}")
            if len(result['invalid_questions']) > 3:
                print(f"    ... and {len(result['invalid_questions'])-3} more")
        
        results.append({
            'file': filename,
            'task': task_folder,
            'scenario': scenario,
            **result
        })
        
        # Save validated questions
        if not args.report_only and result['valid_questions']:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data['questions'] = result['valid_questions']
            data['validation'] = {
                'original_count': result['total'],
                'valid_count': result['valid'],
                'rejected_count': result['invalid']
            }
            
            output_path = os.path.join(args.output, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total valid questions: {total_valid}")
    print(f"Total invalid (hallucinated): {total_invalid}")
    print(f"Validation rate: {total_valid/(total_valid+total_invalid)*100:.1f}%")
    
    if not args.report_only:
        print(f"\nValidated questions saved to: {args.output}/")


if __name__ == '__main__':
    main()
