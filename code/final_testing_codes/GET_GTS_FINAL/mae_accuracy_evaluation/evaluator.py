"""Main evaluator orchestrator"""
from .config import GROUND_TRUTH_DIR, PREDICTIONS_DIR, OUTPUT_DIR
from .data_loader import load_ground_truths, load_predictions
from .predictive_evaluator import evaluate_predictive_questions
from .qna_evaluator import evaluate_qna_questions
from .reporter import generate_report


def run_evaluation():
    """Main evaluation function."""
    print("=" * 80)
    print("MAE AND ACCURACY EVALUATION")
    print("=" * 80)
    print()
    
    # Load data
    print("📂 Loading ground truths...")
    ground_truths = load_ground_truths(GROUND_TRUTH_DIR)
    print(f"   Loaded {len(ground_truths)} ground truth entries")
    
    print("📂 Loading predictions...")
    predictions = load_predictions(PREDICTIONS_DIR)
    print(f"   Loaded {len(predictions)} prediction entries")
    
    # Show prediction coverage
    predictions_with_answers = sum(1 for p in predictions.values() if p.get('is_answer_present', False))
    print(f"   Predictions with actual answers: {predictions_with_answers}/{len(predictions)}")
    
    # Show coverage by task-scenario
    from collections import defaultdict
    coverage = defaultdict(lambda: {'total': 0, 'with_answers': 0})
    for pred_id, pred_data in predictions.items():
        task_num = pred_data.get('task_num', 'unknown')
        scenario_num = pred_data.get('scenario_num', 'unknown')
        key = f"{task_num}_scenario_{scenario_num}"
        coverage[key]['total'] += 1
        if pred_data.get('is_answer_present', False):
            coverage[key]['with_answers'] += 1
    
    print("\n   Prediction coverage by task-scenario:")
    for key in sorted(coverage.keys()):
        stats = coverage[key]
        print(f"     {key}: {stats['with_answers']}/{stats['total']} have answers")
    print()
    
    # Evaluate predictive questions (MAE)
    print("🔢 Evaluating predictive questions (MAE)...")
    mae_results = evaluate_predictive_questions(ground_truths, predictions)
    print(f"   Evaluated {len(mae_results)} predictive questions")
    print()
    
    # Evaluate QnA questions (Accuracy)
    print("✓ Evaluating QnA questions (Accuracy)...")
    qna_results = evaluate_qna_questions(ground_truths, predictions)
    print(f"   Evaluated {len(qna_results)} QnA questions")
    print()
    
    # Generate report
    print("📊 Generating evaluation report...")
    generate_report(mae_results, qna_results, OUTPUT_DIR)
    print()
    
    print("=" * 80)
    print("✅ Evaluation completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    run_evaluation()
