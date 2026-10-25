# Ground Truth & Evaluation Pipeline

## 1. Generate Ground Truths
```bash
python -m ground_truth_generator_v2.main
```
- Extracts GT from web search responses in agent outputs
- Output: `Ground_truths_X/{task}_scenario_{n}_ground_truths.json`

## 2. Extract Predictions from Agent Reports
```bash
python -m evaluation_performance_metrics_v2.main
```
**Config** (`evaluation_performance_metrics_v2/config.py`):
```python
EVALUATION_RESULTS_DIRECTORIES = [ROOT_DIR / "your_output_folder"]
OUTPUT_DIR = ROOT_DIR / "results" / "method_name"
```

## 3. Calculate MAE & Accuracy
```bash
python run_mae_accuracy_evaluation.py
```
**Config** (`mae_accuracy_evaluation/config.py`):
```python
GROUND_TRUTH_DIR = BASE_DIR / "Ground_truths_5"
PREDICTIONS_DIR = BASE_DIR / "results" / "method_name"
OUTPUT_DIR = BASE_DIR / "mae_accuracy_results" / "run_name"
```

## Output Format
```json
{
  "unique_id": "uuid",
  "is_answer_present": true,
  "predictive_or_qna": "predictive",
  "ground_truth_metrics_and_values_for_predictive": [
    {"metric_name": "pass@1", "value": "61.25", "value_in_100_range": 61.25}
  ],
  "answer_text_for_qna": "text for QnA"
}
```

## Metrics
- **Predictive**: MAE on `value_in_100_range`
- **QnA**: Exact match accuracy
