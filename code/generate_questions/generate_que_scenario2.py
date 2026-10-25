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


prompt_scenario2_mapping = """
You are given a language-to-models mapping for a specific NLP task where ground truth (GT) data is NOT available.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show which models have been benchmarked on which languages for this task.
Each language maps to a list of models that have been evaluated on it.

### Goal

Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
Generate questions of the following types:

1. **Task + Model + Language**: Questions about specific model performance on specific language
2. **Task + Language**: Questions about how different models perform on a specific language  
3. **Model + Language**: Questions about model performance on language (task implied)
4. **Task only**: Questions about overall task performance across languages/models

### Question Templates (adapt and vary phrasing):

1. *What is the performance of {{model}} on {{task}} for {{language}}?*
2. *How does {{model}} perform on {{task}} in {{language}}?*
3. *Compare {{model1}} and {{model2}} performance for {{language}} on {{task}}.*
4. *Which model performs best for {{task}} in {{language}}?*
5. *How does {{language}} performance vary across models for {{task}}?*
6. *What languages show the best performance for {{task}}?*
7. *Which models have been evaluated for {{task}} in {{language}}?*
8. *How do low-resource languages perform on {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. for tasks like code generation, programming languages might be present as well. DONOT generate questions for programming languages
2. Use the exact task name provided
3. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
4. If task, model, or language is not present in a question, set it as `""` in the output
5. Questions must be clear, end with `?`, and avoid hallucinations
6. Generate diverse questions - avoid repetitive phrasing
7. Focus on evaluation gaps and missing benchmarks where GT data is NOT available

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


def load_mapping_file(file_path):
    """Load a mapping file and return the LANGUAGE_MODELS_MAPPING."""
    if not os.path.exists(file_path):
        print(f"Warning: Mapping file not found: {file_path}")
        return None
    
    # Load the mapping file as a module
    spec = importlib.util.spec_from_file_location("mapping_module", file_path)
    mapping_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mapping_module)
    
    # Extract the mapping
    if hasattr(mapping_module, 'LANGUAGE_MODELS_MAPPING'):
        return mapping_module.LANGUAGE_MODELS_MAPPING
    else:
        print(f"Warning: LANGUAGE_MODELS_MAPPING not found in {file_path}")
        return None


def compute_difference_mapping(task_folder_path):
    """Compute the difference between combined and reduced mappings for scenario 2."""
    task_name = os.path.basename(task_folder_path).lower()
    
    # Paths to the mapping files
    combined_file = os.path.join(task_folder_path, f"{task_name}_language_models_mapping.py")
    reduced_file = os.path.join(task_folder_path, f"reduced_{task_name}_language_models_mapping.py")
    
    # Load both mappings
    combined_mapping = load_mapping_file(combined_file)
    reduced_mapping = load_mapping_file(reduced_file)
    
    if not combined_mapping or not reduced_mapping:
        return None, None
    
    # Compute difference: models in combined but not in reduced for each language
    difference_mapping = {}
    
    for language in combined_mapping:
        combined_models = set(combined_mapping[language])
        reduced_models = set(reduced_mapping.get(language, []))
        
        # Models that are in combined but not in reduced (missing evaluations)
        missing_models = combined_models - reduced_models
        
        if missing_models:  # Only include languages with missing models
            difference_mapping[language] = sorted(list(missing_models))
    
    return task_name, difference_mapping


def format_mapping_for_prompt(mapping):
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in mapping.items():
        models_str = ", ".join(models)  # Limit to first 5 models for readability
        formatted_lines.append(f"  {lang}: [{models_str}]")
    
    return "\n".join(formatted_lines)

def generate_questions_for_task_scenario2(task_folder_path, num_questions=20):
    """Generate scenario 2 questions for a specific task using difference mapping."""
    task_name, difference_mapping = compute_difference_mapping(task_folder_path)
    
    if not task_name or not difference_mapping:
        return None
    
    if not difference_mapping:
        print(f"No missing evaluations found for {task_name}")
        return None
    
    # Clean up task name for better readability
    clean_task_name = task_name.replace("_", " ").replace("01 ", "").replace("02 ", "").replace("03 ", "").replace("04 ", "").replace("05 ", "").replace("06 ", "")
    
    # Format mapping for prompt
    # formatted_mapping = format_mapping_for_prompt(difference_mapping)
    formatted_mapping = difference_mapping

    # Generate questions using the LLM
    print("generating scenario 2 questions for the following parameters: ")
    print(f"  Task Name: {clean_task_name}")
    print(f"  Missing Evaluation Mappings:\n{formatted_mapping}")
    print(f"  Number of Questions: {num_questions}")
    
    prompt = prompt_scenario2_mapping.format(
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


def save_questions_to_file(questions, task_name, output_dir="generated_questions"):
    """Save generated questions to a JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{task_name}_questions_scenario2.json")
    
    # Convert to dict for JSON serialization
    questions_dict = {
        "task": task_name,
        "scenario": "GT_not_available",
        "questions": [q.model_dump() for q in questions.questions]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(questions.questions)} questions to {output_file}")


def process_all_tasks_scenario2(base_path=r"./all_final_csvs_finall", num_questions_per_task=60):
    """Process all task folders and generate scenario 2 questions for each."""
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
        print(f"\nProcessing {folder} for scenario 2...")
        
        questions = generate_questions_for_task_scenario2(folder_path, num_questions_per_task)
        
        if questions:
            save_questions_to_file(questions, folder)
            all_results[folder] = len(questions.questions)
            print(f"Generated {len(questions.questions)} questions for {folder}")
        else:
            print(f"Failed to generate questions for {folder}")
    
    # Print summary
    print(f"\n" + "="*60)
    print("SCENARIO 2 QUESTION GENERATION SUMMARY")
    print("="*60)
    total_questions = sum(all_results.values())
    print(f"Total tasks processed: {len(all_results)}")
    print(f"Total questions generated: {total_questions}")
    
    for task, count in all_results.items():
        print(f"  {task}: {count} questions")


if __name__ == "__main__":
    # Process all tasks in the all_final_csvs_finall folder for scenario 2
    process_all_tasks_scenario2()
    
    # Alternative: Process a single task
    # questions = generate_questions_for_task_scenario2("all_final_csvs_finall/01_Code_Generation")
    # if questions:
    #     save_questions_to_file(questions, "01_Code_Generation")