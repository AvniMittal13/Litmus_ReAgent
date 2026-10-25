"""
Configuration file for Ground Truth Generator V2
Contains all directory paths and constants
"""
from pathlib import Path

# Base directories
ROOT_DIR = Path(r"./")

# Input directories
GENERATED_QUESTIONS_DIR = ROOT_DIR / "generated_questions"

# Response directories to search for query_id folders
RESPONSE_DIRECTORIES = [
    # ROOT_DIR / "final_testing_codes" / "task_scenario_new_final_1_responses_combined",
    ROOT_DIR / "final_testing_codes" / "task_scenario_new_final_2_responses",
    # ROOT_DIR / "final_testing_codes" / "task_scenario_thoguht_new_final_1_1_responses"
]

# Cache file path
QUERY_CACHE_PATH = ROOT_DIR / "query_cache.pkl"

# Output directory
OUTPUT_DIR = ROOT_DIR / "final_testing_codes" / "GET_GTS_FINAL" / "Ground_truths_5"

# Task names
TASKS = [
    "01_Code_Generation",
    "02_Math_Reasoning",
    "03_QA_VQA",
    "04_Classification_NLI",
    "05_Text_Summarization",
    "06_Machine_Translation"
]

# Number of scenarios per task
NUM_SCENARIOS = 5

# Intermediate file patterns
INTERMEDIATE_FILE_PATTERNS = [
    "*_intermediates.json",  # For combined/new responses
    "agent_intermediates.json"  # For thought responses
]

# Reprocessing mode settings
USE_ACTIVE_DB_SEARCH = True  # Call actual db_search on cache miss
EXISTING_OUTPUT_DIR = ROOT_DIR / "final_testing_codes" / "GET_GTS_FINAL" / "Ground_truths_1"

# Task to combined pkl database mapping
# Folder: 01_Code_Generation -> PKL: combined_01_code_generation_embeddings.pkl
TASK_DB_MAPPINGS = {
    "01_Code_Generation": ("01_Code_Generation", "combined_01_code_generation_embeddings.pkl"),
    "02_Math_Reasoning": ("02_Math_Reasoning", "combined_02_math_reasoning_embeddings.pkl"),
    "03_QA_VQA": ("03_QA_VQA", "combined_03_qa_vqa_embeddings.pkl"),
    "04_Classification_NLI": ("04_Classification_NLI", "combined_04_classification_nli_embeddings.pkl"),
    "05_Text_Summarization": ("05_Text_Summarization", "combined_05_text_summarization_embeddings.pkl"),
    "06_Machine_Translation": ("06_Machine_Translation", "combined_06_machine_translation_embeddings.pkl")
}

def get_combined_db_path(task: str) -> Path:
    """Get path to combined pkl database for a task."""
    if task not in TASK_DB_MAPPINGS:
        print(f"Warning: Unknown task '{task}'")
        return None
    
    folder, pkl_file = TASK_DB_MAPPINGS[task]
    db_path = ROOT_DIR / "all_final_csvs_finall" / folder / pkl_file
    
    if db_path.exists():
        return db_path
    else:
        print(f"Warning: DB file not found: {db_path}")
        return None
