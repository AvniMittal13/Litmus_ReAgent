"""
Ablation extraction script — extracts predictions from ablation run reports.

Ablation runs use a different folder structure than the main runs:
  Main runs:     {task}/ScenarioPair_{N}/{uuid}/response.md
  Ablation runs: {task}/Scenario_{N}/{uuid}/response.md

This script reuses the existing pipeline modules (query_loader, report_extractor,
prediction_generator) but overrides the report-finding logic for the ablation
folder structure.

Usage (from repo root):
  python -m final_testing_codes.GET_GTS_FINAL.evaluation_performance_metrics_v2.run_ablation_extraction --ablation no_coder
  python -m final_testing_codes.GET_GTS_FINAL.evaluation_performance_metrics_v2.run_ablation_extraction --ablation no_expert_knowledge
"""
import json
import argparse
from pathlib import Path
from typing import Dict, Optional

from .query_loader import load_questions
from .report_extractor import extract_all_reports
from .prediction_generator import generate_predictions_for_questions
from .config import ROOT_DIR, TASKS, NUM_SCENARIOS

# Ablation base directory
ABLATION_BASE = ROOT_DIR / "final_testing_codes" / "ABLATION_RUNS"

# Ablation configs: ablation_name -> { dir, tasks, scenarios }
ABLATION_CONFIGS = {
    "no_coder": {
        "responses_dir": ABLATION_BASE / "no_coder",
        "tasks": ["01_Code_Generation"],
        "scenarios": [1, 3, 5],
    },
    "no_expert_knowledge": {
        "responses_dir": ABLATION_BASE / "no_expert_knowledge",
        "tasks": ["01_Code_Generation"],
        "scenarios": [1, 3, 5],
    },
}


def find_report_file_ablation(responses_dir: Path, task: str, scenario_num: int, unique_id: str) -> Optional[Path]:
    """
    Find response.md for ablation folder layout: {task}/Scenario_{N}/{uuid}/response.md
    """
    report_file = responses_dir / task / f"Scenario_{scenario_num}" / unique_id / "response.md"
    if report_file.exists():
        return report_file
    return None


def find_all_reports_ablation(responses_dir: Path, task: str, scenario_num: int, questions: list) -> Dict[str, Optional[Path]]:
    """Find response.md files for all questions using ablation folder structure."""
    report_files = {}
    for question in questions:
        unique_id = question.get('unique_id')
        if not unique_id:
            continue
        report_file = find_report_file_ablation(responses_dir, task, scenario_num, unique_id)
        report_files[unique_id] = report_file
        if report_file is None:
            print(f"  Warning: No report for {unique_id}")

    found = sum(1 for p in report_files.values() if p is not None)
    print(f"  Found reports for {found}/{len(report_files)} questions")
    return report_files


def process_task_scenario(ablation_name: str, responses_dir: Path, output_dir: Path,
                          task_name: str, scenario_num: int, all_questions: dict) -> bool:
    """Process a single task-scenario for an ablation run."""
    key = f"{task_name}_scenario_{scenario_num}"
    print(f"\n{'='*60}")
    print(f"[{ablation_name}] Processing: {key}")
    print(f"{'='*60}")

    if key not in all_questions:
        print(f"  No questions found for {key}, skipping.")
        return False

    questions = all_questions[key]
    print(f"  {len(questions)} questions loaded")

    # Load existing predictions to support resume
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{key}_predictions.json"

    existing_predictions = {}
    if output_file.exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_list = json.load(f)
            for item in existing_list:
                uid = item.get('unique_id', '')
                has_pred = bool(item.get('predicted_metrics_and_values_for_predictive'))
                has_ans = bool(item.get('answer_text_for_qna'))
                if has_pred or has_ans:
                    existing_predictions[uid] = item
            print(f"  {len(existing_predictions)} existing predictions found (resuming)")
        except Exception as e:
            print(f"  Warning: Could not load existing: {e}")

    questions_to_process = [q for q in questions if q.get('unique_id', '') not in existing_predictions]
    print(f"  Need to process: {len(questions_to_process)} (skipping {len(questions) - len(questions_to_process)})")

    if not questions_to_process:
        print("  All done, skipping.")
        return True

    # Step 1: Find response.md files (ablation path structure)
    print("  Step 1: Finding response.md files...")
    report_files = find_all_reports_ablation(responses_dir, task_name, scenario_num, questions_to_process)

    # Step 2: Extract report text
    print("  Step 2: Extracting report text...")
    reports = extract_all_reports(report_files)

    # Step 3: Generate predictions via LLM
    print("  Step 3: Generating predictions...")
    new_predictions = generate_predictions_for_questions(questions_to_process, reports)

    # Merge
    new_pred_map = {p['unique_id']: p for p in new_predictions}
    final_predictions = []
    for q in questions:
        uid = q.get('unique_id', '')
        if uid in existing_predictions:
            final_predictions.append(existing_predictions[uid])
        elif uid in new_pred_map:
            final_predictions.append(new_pred_map[uid])
        else:
            final_predictions.append({
                "unique_id": uid,
                "complete_question": q.get('complete_question', ''),
                "atleast_one_successful_execution": False,
                "is_answer_present": False,
                "predictive_or_qna": q.get('question_type', 'predictive').lower(),
                "predicted_metrics_and_values_for_predictive": [],
                "answer_text_for_qna": ""
            })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_predictions, f, indent=2, ensure_ascii=False)

    print(f"  Saved: {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Extract predictions from ablation run reports')
    parser.add_argument('--ablation', type=str, required=True,
                        choices=list(ABLATION_CONFIGS.keys()),
                        help='Ablation name (no_coder or no_expert_knowledge)')
    args = parser.parse_args()

    ablation_name = args.ablation
    cfg = ABLATION_CONFIGS[ablation_name]
    responses_dir = cfg["responses_dir"]
    tasks = cfg["tasks"]
    scenarios = cfg["scenarios"]

    # Output goes to: final_results/ablation_{name}/
    output_dir = ROOT_DIR / "final_testing_codes" / "GET_GTS_FINAL" / "final_results" / f"ablation_{ablation_name}"

    print(f"Ablation: {ablation_name}")
    print(f"Responses dir: {responses_dir}")
    print(f"Output dir: {output_dir}")
    print(f"Tasks: {tasks}")
    print(f"Scenarios: {scenarios}")

    # Load questions
    print("\nLoading all questions...")
    all_questions = load_questions()
    print(f"Loaded {len(all_questions)} task-scenario combinations\n")

    success = 0
    fail = 0
    for task in tasks:
        for scenario in scenarios:
            ok = process_task_scenario(ablation_name, responses_dir, output_dir,
                                       task, scenario, all_questions)
            if ok:
                success += 1
            else:
                fail += 1

    print(f"\n{'='*60}")
    print(f"DONE — {ablation_name}: {success} succeeded, {fail} failed")
    print(f"Predictions saved to: {output_dir}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
