#!/usr/bin/env python3
"""
Run MAE and Accuracy Evaluation

This script evaluates predictions against ground truths:
- MAE (Mean Absolute Error) for predictive questions
- Accuracy for QnA questions

Usage:
    python run_mae_accuracy_evaluation.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mae_accuracy_evaluation.evaluator import run_evaluation


if __name__ == "__main__":
    try:
        run_evaluation()
    except KeyboardInterrupt:
        print("\n\nEvaluation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
