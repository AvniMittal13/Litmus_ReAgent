#!/usr/bin/env python3
"""
Direct question generator for selected task across all scenarios.

This script allows you to:
1. Select a specific task from available tasks
2. Generate questions for that task across all 5 scenarios
3. Uses direct function calls instead of subprocess for better reliability
4. Maintains the same saving conventions as the original scripts

Usage:
    python generate_questions_by_task_direct.py
"""

import sys
import os
import json
import importlib.util
import uuid
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
OUTPUT_DIR = "generated_questions2"

# Question counts per scenario (you can modify these)
QUESTION_COUNTS = {
    1: 10,  # Scenario 1: GT available
    2: 10,  # Scenario 2: Different model performance  
    3: 10,  # Scenario 3: Different language performance
    4: 10,  # Scenario 4: Cross-lingual with gap data
    5: 10,  # Scenario 5: Cross-lingual without gap data
}

# Scenario configurations
SCENARIO_CONFIGS = {
    1: {
        "name": "GT_available",
        "description": "Questions when ground truth data is available",
        "prompt_template": """
You are given a language-to-models mapping for a specific NLP task where ground truth (GT) data is available.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show which models have been benchmarked on which languages for this task.
Each language maps to a list of models that have been evaluated on it.

### Goal

Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
Generate questions of the following types:

1. **Task + Model + Language**: Questions about specific model performance on specific language
2. **Task + Language**: Questions about how different models perform on a specific language  
3. **Task + Model**: Questions about how a specific model performs across languages
4. **Model + Language**: Questions about model performance on language (task implied)
5. **Task only**: Questions about overall task performance across languages/models

### Question Templates (adapt and vary phrasing):

1. *What is the performance of {{model}} on {{task}} for {{language}}?*
2. *How does {{model}} perform on {{task}} in {{language}}?*
3. *Compare {{model1}} and {{model2}} performance for {{language}} on {{task}}.*
4. *Which model performs best for {{task}} in {{language}}?*
5. *What are the {{task}} results for {{model}} across all languages?*
6. *How does {{language}} performance vary across models for {{task}}?*
7. *What languages show the best performance for {{task}}?*
8. *Which models have been evaluated for {{task}} in {{language}}?*
9. *What is the cross-lingual performance of {{model}} on {{task}}?*
10. *How do low-resource languages perform on {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. for tasks like code generation, programming languages might be present as well. DONOT generate questions for programming languages
2. Use the exact task name provided
3. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
4. If task, model, or language is not present in a question, set it as `""` in the output
5. Questions must be clear, end with `?`, and avoid hallucinations
6. Generate diverse questions - avoid repetitive phrasing
7. Focus on realistic evaluation scenarios where GT data would be available

Generate {num_questions} diverse questions covering different question types and language-model combinations.
"""
    },
    2: {
        "name": "model_comparison",
        "description": "Questions comparing different model performances",
        "prompt_template": """
You are given a language-to-models mapping for a specific NLP task to generate comparison questions between different models.

Task: {task_name}
Language-Model Mappings: {mappings}

### Goal

Generate questions that compare different models' performance on the same task. Focus on:

1. **Direct Model Comparisons**: Compare 2-3 specific models
2. **Model Categories**: Compare model families/types
3. **Best/Worst Performance**: Ask about top/bottom performing models
4. **Model Rankings**: Ask about model rankings for specific languages

### Question Templates:

1. *Compare {{model1}} and {{model2}} performance on {{task}} for {{language}}.*
2. *Which model performs better: {{model1}} or {{model2}} on {{task}}?*
3. *What is the ranking of models for {{task}} in {{language}}?*
4. *Which model achieves the best {{task}} performance in {{language}}?*
5. *How do open-source models compare to proprietary models for {{task}}?*
6. *What is the performance gap between {{model1}} and {{model2}} on {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping**
2. Focus on model comparison aspects
3. If multiple models/languages, list alphabetically, comma-separated (no spaces)
4. If task, model, or language is not present, set as `""`
5. Generate diverse comparison scenarios

Generate {num_questions} questions focused on model comparisons.
"""
    },
    3: {
        "name": "language_comparison", 
        "description": "Questions comparing performance across languages",
        "prompt_template": """
You are given a language-to-models mapping for a specific NLP task to generate questions about cross-lingual performance.

Task: {task_name}
Language-Model Mappings: {mappings}

### Goal

Generate questions that compare performance across different languages. Focus on:

1. **Language Comparisons**: Compare specific languages
2. **Cross-lingual Performance**: How models perform across languages
3. **Language Categories**: High/low resource languages
4. **Language Families**: Performance within language families

### Question Templates:

1. *How does {{model}} performance compare between {{lang1}} and {{lang2}} for {{task}}?*
2. *Which languages show the best {{task}} performance?*
3. *How do low-resource languages perform compared to high-resource languages for {{task}}?*
4. *What is the cross-lingual performance of {{model}} on {{task}}?*
5. *Which language family performs best for {{task}}?*
6. *What is the performance gap between English and {{language}} for {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping**
2. Focus on cross-lingual aspects
3. Generate questions about language performance patterns
4. If multiple models/languages, list alphabetically, comma-separated (no spaces)
5. If task, model, or language is not present, set as `""`

Generate {num_questions} questions focused on cross-lingual performance.
"""
    },
    4: {
        "name": "cross_lingual_gap",
        "description": "Questions about cross-lingual performance with gap analysis",
        "prompt_template": """
You are given a language-to-models mapping for a specific NLP task to generate questions about performance gaps between languages.

Task: {task_name}
Language-Model Mappings: {mappings}

### Goal

Generate questions that explore performance gaps and disparities between languages, especially focusing on:

1. **Performance Gaps**: Differences between languages
2. **Resource Disparity**: High vs low resource languages
3. **Model Bias**: Language-specific biases
4. **Gap Analysis**: Quantifying disparities

### Question Templates:

1. *What is the performance gap between English and {{language}} for {{model}} on {{task}}?*
2. *Which languages show the largest performance drops for {{task}}?*
3. *How significant is the cross-lingual performance gap for {{model}}?*
4. *What factors contribute to poor {{task}} performance in {{language}}?*
5. *Which models show the smallest cross-lingual performance gaps?*
6. *How does {{task}} performance degrade for low-resource languages?*

### Rules

1. **Only use languages and models from the provided mapping**
2. Focus on gap analysis and performance disparities
3. Emphasize comparative aspects highlighting differences
4. If multiple models/languages, list alphabetically, comma-separated (no spaces)
5. If task, model, or language is not present, set as `""`

Generate {num_questions} questions focused on cross-lingual performance gaps.
"""
    },
    5: {
        "name": "cross_lingual_no_gap",
        "description": "Questions about cross-lingual performance without gap focus",
        "prompt_template": """
You are given a language-to-models mapping for a specific NLP task to generate general cross-lingual questions.

Task: {task_name}
Language-Model Mappings: {mappings}

### Goal

Generate general questions about cross-lingual performance without focusing on gaps or disparities:

1. **General Cross-lingual**: Overall performance patterns
2. **Language Support**: Which languages are supported
3. **Multilingual Capabilities**: Model multilingual abilities
4. **Language Coverage**: Breadth of language support

### Question Templates:

1. *How does {{model}} perform across different languages for {{task}}?*
2. *Which languages are supported by {{model}} for {{task}}?*
3. *What is the overall cross-lingual performance of {{model}}?*
4. *How many languages has {{model}} been evaluated on for {{task}}?*
5. *Which models provide the best multilingual support for {{task}}?*
6. *What languages show consistent performance across models for {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping**
2. Focus on general cross-lingual aspects (not gaps)
3. Emphasize multilingual capabilities and support
4. If multiple models/languages, list alphabetically, comma-separated (no spaces)
5. If task, model, or language is not present, set as `""`

Generate {num_questions} questions about general cross-lingual performance.
"""
    }
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

def format_mapping_for_prompt(mapping: Dict) -> str:
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in mapping.items():
        models_str = ", ".join(models[:5])  # Limit to first 5 models for readability
        if len(models) > 5:
            models_str += f" (and {len(models)-5} more)"
        formatted_lines.append(f"  {lang}: [{models_str}]")
    
    return "\n".join(formatted_lines)

def add_unique_ids_to_questions(questions: QuestionsGenerated) -> QuestionsGenerated:
    """Add unique IDs to questions that don't have them."""
    for question in questions.questions:
        if not hasattr(question, 'unique_id') or not question.unique_id:
            question.unique_id = str(uuid.uuid4())
    return questions

def generate_questions_for_scenario(task_name: str, mapping: Dict, scenario_num: int, num_questions: int = 10) -> Optional[QuestionsGenerated]:
    """Generate questions for a specific scenario."""
    
    if scenario_num not in SCENARIO_CONFIGS:
        print(f"Error: Unknown scenario {scenario_num}")
        return None
    
    config = SCENARIO_CONFIGS[scenario_num]
    
    # Clean up task name for better readability
    clean_task_name = task_name.replace("_", " ").replace("01 ", "").replace("02 ", "").replace("03 ", "").replace("04 ", "").replace("05 ", "").replace("06 ", "")
    
    # Format mapping for prompt
    formatted_mapping = format_mapping_for_prompt(mapping)
    
    # Generate questions using the LLM
    print(f"    Generating {num_questions} questions for scenario {scenario_num} ({config['name']})...")
    
    prompt = config['prompt_template'].format(
        task_name=clean_task_name,
        mappings=formatted_mapping,
        num_questions=num_questions
    )
    
    try:
        response = get_structured_response(
            prompt=prompt,
            structuredClass=QuestionsGenerated
        )
        response = QuestionsGenerated(**json.loads(response))
        
        # Add unique IDs to questions
        for question in response.questions:
            if not hasattr(question, 'unique_id'):
                # Create a new question dict with unique_id
                question_dict = question.dict()
                question_dict['unique_id'] = str(uuid.uuid4())
                # Update the question object (note: this is a workaround for immutable pydantic models)
        
        return response
        
    except Exception as e:
        print(f"    Error generating questions for scenario {scenario_num}: {e}")
        return None

def save_questions_to_file(questions: QuestionsGenerated, task_name: str, scenario_num: int) -> bool:
    """Save generated questions to a JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    config = SCENARIO_CONFIGS[scenario_num]
    output_file = os.path.join(OUTPUT_DIR, f"{task_name}_questions_scenario{scenario_num}.json")
    
    try:
        # Convert to dict for JSON serialization and add unique IDs
        questions_list = []
        for q in questions.questions:
            q_dict = q.dict()
            if 'unique_id' not in q_dict:
                q_dict['unique_id'] = str(uuid.uuid4())
            questions_list.append(q_dict)
        
        questions_dict = {
            "task": task_name,
            "scenario": config['name'],
            "questions": questions_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(questions_dict, f, indent=2, ensure_ascii=False)
        
        print(f"    ✓ Saved {len(questions.questions)} questions to {output_file}")
        return True
        
    except Exception as e:
        print(f"    ✗ Error saving questions to {output_file}: {e}")
        return False

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
        config = SCENARIO_CONFIGS[scenario_num]
        questions_count = QUESTION_COUNTS.get(scenario_num, 10)
        print(f"  {scenario_num}. {config['description']} ({questions_count} questions)")
    
    # Ask for confirmation
    print(f"\nThis will generate questions for {task_name} across all 5 scenarios.")
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled.")
        return False
    
    # Generate questions for each scenario
    success_count = 0
    all_results = {}
    
    for scenario_num in range(1, 6):
        config = SCENARIO_CONFIGS[scenario_num]
        print(f"\n--- Scenario {scenario_num}: {config['description']} ---")
        
        num_questions = QUESTION_COUNTS.get(scenario_num, 10)
        questions = generate_questions_for_scenario(task_name, mapping, scenario_num, num_questions)
        
        if questions:
            if save_questions_to_file(questions, task_name, scenario_num):
                success_count += 1
                all_results[scenario_num] = len(questions.questions)
            else:
                all_results[scenario_num] = 0
        else:
            print(f"    ✗ Failed to generate questions for scenario {scenario_num}")
            all_results[scenario_num] = 0
    
    # Print summary
    print(f"\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    
    total_questions = sum(all_results.values())
    print(f"Task: {task_name}")
    print(f"Scenarios attempted: 5")
    print(f"Scenarios successful: {success_count}")
    print(f"Total questions generated: {total_questions}")
    
    for scenario_num, count in all_results.items():
        config = SCENARIO_CONFIGS[scenario_num]
        status = "✓" if count > 0 else "✗"
        print(f"  {status} Scenario {scenario_num} ({config['name']}): {count} questions")
    
    if success_count == 5:
        print(f"\n✓ All question files generated successfully for {task_name}!")
        return True
    else:
        print(f"\n⚠ Some question files may be missing or incomplete.")
        return False

def main():
    """Main function to run the interactive task selection and question generation."""
    print("Question Generator for Selected Task (Direct Mode)")
    print("This script generates questions for a selected task across all scenarios.")
    print("Uses direct function calls for better reliability and speed.")
    
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
