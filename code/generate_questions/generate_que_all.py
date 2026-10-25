import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response
from pydantic import BaseModel
import importlib.util
import json
from pathlib import Path

class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str
        languages: str

    questions: list[Question]


prompt_scenario1_mapping = """
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

### Output Format

Return **only JSON** in this structure:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str

    questions: list[Question]
```

Generate {num_questions} diverse questions covering different question types and language-model combinations.
"""


def load_task_mapping(task_folder_path):
    """Load the language-models mapping from a task folder."""
    task_name = os.path.basename(task_folder_path).lower()
    mapping_file = os.path.join(task_folder_path, f"{task_name}_language_models_mapping.py")
    # mapping_file = os.path.join(task_folder_path, f"reduced_{task_name}_language_models_mapping.py")

    if not os.path.exists(mapping_file):
        print(f"Warning: Mapping file not found: {mapping_file}")
        return None, None
    
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


def format_mapping_for_prompt(mapping):
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in mapping.items():
        models_str = ", ".join(models[:5])  # Limit to first 5 models for readability
        if len(models) > 5:
            models_str += f" (and {len(models)-5} more)"
        formatted_lines.append(f"  {lang}: [{models_str}]")
    
    return "\n".join(formatted_lines)


def generate_questions_for_task(task_folder_path, num_questions=5):
    """Generate questions for a specific task using its language-models mapping."""
    task_name, mapping = load_task_mapping(task_folder_path)
    
    if not task_name or not mapping:
        return None
    
    # Clean up task name for better readability
    clean_task_name = task_name.replace("_", " ").replace("01 ", "").replace("02 ", "").replace("03 ", "").replace("04 ", "").replace("05 ", "").replace("06 ", "")
    
    # Format mapping for prompt
    formatted_mapping = format_mapping_for_prompt(mapping)
    
    # Generate questions using the LLM
    print("generating questions for the following parameters: ")
    print(f"  Task Name: {clean_task_name}")
    print(f"  Mappings:\n{formatted_mapping}")
    print(f"  Number of Questions: {num_questions}")
    prompt = prompt_scenario1_mapping.format(
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

        return response
    
    except Exception as e:
        print(f"Error generating questions for {task_name}: {e}")
        return None


def save_questions_to_file(questions, task_name, output_dir="generated_questions_overall"):
    """Save generated questions to a JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{task_name}_questions_scenario1.json")
    
    # Convert to dict for JSON serialization
    print(questions)
    questions_dict = {
        "task": task_name,
        "scenario": "GT_available",
        "questions": [q.dict() for q in questions.questions]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(questions.questions)} questions to {output_file}")


def process_all_tasks(base_path=r"./all_final_csvs_finall", num_questions_per_task=5):
    """Process all task folders and generate questions for each."""
    if not os.path.exists(base_path):
        print(f"Base path not found: {base_path}")
        return
    
    task_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    
    print(f"Found {len(task_folders)} task folders to process:")
    for folder in task_folders:
        print(f"  - {folder}")
    
    all_results = {}
    
    for folder in sorted(task_folders):
        folder_path = os.path.join(base_path, folder)
        print(f"\nProcessing {folder}...")
        
        questions = generate_questions_for_task(folder_path, num_questions_per_task)
        
        if questions:
            save_questions_to_file(questions, folder)
            all_results[folder] = len(questions.questions)
            print(f"Generated {len(questions.questions)} questions for {folder}")
        else:
            print(f"Failed to generate questions for {folder}")
    
    # Print summary
    print(f"\n" + "="*60)
    print("QUESTION GENERATION SUMMARY")
    print("="*60)
    total_questions = sum(all_results.values())
    print(f"Total tasks processed: {len(all_results)}")
    print(f"Total questions generated: {total_questions}")
    
    for task, count in all_results.items():
        print(f"  {{task}}: {count} questions")


if __name__ == "__main__":
    # Process all tasks in the all_final_csvs folder
    process_all_tasks()
    
    # Alternative: Process a single task
    # questions = generate_questions_for_task("all_final_csvs/01_Code_Generation")
    # if questions:
    #     save_questions_to_file(questions, "01_Code_Generation")