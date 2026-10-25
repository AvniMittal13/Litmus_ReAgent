"""
Core question generation logic.
Uses mapping computers + prompts to generate questions.
"""
import os
import sys
import json
import uuid
from typing import Dict, List, Optional, Callable, Tuple

# Add parent directory to path for utils import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response
from models import QuestionsGenerated, Question
from gen_utils import format_mapping_for_prompt, clean_task_name


def validate_questions(
    questions: QuestionsGenerated, 
    mapping: Dict[str, List[str]]
) -> Tuple[List[Question], List[Question]]:
    """
    Validate questions against the provided mapping.
    Returns (valid_questions, invalid_questions).
    """
    valid_langs = set(mapping.keys())
    valid_models = set()
    for models in mapping.values():
        valid_models.update(models)
    
    valid = []
    invalid = []
    
    for q in questions.questions:
        is_valid = True
        
        # Check languages
        if q.languages:
            q_langs = [l.strip() for l in q.languages.split(',')]
            for lang in q_langs:
                if lang and lang not in valid_langs:
                    is_valid = False
                    break
        
        # Check models
        if q.models and is_valid:
            q_models = [m.strip() for m in q.models.split(',')]
            for model in q_models:
                if model and model not in valid_models:
                    is_valid = False
                    break
        
        if is_valid:
            valid.append(q)
        else:
            invalid.append(q)
    
    return valid, invalid


def generate_questions(
    task_name: str,
    mapping: Dict[str, List[str]],
    prompt_template: str,
    num_questions: int = 50,
    num_predictive: int = 25,
    num_qna: int = 25
) -> Optional[QuestionsGenerated]:
    """
    Generate questions using the provided mapping and prompt template.
    
    Args:
        task_name: Name of the task
        mapping: Language-model mapping dictionary
        prompt_template: Prompt template to use (must have placeholders)
        num_questions: Total number of questions to generate
        num_predictive: Number of predictive questions (for common prompt)
        num_qna: Number of QnA questions (for common prompt)
    
    Returns:
        QuestionsGenerated object or None if failed
    """
    if not mapping:
        print(f"Empty mapping for {task_name}")
        return None
    
    # Clean up task name
    clean_name = clean_task_name(task_name)
    
    # Format mapping for prompt
    formatted_mapping = format_mapping_for_prompt(mapping)
    
    # Build prompt with available placeholders
    prompt_kwargs = {
        'task_name': clean_name,
        'mappings': formatted_mapping,
        'num_questions': num_questions,
    }
    
    # Add optional placeholders if they exist in the template
    if '{num_predictive}' in prompt_template:
        prompt_kwargs['num_predictive'] = num_predictive
    if '{num_qna}' in prompt_template:
        prompt_kwargs['num_qna'] = num_qna
    
    prompt = prompt_template.format(**prompt_kwargs)
    
    try:
        response = get_structured_response(
            prompt=prompt,
            structuredClass=QuestionsGenerated
        )
        result = QuestionsGenerated(**json.loads(response))
        return result
    
    except Exception as e:
        print(f"Error generating questions for {task_name}: {e}")
        return None


def generate_questions_validated(
    task_name: str,
    mapping: Dict[str, List[str]],
    prompt_template: str,
    num_questions: int = 50,
    num_predictive: int = 25,
    num_qna: int = 25,
    max_retries: int = 3
) -> Optional[QuestionsGenerated]:
    """
    Generate questions with validation and retry logic.
    Rejects hallucinated questions and retries until target is met.
    
    Args:
        task_name: Name of the task
        mapping: Language-model mapping dictionary
        prompt_template: Prompt template to use
        num_questions: Total number of questions to generate
        num_predictive: Number of predictive questions
        num_qna: Number of QnA questions
        max_retries: Maximum number of retry attempts
    
    Returns:
        QuestionsGenerated object with only validated questions, or None if failed
    """
    all_valid = []
    target = num_questions
    
    for attempt in range(max_retries):
        # Request more questions to compensate for potential rejections
        remaining = target - len(all_valid)
        if remaining <= 0:
            break
            
        # Request 50% extra to account for rejections
        request_count = min(int(remaining * 1.5) + 5, 60)
        request_predictive = request_count // 2
        request_qna = request_count - request_predictive
        
        result = generate_questions(
            task_name, mapping, prompt_template, 
            request_count, request_predictive, request_qna
        )
        
        if not result:
            print(f"Attempt {attempt+1}: Generation failed, retrying...")
            continue
        
        valid, invalid = validate_questions(result, mapping)
        all_valid.extend(valid)
        
        if invalid:
            invalid_langs = set()
            invalid_models = set()
            for q in invalid:
                if q.languages:
                    for l in q.languages.split(','):
                        l = l.strip()
                        if l and l not in mapping:
                            invalid_langs.add(l)
                if q.models:
                    all_models = set()
                    for m_list in mapping.values():
                        all_models.update(m_list)
                    for m in q.models.split(','):
                        m = m.strip()
                        if m and m not in all_models:
                            invalid_models.add(m)
            
            print(f"Attempt {attempt+1}: Rejected {len(invalid)} hallucinated questions")
            if invalid_langs:
                print(f"  - Invalid languages: {invalid_langs}")
            if invalid_models:
                print(f"  - Invalid models: {invalid_models}")
        
        print(f"Attempt {attempt+1}: Collected {len(all_valid)}/{target} valid questions")
        
        if len(all_valid) >= target:
            break
    
    if not all_valid:
        print(f"Failed to generate any valid questions after {max_retries} attempts")
        return None
    
    # Trim to exact target
    final_questions = all_valid[:target]
    
    if len(final_questions) < target:
        print(f"Warning: Only generated {len(final_questions)}/{target} valid questions")
    
    return QuestionsGenerated(questions=final_questions)


def save_questions(
    questions: QuestionsGenerated,
    task_name: str,
    scenario: int,
    scenario_name: str,
    output_dir: str = "generated_questions"
) -> str:
    """
    Save generated questions to a JSON file.
    
    Args:
        questions: QuestionsGenerated object
        task_name: Name of the task folder
        scenario: Scenario number (1-5)
        scenario_name: Human-readable scenario name
        output_dir: Output directory path
    
    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{task_name}_questions_scenario{scenario}.json")
    
    # Add unique_id to each question
    questions_with_ids = []
    for q in questions.questions:
        q_dict = q.model_dump()
        q_dict["unique_id"] = str(uuid.uuid4())
        questions_with_ids.append(q_dict)
    
    questions_dict = {
        "task": task_name,
        "scenario": scenario_name,
        "questions": questions_with_ids
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(questions.questions)} questions to {output_file}")
    return output_file
