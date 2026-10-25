"""
Configuration file for Evaluation Performance Metrics V2
Contains all directory paths and constants
"""
from pathlib import Path

# Base directories
ROOT_DIR = Path(r"./")

# Input directories
GENERATED_QUESTIONS_DIR = ROOT_DIR / "generated_questions"

# Evaluation results directories to search for response.md files
EVALUATION_RESULTS_DIRECTORIES = [
    # ROOT_DIR / "final_testing_codes" / "task_scenario_new_final_2_responses",
    # ROOT_DIR / "final_testing_codes" / "task_scenario_thoguht_new_final_1_1_responses"
    # ROOT_DIR / "magnetic_one_results_ijcai_restructured_combined_new"
    # ROOT_DIR / "final_testing_codes" / "gpt4_baseline_responses"
    # ROOT_DIR / "final_testing_codes" / "FINAL_RUS" / "litmus_plus_plus_orig_1_responses"
    # --- ABLATION RUNS (use run_ablation_extraction.py, these use Scenario_N not ScenarioPair_N) ---
    ROOT_DIR / "final_testing_codes" / "ABLATION_RUNS" / "no_coder"
    # ROOT_DIR / "final_testing_codes" / "ABLATION_RUNS" / "no_expert_knowledge"
]

# Output directory for predictions
# OUTPUT_DIR = ROOT_DIR / "final_testing_codes" / "GET_GTS_FINAL" / "final_results" / "litmus_plus_plus_orig_1_responses"
OUTPUT_DIR = ROOT_DIR / "final_testing_codes" / "GET_GTS_FINAL" / "final_results" / "ablation_no_coder"
# OUTPUT_DIR = ROOT_DIR / "final_testing_codes" / "GET_GTS_FINAL" / "final_results" / "ablation_no_expert_knowledge"

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

# Scenario-to-ScenarioPair mapping
# Maps scenario numbers to their corresponding ScenarioPair folder
SCENARIO_TO_PAIR_MAPPING = {
    1: 1,  # Scenario 1 -> ScenarioPair_1
    2: 1,  # Scenario 2 -> ScenarioPair_1
    3: 1,  # Scenario 3 -> ScenarioPair_2
    4: 1,  # Scenario 4 -> ScenarioPair_2
    5: 1   # Scenario 5 -> ScenarioPair_2
}

# Report file name (response.md contains the agent's report)
REPORT_FILE_NAME = "response.md"
