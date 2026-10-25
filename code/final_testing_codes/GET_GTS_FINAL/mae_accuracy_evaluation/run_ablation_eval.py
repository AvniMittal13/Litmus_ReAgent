"""
Ablation MAE evaluator — runs MAE/accuracy evaluation for ablation predictions.

Reuses the existing evaluation pipeline but with ablation-specific paths.
Does NOT modify the existing config.py.

Usage (from repo root):
  python -m final_testing_codes.GET_GTS_FINAL.mae_accuracy_evaluation.run_ablation_eval --ablation no_coder
  python -m final_testing_codes.GET_GTS_FINAL.mae_accuracy_evaluation.run_ablation_eval --ablation no_expert_knowledge
"""
import argparse
from pathlib import Path
from .data_loader import load_ground_truths, load_predictions
from .predictive_evaluator import evaluate_predictive_questions
from .qna_evaluator import evaluate_qna_questions
from .reporter import generate_report

BASE_DIR = Path(__file__).parent.parent
GROUND_TRUTH_DIR = BASE_DIR / "Ground_truths_5"

ABLATION_CONFIGS = {
    "no_coder": {
        "predictions_dir": BASE_DIR / "final_results" / "ablation_no_coder",
        "output_dir": BASE_DIR / "mae_accuracy_results_final" / "ablation_no_coder_final",
    },
    "no_expert_knowledge": {
        "predictions_dir": BASE_DIR / "final_results" / "ablation_no_expert_knowledge",
        "output_dir": BASE_DIR / "mae_accuracy_results_final" / "ablation_no_expert_knowledge_final",
    },
}


def run_evaluation(ablation_name: str):
    cfg = ABLATION_CONFIGS[ablation_name]
    predictions_dir = cfg["predictions_dir"]
    output_dir = cfg["output_dir"]

    print("=" * 80)
    print(f"MAE AND ACCURACY EVALUATION — Ablation: {ablation_name}")
    print("=" * 80)
    print(f"Ground truths: {GROUND_TRUTH_DIR}")
    print(f"Predictions:   {predictions_dir}")
    print(f"Output:        {output_dir}")
    print()

    print("Loading ground truths...")
    ground_truths = load_ground_truths(GROUND_TRUTH_DIR)
    print(f"  Loaded {len(ground_truths)} ground truth entries")

    print("Loading predictions...")
    predictions = load_predictions(predictions_dir)
    print(f"  Loaded {len(predictions)} prediction entries")

    predictions_with_answers = sum(1 for p in predictions.values() if p.get('is_answer_present', False))
    print(f"  Predictions with answers: {predictions_with_answers}/{len(predictions)}")

    from collections import defaultdict
    coverage = defaultdict(lambda: {'total': 0, 'with_answers': 0})
    for pred_data in predictions.values():
        task_num = pred_data.get('task_num', 'unknown')
        scenario_num = pred_data.get('scenario_num', 'unknown')
        key = f"{task_num}_scenario_{scenario_num}"
        coverage[key]['total'] += 1
        if pred_data.get('is_answer_present', False):
            coverage[key]['with_answers'] += 1

    print("\n  Coverage by task-scenario:")
    for key in sorted(coverage.keys()):
        stats = coverage[key]
        print(f"    {key}: {stats['with_answers']}/{stats['total']} have answers")
    print()

    print("Evaluating predictive questions (MAE)...")
    mae_results = evaluate_predictive_questions(ground_truths, predictions)
    print(f"  Evaluated {len(mae_results)} predictive questions\n")

    print("Evaluating QnA questions (Accuracy)...")
    qna_results = evaluate_qna_questions(ground_truths, predictions)
    print(f"  Evaluated {len(qna_results)} QnA questions\n")

    print("Generating evaluation report...")
    generate_report(mae_results, qna_results, output_dir)
    print()

    print("=" * 80)
    print(f"Evaluation completed — results in: {output_dir}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Run MAE evaluation for ablation predictions')
    parser.add_argument('--ablation', type=str, required=True,
                        choices=list(ABLATION_CONFIGS.keys()),
                        help='Ablation name')
    args = parser.parse_args()
    run_evaluation(args.ablation)


if __name__ == "__main__":
    main()
