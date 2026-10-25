"""QnA question evaluator (Accuracy calculation)"""
from .normalizer import (
    normalize_answer_text, 
    split_comma_separated,
    fuzzy_match_model,
    fuzzy_match_language,
    semantic_similarity_match,
    normalize_metric_name_v2
)


def extract_answer_from_metrics(pred_data: dict) -> str:
    """Extract normalized metric names from predicted_metrics_and_values_for_predictive."""
    metrics = pred_data.get('predicted_metrics_and_values_for_predictive', [])
    if not metrics:
        return ''
    
    # Extract metric_name from each item in the list and normalize
    names = [normalize_metric_name_v2(m.get('metric_name', '')) for m in metrics if m.get('metric_name')]
    return ', '.join(set(names)) if names else ''


def check_exact_match(gt_answer: str, pred_answer: str) -> tuple:
    """Check if answers match after normalization.
    
    Handles comma-separated values with fuzzy matching for models/languages.
    Returns match result and match details.
    
    Args:
        gt_answer: Ground truth answer
        pred_answer: Predicted answer
        
    Returns:
        Tuple of (is_match, match_score, match_details)
        - is_match: True if fully or partially matched
        - match_score: Float 0-1 indicating match quality
        - match_details: Dict with matching info
    """
    if not gt_answer or not pred_answer:
        return False, 0.0, {'reason': 'Empty answer'}
    
    # Normalize both answers
    print("in check_exact_match")
    gt_normalized = normalize_answer_text(gt_answer)
    pred_normalized = normalize_answer_text(pred_answer)
    
    # Check exact match first
    if gt_normalized == pred_normalized:
        return True, 1.0, {'reason': 'Exact match'}
    
    # Check bidirectional containment for simple answers
    if gt_normalized in pred_normalized or pred_normalized in gt_normalized:
        return True, 1.0, {'reason': 'Containment match'}
    
    # Check fuzzy model name match
    if fuzzy_match_model(pred_answer, gt_answer):
        return True, 1.0, {'reason': 'Fuzzy model match'}
    
    # Check fuzzy language match
    if fuzzy_match_language(pred_answer, gt_answer):
        return True, 1.0, {'reason': 'Fuzzy language match'}
    
    print("in check_exact_match after basic")
    
    # Check for comma-separated values (partial matching)
    gt_values = split_comma_separated(gt_answer)
    pred_values = split_comma_separated(pred_answer)

    print("gt answer: ", gt_answer)
    print("pred answer: ", pred_answer)

    print("[CONCEPT-NORM] gt values: ", gt_values)
    print("[CONCEPT-NORM] pred values: ", pred_values)
    
    
    if not gt_values or not pred_values:
        return False, 0.0, {'reason': 'No values to compare'}
    
    # Count matches (including fuzzy)
    matched_gt = set()
    matched_pred = set()
    
    for i, pred_val in enumerate(pred_values):
        for j, gt_val in enumerate(gt_values):
            if j in matched_gt:
                continue
            # Check exact, containment, or fuzzy match
            if (pred_val == gt_val or 
                pred_val in gt_val or 
                gt_val in pred_val or
                fuzzy_match_model(pred_val, gt_val) or
                fuzzy_match_language(pred_val, gt_val)):
                matched_gt.add(j)
                matched_pred.add(i)
                break
    

    num_matched = len(matched_gt)
    total_gt = len(gt_values)

    print("is_match: ", num_matched)
    print("="*20)
    
    if num_matched == 0:
        # Additional check: Semantic similarity for unmatched values
        unmatched_pred = [pred_values[i] for i in range(len(pred_values)) if i not in matched_pred]
        unmatched_gt = [gt_values[j] for j in range(len(gt_values)) if j not in matched_gt]
        unmatched_pred_indices = [i for i in range(len(pred_values)) if i not in matched_pred]
        unmatched_gt_indices = [j for j in range(len(gt_values)) if j not in matched_gt]
        
        print(f"[SEMANTIC] No fuzzy matches found. Trying semantic similarity...")
        print(f"[SEMANTIC] Unmatched pred values: {unmatched_pred}")
        print(f"[SEMANTIC] Unmatched gt values: {unmatched_gt}")
        
        if unmatched_pred and unmatched_gt:
            semantic_result = semantic_similarity_match(unmatched_pred, unmatched_gt, threshold=0.80)
            print(f"[SEMANTIC] Result: matched_gt={semantic_result['matched_gt']}, matched_pred={semantic_result['matched_pred']}")
            print(f"[SEMANTIC] Match pairs: {semantic_result.get('match_pairs', [])}")
            # Map back to original indices
            for local_pred_idx in semantic_result['matched_pred']:
                matched_pred.add(unmatched_pred_indices[local_pred_idx])
            for local_gt_idx in semantic_result['matched_gt']:
                matched_gt.add(unmatched_gt_indices[local_gt_idx])
        
        num_matched = len(matched_gt)
        total_gt = len(gt_values)
        print(f"[SEMANTIC] After semantic matching: {num_matched}/{total_gt} matched")

        if num_matched == 0:
            return False, 0.0, {'reason': 'No match', 'matched': 0, 'total': total_gt}

    match_score = num_matched / total_gt
    
    # Consider it a match if at least one GT value matched
    is_match = num_matched > 0


    
    return is_match, match_score, {
        'reason': f'Partial match ({num_matched}/{total_gt})',
        'matched': num_matched,
        'total': total_gt,
        'matched_gt_indices': list(matched_gt),
        'matched_pred_indices': list(matched_pred)
    }


