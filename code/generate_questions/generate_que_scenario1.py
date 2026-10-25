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


# prompt_scenario1_mapping = """
# You are given a language-to-models mapping for a specific NLP task where ground truth (GT) data is available.

# Task: {task_name}
# Language-Model Mappings: {mappings}

# The mappings show which models have been benchmarked on which languages for this task.
# Each language maps to a list of models that have been evaluated on it.

# ### Goal

# Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
# Generate questions of the following types:

# 1. **Task + Model + Language**: Questions about specific model performance on specific language
# 2. **Task + Language**: Questions about how different models perform on a specific language  
# 3. **Task + Model**: Questions about how a specific model performs across languages
# 4. **Model + Language**: Questions about model performance on language (task implied)
# 5. **Task only**: Questions about overall task performance across languages/models

# ### Question Templates (adapt and vary phrasing):

# 1. *What is the performance of {{model}} on {{task}} for {{language}}?*
# 2. *How does {{model}} perform on {{task}} in {{language}}?*
# 3. *Compare {{model1}} and {{model2}} performance for {{language}} on {{task}} and tell which one is better*
# 4. *Which model performs best for {{task}} in {{language}}?*
# 7. *Which languages has the best performance for {{task}} for model {{model}}?*
# 8. *Which is the best performing model for {{task}} in {{language}}?*

# ### Rules

# 1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. for tasks like code generation, programming languages might be present as well. DONOT generate questions for programming languages
# 2. Use the exact task name provided
# 3. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
# 4. If task, model, or language is not present in a question, set it as `""` in the output
# 5. Questions must be clear, end with `?`, and avoid hallucinations. Use ONLY the information provided in the mapping. Assume ground truth is available for the provided data.
# 6. Generate diverse questions - avoid repetitive phrasing
# 7. Focus on realistic evaluation scenarios where GT data would be available

# ### Output Format

# Return **only JSON** in this structure:

prompt_scenario1_improved = """
You are given a language-to-models mapping for a specific NLP task where ground truth benchmark data is available.

Task: {task_name}
Language-Model Mappings: {mappings}

### Goal

Generate benchmark evaluation questions that have **EXACT, SINGULAR answers** from the ground truth data.
Focus on **low-resource languages** when available in the mapping.

### Question Categories

#### Category 1: PREDICTIVE Questions (Numerical Answer)
Questions where the answer is ONE numerical score/value.

Templates:
- "What is the performance of {{model}} on {{task}} for {{language}}?"
- "What score does {{model}} achieve for {{task}} in {{language}}?"
- "How well does {{model}} perform on {{task}} for {{language}}?"

Examples:
- "What is the performance of GPT-4 on Code Generation for Hindi?"
- "What score does LLaMA-3 achieve for Machine Translation in Bengali?"

#### Category 2: QnA Questions (Single Categorical Answer)  
Questions where the answer is ONE exact model name or language name.

Templates:
- "Which model performs best for {{task}} in {{language}}?"
- "What is the top-performing model for {{task}} in {{language}}?"
- "For {{task}}, which language shows the best performance with {{model}}?"
- "Which model achieves the highest score for {{task}} in {{language}}?"

Examples:
- "Which model performs best for Code Generation in Hindi?"
- "Which language has the best performance for Math Reasoning with LLaMA-3?"

### Rules

1. **ONLY use languages and models from the provided mapping** - no invented data
2. **EXCLUDE programming languages** - only natural languages (Hindi, French, Bengali, etc.)
3. **Prioritize low-resource languages** when available over high-resource ones (e.g., prefer Hindi, Swahili, Bengali over English)
4. **Each question must have exactly ONE answer** - no comparisons or lists
5. **DO NOT specify metrics** in the question (no "accuracy", "F1", "BLEU", etc.)
6. Use exact task name provided
7. If multiple models/languages, list alphabetically comma-separated
8. Set empty string "" for missing fields
9. **Avoid questions like**:
   - "Compare X and Y" (multiple answers)
   - "What are the performances across..." (multiple values)
   - "List all models that..." (list answer)

### Output Distribution
- Generate approximately {num_predictive} PREDICTIVE questions
- Generate approximately {num_qna} QnA questions

### Output Format

Return **only JSON**:

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
    # mapping_file = os.path.join(task_folder_path, f"{task_name}_language_models_mapping.py")
    mapping_file = os.path.join(task_folder_path, f"reduced_{task_name}_language_models_mapping.py")

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
        models_str = ", ".join(models)  # Limit to first 5 models for readability
        formatted_lines.append(f"  {lang}: [{models_str}]")
    
    return "\n".join(formatted_lines)


def generate_questions_for_task(task_folder_path, num_questions=50):
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


def save_questions_to_file(questions, task_name, output_dir="generated_questions"):
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


def process_all_tasks(base_path=r"./all_final_csvs_finall", num_questions_per_task=60):
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