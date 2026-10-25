import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response
from pydantic import BaseModel
import importlib.util
import json
from pathlib import Path

from language_mapping import SIMILAR_LANGUAGES_MAPPING

class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str
        languages: str

    questions: list[Question]



prompt_scenario5_mapping = """
You are given a language-to-models mapping for a specific NLP task where both the language AND the model are NOT available in the system's accessible data.

Task: {task_name}
Language-Model Mappings: {mappings}

This is **Scenario 5: Different Language, Different Model (Both Unavailable)**
The mappings show language-model combinations where:
- The language is NOT available in the accessible data (Lav)
- The model is also NOT available for ANY language in the accessible data
- These combinations exist only in the ground truth (Lgt) but not in Lav

### Goal

Generate natural, varied evaluation questions for this task focusing on scenarios where we need to evaluate performance but have NO direct data for either the language or the model.

Generate questions of the following types:

1. **Zero-Shot Evaluation**: Questions about evaluating without any available data
2. **Model-Language Gap**: Questions about missing model support for specific languages
3. **Resource Limitation**: Questions about working with completely unavailable combinations
4. **Transfer Feasibility**: Questions about whether transfer is even possible
5. **Alternative Approaches**: Questions about finding workarounds for missing data

### Question Templates (adapt and vary phrasing):

1. *How can we estimate {{model}} performance on {{language}} when neither is available in our data?*
2. *What is the expected performance of {{model}} for {{task}} in {{language}}?*
3. *Can we evaluate {{model}} on {{language}} without any direct benchmark data?*
4. *What approaches exist for assessing {{task}} performance in {{language}} using {{model}}?*
5. *How would {{model}} handle {{task}} for {{language}} based on related benchmarks?*
6. *What is the gap in coverage for {{model}} on {{language}} in {{task}}?*
7. *Are there any benchmarks for {{model}} performance on {{language}} for {{task}}?*
8. *How reliable would estimates be for {{model}} on {{language}} given no direct data?*
9. *What challenges exist in evaluating {{model}} for {{language}} in {{task}}?*
10. *Can cross-lingual methods help evaluate {{model}} on {{language}} for {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. For tasks like code generation, programming languages might be present as well. DO NOT generate questions for programming languages.
2. Use the exact task name provided
3. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
4. If task, model, or language is not present in a question, set it as `""` in the output
5. Questions must be clear, end with `?`, and avoid hallucinations
6. Generate diverse questions - avoid repetitive phrasing
7. Focus on scenarios where BOTH language AND model are unavailable

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


def compute_scenario5_mapping(task_folder_path):
    """
    Compute scenario 5 mapping: different language AND different model (both unavailable).
    
    CORRECTED Logic:
    1. Lgap = Lgt - Lav (languages in ground truth but not available)
    2. Get ALL models available in Lav (across ALL languages)
    3. For each language in Lgap:
       - Get models for that language from Lgt (ground truth)
       - EXCLUDE models that are available in Lav (for ANY language)
       - The remaining models are truly "different" - not available in Lav at all
    
    This ensures both the language AND the model are NOT in Lav.
    """
    task_name = os.path.basename(task_folder_path).lower()
    
    # Paths to the mapping files
    combined_file = os.path.join(task_folder_path, f"{task_name}_language_models_mapping.py")
    reduced_file = os.path.join(task_folder_path, f"reduced_{task_name}_language_models_mapping.py")
    
    # Load both mappings
    combined_mapping = load_mapping_file(combined_file)  # Ground truth (Lgt)
    reduced_mapping = load_mapping_file(reduced_file)    # Available (Lav)
    
    if not combined_mapping or not reduced_mapping:
        return None, None
    
    # Step 1: Compute Lgap = Lgt - Lav (languages in ground truth but not available)
    lgt_languages = set(combined_mapping.keys())
    lav_languages = set(reduced_mapping.keys())
    lgap_languages = lgt_languages - lav_languages
    
    # Step 2: Get ALL models available in Lav (across ALL languages)
    all_lav_models = set()
    for lang in lav_languages:
        all_lav_models.update(reduced_mapping[lang])
    
    print(f"Task: {task_name}")
    print(f"Ground truth languages (Lgt): {len(lgt_languages)}")
    print(f"Available languages (Lav): {len(lav_languages)}")
    print(f"Gap languages (Lgap): {len(lgap_languages)}")
    print(f"All models in Lav (across all languages): {len(all_lav_models)}")
    
    # Step 3: For each language in Lgap, find models that are NOT in Lav (for any language)
    scenario5_mapping = {}
    
    for gap_language in lgap_languages:
        # Get models that exist for this gap language in ground truth
        gap_language_models = set(combined_mapping[gap_language])
        
        # CRITICAL: Find models that are in Lgt for this language but NOT in Lav at all
        # This ensures BOTH language AND model are unavailable in Lav
        different_models = gap_language_models - all_lav_models
        
        if different_models:
            scenario5_mapping[gap_language] = sorted(list(different_models))
            print(f"  {gap_language}: {len(different_models)} models (both lang and model not in Lav)")
    
    print(f"\nTotal gap languages with different models: {len(scenario5_mapping)}")
    
    return task_name, scenario5_mapping


def format_mapping_for_prompt(mapping):
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in mapping.items():
        models_str = ", ".join(models)
        formatted_lines.append(f"  {lang}: [{models_str}]")
    
    return "\n".join(formatted_lines)


def generate_questions_for_task_scenario5(task_folder_path, num_questions=50):
    """Generate scenario 5 questions for a specific task using different language + different model mapping."""
    task_name, scenario5_mapping = compute_scenario5_mapping(task_folder_path)
    
    if not task_name or not scenario5_mapping:
        return None
    
    if not scenario5_mapping:
        print(f"No different language + different model mappings found for {task_name}")
        return None
    
    # Clean up task name for better readability
    clean_task_name = task_name.replace("_", " ").replace("01 ", "").replace("02 ", "").replace("03 ", "").replace("04 ", "").replace("05 ", "").replace("06 ", "")
    
    # Format mapping for prompt
    formatted_mapping = format_mapping_for_prompt(scenario5_mapping)
    
    # Generate questions using the LLM
    print("\nGenerating scenario 5 questions for the following parameters: ")
    print(f"  Task Name: {clean_task_name}")
    print(f"  Different Language + Different Model Mappings:\n{formatted_mapping}")
    print(f"  Number of Questions: {num_questions}")
    
    prompt = prompt_scenario5_mapping.format(
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
    
    output_file = os.path.join(output_dir, f"{task_name}_questions_scenario5.json")
    
    # Convert to dict for JSON serialization
    questions_dict = {
        "task": task_name,
        "scenario": "different_language_different_model_both_unavailable",
        "questions": [q.model_dump() for q in questions.questions]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(questions.questions)} questions to {output_file}")


def process_all_tasks_scenario5(base_path=r"./all_final_csvs_finall", num_questions_per_task=50):
    """Process all task folders and generate scenario 5 questions for each."""
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
        print(f"\n{'='*60}")
        print(f"Processing {folder} for scenario 5...")
        print('='*60)
        
        questions = generate_questions_for_task_scenario5(folder_path, num_questions_per_task)
        
        if questions:
            save_questions_to_file(questions, folder)
            all_results[folder] = len(questions.questions)
            print(f"Generated {len(questions.questions)} questions for {folder}")
        else:
            print(f"Failed to generate questions for {folder}")
    
    # Print summary
    print(f"\n" + "="*60)
    print("SCENARIO 5 QUESTION GENERATION SUMMARY")
    print("="*60)
    total_questions = sum(all_results.values())
    print(f"Total tasks processed: {len(all_results)}")
    print(f"Total questions generated: {total_questions}")
    
    for task, count in all_results.items():
        print(f"  {task}: {count} questions")


if __name__ == "__main__":
    # Process all tasks in the all_final_csvs_finall folder for scenario 5
    process_all_tasks_scenario5()
    
    # Alternative: Process a single task
    # questions = generate_questions_for_task_scenario5("all_final_csvs_finall/01_Code_Generation")
    # if questions:
    #     save_questions_to_file(questions, "01_Code_Generation")
