# MAE and Accuracy Evaluation System

This package evaluates model predictions against ground truths using two metrics:
- **MAE (Mean Absolute Error)** for predictive questions
- **Accuracy** for QnA questions

## Features

### For Predictive Questions (MAE):
- Matches metrics using intelligent similarity detection (exact match, substring match, equivalence groups)
- Uses maximum ground truth value as reference when multiple GT values exist
- Calculates MAE against all GT values and selects minimum
- Uses `value_in_100_range` for calculations
- Skips questions without predictions

### For QnA Questions (Accuracy):
- Normalizes text (lowercase, remove punctuation, trim whitespace)
- Handles comma-separated values
- Checks for exact match after normalization
- Counts missing predictions as incorrect

### Metric Matching Rules:
1. **Exact match** after normalization: `pass@1` == `pass@1`
2. **Substring match**: `f1` matches `f1-score`
3. **Equivalence groups**: `accuracy` == `pass@1` (configurable in `config.py`)

## Directory Structure

```
mae_accuracy_evaluation/
├── __init__.py              # Package initialization
├── config.py                # Configuration (paths, metric mappings)
├── data_loader.py           # Load ground truths and predictions
├── metric_matcher.py        # Metric name similarity matching
├── normalizer.py            # Text and metric normalization
├── predictive_evaluator.py # MAE calculation for predictive questions
├── qna_evaluator.py         # Accuracy calculation for QnA questions
├── reporter.py              # Report generation
└── evaluator.py             # Main orchestrator
```

## Usage

### Run Evaluation

```bash
cd GET_GTS_FINAL
python run_mae_accuracy_evaluation.py
```

### Input Files

**Ground Truths** (in `Ground_truths_1/`):
- Format: `{task}_scenario_{scenario}_ground_truths.json`
- Example: `01_Code_Generation_scenario_1_ground_truths.json`

**Predictions** (in `Predictions_1/`):
- Format: `{task}_scenario_{scenario}_predictions.json`
- Example: `01_Code_Generation_scenario_1_predictions.json`

### Output Files

Results are saved in `mae_accuracy_results/`:
1. **`evaluation_report.json`** - Full detailed report with:
   - Overall metrics (MAE and Accuracy)
   - Per-task breakdown
   - Per-scenario breakdown
   - Per-task-scenario breakdown
   - Per-metric MAE statistics
   - Detailed results for each question

2. **`evaluation_summary.txt`** - Readable summary with formatted statistics

## Ground Truth Format

```json
{
  "unique_id": "uuid",
  "complete_question": "Question text",
  "predictive_or_qna": "predictive" or "qna",
  "is_answer_present": true/false,
  "ground_truth_metrics_and_values_for_predictive": [
    {
      "metric_name": "pass@1",
      "value": "61.25",
      "value_in_100_range": 61.25
    }
  ],
  "answer_text_for_qna": "GPT-4"
}
```

## Prediction Format

```json
{
  "unique_id": "uuid",
  "complete_question": "Question text",
  "predictive_or_qna": "predictive" or "qna",
  "predicted_metrics_and_values_for_predictive": [
    {
      "metric_name": "pass@1",
      "value": "65.00",
      "value_in_100_range": 65.0
    }
  ],
  "answer_text_for_qna": "GPT-4"
}
```

## Configuration

Edit `mae_accuracy_evaluation/config.py` to customize:

### Paths
```python
GROUND_TRUTH_DIR = BASE_DIR / "Ground_truths_1"
PREDICTIONS_DIR = BASE_DIR / "Predictions_1"
OUTPUT_DIR = BASE_DIR / "mae_accuracy_results"
```

### Metric Equivalence Groups
```python
METRIC_EQUIVALENTS = {
    "accuracy": ["pass@1", "acc", "pass@k"],
    "f1": ["f1-score", "f1_score"],
    "bleu": ["bleu-4", "bleu4"],
    # Add more mappings as needed
}
```

## Example Output

```
================================================================================
MAE AND ACCURACY EVALUATION REPORT
================================================================================

📊 MAE (Mean Absolute Error) - Predictive Questions
--------------------------------------------------------------------------------
Overall Mean MAE: 21.18
Total Questions Evaluated: 15
Total Metrics Compared: 15

Per-Task MAE:
  Code_Generation:
    Mean MAE: 21.18
    Questions: 15
    Metrics: 15

Per-Task-Scenario MAE:
  Code_Generation_GT_available:
    Mean MAE: 21.18
    Questions: 15
    Metrics: 15

================================================================================
✓ ACCURACY - QnA Questions
--------------------------------------------------------------------------------
Overall Accuracy: 11.70%
Correct: 11/94

Per-Task-Scenario Accuracy:
  Code_Generation_GT_available:
    Accuracy: 55.00%
    Correct: 11/20
```

## Algorithm Details

### MAE Calculation
1. Match each GT metric with predicted metrics using similarity rules
2. For matched metrics:
   - Get maximum GT value (if multiple GT values exist)
   - Calculate MAE between predicted value and each GT value
   - Select minimum MAE
3. Aggregate MAE values by task, scenario, task-scenario, and metric type

### Accuracy Calculation
1. Normalize both GT and predicted answers (lowercase, remove punctuation)
2. Handle comma-separated values (check if any predicted value matches any GT value)
3. Check for exact match
4. Aggregate by task, scenario, and task-scenario pairs

## Notes

- Questions without predictions are skipped for MAE calculation
- Questions without predictions are counted as incorrect for Accuracy
- Empty GT answers are skipped
- Multiple GT values are handled by using the maximum as reference
- All values are expected in 100-range format (0-100)

## Troubleshooting

**Issue**: No predictions loaded
- Check `PREDICTIONS_DIR` path in `config.py`
- Ensure prediction files follow naming convention

**Issue**: Low match rate for metrics
- Review metric names in ground truth vs predictions
- Add new equivalence mappings to `METRIC_EQUIVALENTS` in `config.py`

**Issue**: Unexpected accuracy results
- Check answer normalization in `normalizer.py`
- Verify comma-separated value handling matches your data format
