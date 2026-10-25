"""
Filtered MAE evaluator — runs MAE/accuracy evaluation for litmus_reagent
using ONLY the questions that appear in ablation runs.

This enables apples-to-apples comparison between ablation results and
the full Litmus Reagent on the exact same question set.

Usage (from repo root):
  python -m final_testing_codes.GET_GTS_FINAL.mae_accuracy_evaluation.run_filtered_reagent_eval --ablation no_coder
  python -m final_testing_codes.GET_GTS_FINAL.mae_accuracy_evaluation.run_filtered_reagent_eval --ablation no_expert_knowledge
"""
import json
import argparse
from pathlib import Path
from .data_loader import load_ground_truths
from .predictive_evaluator import evaluate_predictive_questions
from .qna_evaluator import evaluate_qna_questions
from .reporter import generate_report

BASE_DIR = Path(__file__).parent.parent
ROOT_DIR = BASE_DIR.parent.parent
GROUND_TRUTH_DIR = BASE_DIR / "Ground_truths_5"
REAGENT_PREDICTIONS_DIR = BASE_DIR / "final_results" / "litmus_reagent_1_responses"
ABLATION_RESPONSES_BASE = ROOT_DIR / "final_testing_codes" / "ABLATION_RUNS"

ABLATION_CONFIGS = {
    "no_coder": {
        "responses_dir": ABLATION_RESPONSES_BASE / "no_coder",
        "output_dir": BASE_DIR / "mae_accuracy_results_final" / "litmus_reagent_filtered_no_coder_questions",
    },
    "no_expert_knowledge": {
        "responses_dir": ABLATION_RESPONSES_BASE / "no_expert_knowledge",
        "output_dir": BASE_DIR / "mae_accuracy_results_final" / "litmus_reagent_filtered_no_expert_knowledge_questions",
    },
}


def get_ablation_question_ids(responses_dir: Path) -> set:
    """Collect unique_ids from ablation response folders (only questions actually run).
    
    Scans: {responses_dir}/{task}/Scenario_{N}/{uuid}/response.md
    """
    uids = set()
    for task_dir in responses_dir.iterdir():
        if not task_dir.is_dir():
            continue
        for scenario_dir in task_dir.iterdir():
            if not scenario_dir.is_dir():
                continue
            for uuid_dir in scenario_dir.iterdir():
                if uuid_dir.is_dir() and (uuid_dir / "response.md").exists():
                    uids.add(uuid_dir.name)
    return uids


def load_filtered_predictions(reagent_dir: Path, allowed_uids: set) -> dict:
    """Load reagent predictions filtered to only allowed unique_ids."""
    predictions = {}
    for pred_file in reagent_dir.glob("*.json"):
        try:
            with open(pred_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            filename = pred_file.stem
            task_num = filename.split('_')[0]
            scenario_num = filename.split('_scenario_')[1].split('_')[0]

            for item in data:
                unique_id = item.get('unique_id')
                if unique_id and unique_id in allowed_uids:
                    item['task_num'] = task_num
                    item['scenario_num'] = scenario_num
                    predictions[unique_id] = item
        except Exception as e:
            print(f"Error loading {pred_file}: {e}")
    return predictions


def load_filtered_ground_truths(gt_dir: Path, allowed_uids: set) -> dict:
    """Load ground truths filtered to only allowed unique_ids."""
    ground_truths = {}
    for gt_file in gt_dir.glob("*.json"):
        try:
            with open(gt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            filename = gt_file.stem
            task_num = filename.split('_')[0]
            scenario_num = filename.split('_scenario_')[1].split('_')[0]

            for item in data:
                unique_id = item.get('unique_id')
                if unique_id and unique_id in allowed_uids:
                    item['task_num'] = task_num
                    item['scenario_num'] = scenario_num
                    ground_truths[unique_id] = item
        except Exception as e:
            print(f"Error loading {gt_file}: {e}")
    return ground_truths


def run_evaluation(ablation_name: str):
    cfg = ABLATION_CONFIGS[ablation_name]
    responses_dir = cfg["responses_dir"]
    output_dir = cfg["output_dir"]

    print("=" * 80)
    print(f"LITMUS REAGENT MAE (filtered to {ablation_name} questions)")
    print("=" * 80)

    # Step 1: Get ablation question IDs from actual response folders
    print(f"\nCollecting question IDs from ablation responses: {responses_dir}...")
    allowed_uids = get_ablation_question_ids(responses_dir)
    print(f"  {len(allowed_uids)} unique question IDs actually run in ablation")

    # Step 2: Load filtered ground truths
    print("Loading filtered ground truths...")
    ground_truths = load_filtered_ground_truths(GROUND_TRUTH_DIR, allowed_uids)
    print(f"  {len(ground_truths)} ground truth entries (filtered)")

    # Step 3: Load filtered reagent predictions
    print("Loading filtered litmus_reagent predictions...")
    predictions = load_filtered_predictions(REAGENT_PREDICTIONS_DIR, allowed_uids)
    print(f"  {len(predictions)} prediction entries (filtered)")

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

    # Evaluate
    print("Evaluating predictive questions (MAE)...")
    mae_results = evaluate_predictive_questions(ground_truths, predictions)
    print(f"  Evaluated {len(mae_results)} predictive questions\n")

    print("Evaluating QnA questions (Accuracy)...")
    try:
        qna_results = evaluate_qna_questions(ground_truths, predictions)
        print(f"  Evaluated {len(qna_results)} QnA questions\n")
    except Exception as e:
        print(f"  QnA evaluation skipped due to error: {e}\n")
        qna_results = []

    print("Generating evaluation report...")
    generate_report(mae_results, qna_results, output_dir)
    print()

    print("=" * 80)
    print(f"Done — results in: {output_dir}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Run MAE evaluation for litmus_reagent filtered to ablation question set')
    parser.add_argument('--ablation', type=str, required=True,
                        choices=list(ABLATION_CONFIGS.keys()),
                        help='Which ablation question set to filter by')
    args = parser.parse_args()
    run_evaluation(args.ablation)


if __name__ == "__main__":
    main()
