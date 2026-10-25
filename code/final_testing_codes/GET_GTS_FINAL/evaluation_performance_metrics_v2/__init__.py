"""
Evaluation Performance Metrics V2 Package

This package extracts predictions from agent evaluation reports (judge_result.json files)
and generates structured predictions matching the ground truth format for easy comparison.

Modules:
- config: Configuration for evaluation results directories and output paths
- query_loader: Load questions from generated_questions/ (reused from ground_truth_generator_v2)
- report_finder: Find judge_result.json files in evaluation results directories
- report_extractor: Extract original_report field from judge_result.json files
- prediction_generator: Generate predictions using LLM analysis of agent reports
- main: Orchestrate the prediction generation pipeline

Output:
- Predictions_1/{task}_scenario_{num}_predictions.json
  Structure matches Ground_truths_1/ for direct comparison

Usage:
    python -m evaluation_performance_metrics_v2.main                    # Process all tasks and scenarios
    python -m evaluation_performance_metrics_v2.main --task "01_Code_Generation"  # Single task
    python -m evaluation_performance_metrics_v2.main --task "01_Code_Generation" --scenario 1  # Single scenario
"""

__version__ = "2.0.0"
__all__ = [
    "config",
    "query_loader",
    "report_finder",
    "report_extractor",
    "prediction_generator",
    "main"
]
