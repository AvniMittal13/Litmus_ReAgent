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
You are given a language-to-models mapping for a specific NLP task where different models are available for different languages than the target language.

Task: {task_name}
Language-Model Mappings: {mappings}

This is **Scenario 5: Different Language, Different Model Available**
The mappings show language-model combinations where:
- The target language is NOT available in the training/evaluation data
- The specific model that could work for the target language is also NOT available
- Different models are available for similar/distant languages that could potentially transfer

### Goal

Generate natural, varied evaluation questions for this task focusing on cross-lingual transfer scenarios where both the target language AND the ideal model are unavailable, requiring transfer from different languages using different models.

Generate questions of the following types:

1. **Cross-lingual Transfer**: Questions about transferring from one language-model to another language
2. **Model Adaptation**: Questions about adapting different models for new languages  
3. **Language Coverage Gaps**: Questions about missing language support and alternatives
4. **Transfer Learning**: Questions about how different models perform when transferred across languages
5. **Resource Constraints**: Questions about working with limited language-model combinations

### Question Templates (adapt and vary phrasing):

1. *How would {{model}} trained on {{language1}} perform when transferred to {{target_language}}?*
2. *What alternatives exist for {{task}} in {{target_language}} when {{ideal_model}} is not available?*
3. *Can {{model}} be adapted from {{source_language}} to handle {{target_language}} for {{task}}?*
4. *Which available language-model combination could best substitute for missing {{target_language}} support?*
5. *How effective is cross-lingual transfer from {{model}} on {{source_language}} to {{target_language}}?*
6. *What is the performance gap when using {{model}} instead of native {{target_language}} models for {{task}}?*
7. *How do different models compare for zero-shot transfer to {{target_language}} in {{task}}?*
8. *Which similar language could provide the best transfer learning base for {{target_language}}?*
9. *What challenges arise when {{model}} trained on {{source_language}} is applied to {{target_language}}?*
10. *How can we evaluate {{task}} performance for {{target_language}} without direct language support?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. for tasks like code generation, programming languages might be present as well. DONOT generate questions for programming languages
2. Use the exact task name provided
3. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
4. If task, model, or language is not present in a question, set it as `""` in the output
5. Questions must be clear, end with `?`, and avoid hallucinations
6. Generate diverse questions - avoid repetitive phrasing
7. Focus on realistic cross-lingual and cross-model transfer scenarios

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


def get_all_similar_and_related_languages(language):
    """Get all similar and related languages for a given language."""
    similar_langs = set(SIMILAR_LANGUAGES_MAPPING.get(language, []))
    
    # Also check if the language appears as a similar language for others
    for lang, similar_list in SIMILAR_LANGUAGES_MAPPING.items():
        if language in similar_list:
            similar_langs.add(lang)
            similar_langs.update(similar_list)
    
    # Remove the original language itself
    similar_langs.discard(language)
    return list(similar_langs)


def compute_scenario5_mapping(task_folder_path):
    """
    Compute scenario 5 mapping: different language, different model available.
    
    Logic:
    1. Lgap = Lgt - Lav (languages in ground truth but not available)
    2. For each language in Lgap:
       - Find similar/distant languages that are available 
       - Find models available for those languages
       - EXCLUDE models that exist for the gap language in ground truth
       - Only include language-model pairs where both language AND model are different
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
    
    # Step 2: For each language in Lgap, find different language + different model combinations
    scenario5_mapping = {}
    
    for gap_language in lgap_languages:
        # Get models that exist for this gap language in ground truth
        gap_language_models = set(combined_mapping[gap_language])
        
        # Get similar/related languages for this gap language
        related_languages = get_all_similar_and_related_languages(gap_language)
        
        # Find which related languages are available in the reduced mapping
        available_related_languages = [lang for lang in related_languages if lang in reduced_mapping]
        
        # If no related languages available, try all available languages (distant transfer)
        if not available_related_languages:
            available_related_languages = list(lav_languages)
        
        # Collect models available for related/distant languages
        available_models_for_related = set()
        for rel_lang in available_related_languages:
            available_models_for_related.update(reduced_mapping[rel_lang])
        
        # CRITICAL: Exclude models that exist for the gap language in ground truth
        # This ensures we have "different model" constraint
        different_models = available_models_for_related - gap_language_models
        
        if different_models:
            scenario5_mapping[gap_language] = sorted(list(different_models))
            if available_related_languages:
                relation_type = "similar/related" if any(lang in related_languages for lang in available_related_languages[:3]) else "distant"
                print(f"  {gap_language}: {len(different_models)} different models via {relation_type} languages")
            else:
                print(f"  {gap_language}: {len(different_models)} different models via distant languages")
    
    return task_name, scenario5_mapping


def format_mapping_for_prompt(mapping):
    """Format the mapping dictionary for the prompt."""
    formatted_lines = []
    for lang, models in mapping.items():
        models_str = ", ".join(models)  # Limit to first 5 models for readability
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
    print("generating scenario 5 questions for the following parameters: ")
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
        "scenario": "different_language_different_model_available",
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
        print(f"\nProcessing {folder} for scenario 5...")
        
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