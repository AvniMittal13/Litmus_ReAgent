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


prompt_scenario4_mapping = """
You are given a language-to-models mapping for a specific NLP task where distant language transfer is needed.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show which models can potentially be evaluated on which languages using distant language transfer.
Each language maps to a list of models that could be evaluated on it using distant (non-similar) language benchmarks.

### Goal

Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
These questions should focus on distant cross-lingual transfer scenarios where similar languages are NOT available.
Generate questions of the following types:

1. **Task + Model + Language**: Questions about model performance on specific language using distant language transfer
2. **Task + Language**: Questions about how different models perform on a specific language via distant transfer
3. **Model + Language**: Questions about model performance on language using distant transfer (task implied)

### Question Templates (adapt and vary phrasing):

1. *How would {{model}} perform on {{task}} for {{language}} using distant language transfer?*
2. *Can {{model}} transfer {{task}} performance from distant languages to {{language}}?*
3. *What is the distant cross-lingual performance of {{model}} on {{task}} for {{language}}?*
4. *How does {{language}} {{task}} performance compare using distant language transfer?*
5. *Which models show best distant cross-lingual transfer for {{task}} to {{language}}?*
6. *Can distant language data help evaluate {{task}} performance in {{language}}?*
7. *How effective is distant cross-lingual transfer for {{task}} evaluation in {{language}}?*
8. *How does distant cross-lingual {{task}} evaluation work for low-resource {{language}}?*
9. *Which distant languages provide transfer capabilities for {{task}} in {{language}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. for tasks like code generation, programming languages might be present as well. DONOT generate questions for programming languages
2. Use the exact task name provided
3. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
4. If task, model, or language is not present in a question, set it as `""` in the output
5. Questions must be clear, end with `?`, and avoid hallucinations
6. Generate diverse questions - avoid repetitive phrasing
7. Focus on distant cross-lingual transfer scenarios where similar languages are NOT available

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


def get_similar_languages(language):
    """Get similar languages for a given language."""
    return SIMILAR_LANGUAGES_MAPPING.get(language, [])


def get_all_similar_and_related_languages(language):
    """Get all languages that are similar to or related to the given language."""
    similar_languages = set(get_similar_languages(language))
    
    # Add the language itself
    similar_languages.add(language)
    
    # Add languages for which this language is similar
    for lang, similar_list in SIMILAR_LANGUAGES_MAPPING.items():
        if language in similar_list:
            similar_languages.add(lang)
    
    return similar_languages


def compute_scenario4_mapping(task_folder_path):
    """
    Compute scenario 4 mapping: distant language + same model available.
    
    Logic:
    1. Lgap = Lgt - Lav (languages in ground truth but not available)
    2. For each language in Lgap:
       - Ensure NO similar languages are available (key constraint for scenario 4)
       - Find distant languages (all available languages minus similar ones)
       - Find models that are available for those distant languages
       - Include language-model pairs where distant language + same model is available
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
    
    print(f"Task: {task_name}")
    print(f"Ground truth languages (Lgt): {len(lgt_languages)}")
    print(f"Available languages (Lav): {len(lav_languages)}")
    print(f"Gap languages (Lgap): {len(lgap_languages)}")
    
    # Step 2: For each language in Lgap, check if similar languages are NOT available
    scenario4_mapping = {}
    
    for gap_language in lgap_languages:
        # Get all similar and related languages for this gap language
        similar_and_related = get_all_similar_and_related_languages(gap_language)
        
        # Check if any similar/related languages are available in the reduced mapping
        available_similar_languages = [lang for lang in similar_and_related if lang in reduced_mapping]
        
        # Key constraint for scenario 4: NO similar languages should be available
        if available_similar_languages:
            continue  # Skip this language as similar languages are available (this would be scenario 3)
        
        # Get all models from the ground truth for this gap language
        gap_language_models = set(combined_mapping[gap_language])
        
        # Find distant languages: all available languages that are NOT similar
        distant_languages = [lang for lang in lav_languages if lang not in similar_and_related]
        
        if not distant_languages:
            continue  # No distant languages available
        
        # Collect all models available for distant languages
        distant_language_models = set()
        for distant_lang in distant_languages:
            distant_language_models.update(reduced_mapping[distant_lang])
        
        # Find intersection: models that exist both in gap language (GT) and distant languages (available)
        common_models = gap_language_models.intersection(distant_language_models)
        
        if common_models:
            scenario4_mapping[gap_language] = sorted(list(common_models))
            print(f"  {gap_language}: {len(common_models)} models via distant languages (no similar langs available)")
    
    return task_name, scenario4_mapping


def format_mapping_for_prompt(mapping):
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in mapping.items():
        models_str = ", ".join(models)  # Limit to first 5 models for readability
        formatted_lines.append(f"  {lang}: [{models_str}]")
    
    return "\n".join(formatted_lines)


def generate_questions_for_task_scenario4(task_folder_path, num_questions=50):
    """Generate scenario 4 questions for a specific task using distant language mapping."""
    task_name, scenario4_mapping = compute_scenario4_mapping(task_folder_path)
    
    if not task_name or not scenario4_mapping:
        return None
    
    if not scenario4_mapping:
        print(f"No distant language mappings found for {task_name}")
        return None
    
    # Clean up task name for better readability
    clean_task_name = task_name.replace("_", " ").replace("01 ", "").replace("02 ", "").replace("03 ", "").replace("04 ", "").replace("05 ", "").replace("06 ", "")
    
    # Format mapping for prompt
    formatted_mapping = format_mapping_for_prompt(scenario4_mapping)
    
    # Generate questions using the LLM
    print("generating scenario 4 questions for the following parameters: ")
    print(f"  Task Name: {clean_task_name}")
    print(f"  Distant Language Transfer Mappings:\n{formatted_mapping}")
    print(f"  Number of Questions: {num_questions}")
    
    prompt = prompt_scenario4_mapping.format(
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
    
    output_file = os.path.join(output_dir, f"{task_name}_questions_scenario4.json")
    
    # Convert to dict for JSON serialization
    questions_dict = {
        "task": task_name,
        "scenario": "distant_language_available",
        "questions": [q.model_dump() for q in questions.questions]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(questions.questions)} questions to {output_file}")


def process_all_tasks_scenario4(base_path=r"./all_final_csvs_finall", num_questions_per_task=50):
    """Process all task folders and generate scenario 4 questions for each."""
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
        print(f"\nProcessing {folder} for scenario 4...")
        
        questions = generate_questions_for_task_scenario4(folder_path, num_questions_per_task)
        
        if questions:
            save_questions_to_file(questions, folder)
            all_results[folder] = len(questions.questions)
            print(f"Generated {len(questions.questions)} questions for {folder}")
        else:
            print(f"Failed to generate questions for {folder}")
    
    # Print summary
    print(f"\n" + "="*60)
    print("SCENARIO 4 QUESTION GENERATION SUMMARY")
    print("="*60)
    total_questions = sum(all_results.values())
    print(f"Total tasks processed: {len(all_results)}")
    print(f"Total questions generated: {total_questions}")
    
    for task, count in all_results.items():
        print(f"  {task}: {count} questions")


if __name__ == "__main__":
    # Process all tasks in the all_final_csvs_finall folder for scenario 4
    process_all_tasks_scenario4()
    
    # Alternative: Process a single task
    # questions = generate_questions_for_task_scenario4("all_final_csvs_finall/01_Code_Generation")
    # if questions:
    #     save_questions_to_file(questions, "01_Code_Generation")