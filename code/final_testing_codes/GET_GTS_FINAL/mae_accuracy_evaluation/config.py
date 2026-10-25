"""Configuration for MAE and Accuracy Evaluation"""
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
GROUND_TRUTH_DIR = BASE_DIR / "Ground_truths_5"
PREDICTIONS_DIR = BASE_DIR / "final_results" / "magnetic_one_1_responses"
OUTPUT_DIR = BASE_DIR / "mae_accuracy_results_final" / "magnetic_one_1_responses_final"
# --- ABLATION: no_coder ---
# PREDICTIONS_DIR = BASE_DIR / "final_results" / "ablation_no_coder"
# OUTPUT_DIR = BASE_DIR / "mae_accuracy_results_final" / "ablation_no_coder_final"
# --- ABLATION: no_expert_knowledge ---
# PREDICTIONS_DIR = BASE_DIR / "final_results" / "ablation_no_expert_knowledge"
# OUTPUT_DIR = BASE_DIR / "mae_accuracy_results_final" / "ablation_no_expert_knowledge_final"

# Metric equivalence mapping (normalized form -> list of variations)
METRIC_EQUIVALENTS = {
    "accuracy": ["pass@1", "acc", "pass@k", "passk", "pass_at_1"],
    "f1": ["f1-score", "f1_score", "f1score"],
    "bleu": ["bleu-4", "bleu4", "bleu_score"],
    "rouge": ["rouge-l", "rougel", "rouge_l"],
    "exact_match": ["em", "exact-match"],
    "precision": ["prec"],
    "recall": ["rec"],
}

# Task names for reporting
TASK_NAMES = {
    "01": "Code_Generation",
    "02": "Math_Reasoning",
    "03": "QA_VQA",
    "04": "Classification_NLI",
    "05": "Text_Summarization",
    "06": "Machine_Translation"
}

# Scenario names
SCENARIO_NAMES = {
    "1": "GT_available",
    "2": "Context_available",
    "3": "Baseline_comparison",
    "4": "Performance_analysis",
    "5": "Cross_lingual_evaluation"
}