def evaluate_qna_questions(ground_truths: dict, predictions: dict) -> list:
    """Evaluate all QnA questions.
    
    Args:
        ground_truths: Dictionary of ground truth data
        predictions: Dictionary of prediction data
        
    Returns:
        List of detailed results
    """
    results = []
    
    for unique_id, gt_data in ground_truths.items():
        if gt_data.get('predictive_or_qna') != 'qna':
            continue
        
        # Skip if GT has no answer
        if not gt_data.get('is_answer_present'):
            continue
        
        gt_answer = gt_data.get('answer_text_for_qna', '')
        
        # Skip if no ground truth answer
        if not gt_answer:
            continue
        
        # Find matching prediction
        pred_data = predictions.get(unique_id)
        
        if not pred_data:
            # Count as incorrect if no prediction found
            result = {
                'unique_id': unique_id,
                'task_num': gt_data.get('task_num'),
                'scenario_num': gt_data.get('scenario_num'),
                'question': gt_data.get('complete_question', ''),
                'gt_answer': gt_answer,
                'pred_answer': None,
                'is_correct': False,
                'reason': 'No prediction found'
            }
            results.append(result)
            continue
        
        # If prediction has no answer, count as incorrect
        if not pred_data.get('is_answer_present'):
            result = {
                'unique_id': unique_id,
                'task_num': gt_data.get('task_num'),
                'scenario_num': gt_data.get('scenario_num'),
                'question': gt_data.get('complete_question', ''),
                'gt_answer': gt_answer,
                'pred_answer': None,
                'is_correct': False,
                'reason': 'Prediction has no answer'
            }
            results.append(result)
            continue
        
        pred_answer = pred_data.get('answer_text_for_qna', '')
        
        # If pred_answer is empty, try to extract from predicted_metrics_and_values
        if not pred_answer or not pred_answer.strip():
            pred_answer = extract_answer_from_metrics(pred_data)
            print(f"[FALLBACK] Empty answer_text, extracted from metrics: {pred_answer}")
        
        # Check match with fuzzy logic and partial matching
        is_correct, match_score, match_details = check_exact_match(gt_answer, pred_answer)
        
        result = {
            'unique_id': unique_id,
            'task_num': gt_data.get('task_num'),
            'scenario_num': gt_data.get('scenario_num'),
            'question': gt_data.get('complete_question', ''),
            'gt_answer': gt_answer,
            'pred_answer': pred_answer,
            'is_correct': is_correct,
            'match_score': match_score,
            'reason': match_details.get('reason', 'No match')
        }
        results.append(result)
    
    return results
