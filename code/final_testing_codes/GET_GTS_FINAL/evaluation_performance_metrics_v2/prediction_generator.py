"""
Module for LLM-based prediction generation from agent reports.
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add root directory to path to import utils
root_dir = str(Path(__file__).resolve().parents[3])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utils.aoai_chat import get_chat_response


def create_prediction_prompt(user_query: str, agent_report: str, question_type: str) -> str:
    """
    Create LLM prompt for prediction extraction from agent report.
    Similar structure to ground_truth_generator but adapted for agent reports.
    
    Args:
        user_query: The original user question
        agent_report: The agent's original_report text
        question_type: Type of question (predictive/qna)
    
    Returns:
        Formatted prompt string
    """
    # Truncate report if too long
    if len(agent_report) > 40000:
        agent_report = agent_report[:40000] + "\n\n[TRUNCATED DUE TO LENGTH...]"
    
    # Determine predictive or qna
    predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
    
    prompt = f"""Extract agent's predicted answer from research report.

USER QUERY: {user_query}
QUERY TYPE: {predictive_or_qna}

AGENT RESEARCH REPORT:
{agent_report}

INSTRUCTIONS:

1. DETERMINE is_answer_present:
   - Set to true ONLY if agent's report contains a relevant, clear answer to the user query
   - Set to false if no answer found or report is unclear/irrelevant

2. FOR PREDICTIVE QUERIES:
   - Extract ALL performance metrics mentioned (e.g., accuracy, pass@1, pass@k, BLEU, ROUGE, F1, precision, recall, etc.)
   - For EACH metric found, create an object with:
     * metric_name: exact name of the metric (string, e.g., "pass@1", "accuracy", "BLEU")
     * value: original value AS STATED in the report (string, keep original format like "61.25", "0.85", "85.5")
     * value_in_100_range: numeric value scaled to 0-100 range (float, NO percentage signs or symbols)
   - Scaling rules for value_in_100_range:
     * If value is percentage (e.g., "61.25%"): extract number → 61.25
     * If value is decimal 0-1 (e.g., "0.85"): multiply by 100 → 85.0
     * If value already 0-100 (e.g., "85.5"): use as-is → 85.5
     * If other range: convert proportionally to 0-100
   - predicted_metrics_and_values_for_predictive MUST be a LIST of objects (can be empty list if no metrics found)

3. FOR QNA QUERIES:
   - Extract CONCISE answer value(s) from agent's report:
     * For model questions: extract model name ONLY (e.g., "GPT-4", "CodeGen2 (7B)")
     * For language questions: extract language name(s) ONLY (e.g., "French", "Chinese, Japanese, Korean")
     * For paper/method questions: extract paper/method name ONLY
     * For numeric questions: extract number(s) ONLY (e.g., "82.5", "61.25, 78.5")
     * For list questions: extract comma-separated values (e.g., "Python, Java, JavaScript")
   - NEVER include full sentences or explanations
   - If multiple values: use comma-separated format
   - If no clear answer: leave as empty string ""

4. BOTH PREDICTIVE AND QNA (IMPORTANT):
   - If the question can be answered BOTH ways (metrics exist AND there's a concise answer like model name):
     * Provide BOTH predicted_metrics_and_values_for_predictive (with list of metrics)
     * AND answer_text_for_qna (with concise value)
   - Example: "Which model performs best?" → metrics: [{{...}}] AND answer_text_for_qna: "GPT-4"
   - For questions like "what are the metrics", "compare related questions" - you might need to compare which model is best or which language is best
   - The answer should be the best performing model/language and the predictive metrics should be the best performing value for the metrics for answering the particular question

OUTPUT FORMAT (strict JSON, no markdown, no explanation):

For PREDICTIVE only:
{{{{
  "is_answer_present": true,
  "predicted_metrics_and_values_for_predictive": [
    {{{{
      "metric_name": "pass@1",
      "value": "61.25",
      "value_in_100_range": 61.25
    }}}}
  ],
  "answer_text_for_qna": ""
}}}}

For QNA only:
{{{{
  "is_answer_present": true,
  "predicted_metrics_and_values_for_predictive": [],
  "answer_text_for_qna": "GPT-4"
}}}}

For BOTH (when metrics exist AND there's a concise answer):
{{{{
  "is_answer_present": true,
  "predicted_metrics_and_values_for_predictive": [
    {{{{
      "metric_name": "pass@1",
      "value": "82.5",
      "value_in_100_range": 82.5
    }}}}
  ],
  "answer_text_for_qna": "GPT-4"
}}}}

CRITICAL RULES:
- Use ONLY information from agent's report above
- value_in_100_range must be NUMERIC ONLY (no %, no strings, just float)
- value keeps original format as string
- answer_text_for_qna must be CONCISE (model name, language, number, etc.) - NO full sentences
- If both metrics and concise answer exist, provide BOTH
- predicted_metrics_and_values_for_predictive is always a LIST ([] if empty, never null)
- answer_text_for_qna is always a STRING ("" if empty, never null)
- Output valid JSON only
"""
    
    return prompt


def generate_prediction(user_query: str, agent_report: str, question_type: str) -> Dict:
    """
    Generate prediction using LLM based on agent's report.
    Returns format matching ground truth structure.
    
    Args:
        user_query: The original user question
        agent_report: The agent's original_report text
        question_type: Type of question (predictive/qna)
    
    Returns:
        Dict with is_answer_present, predicted_metrics_and_values_for_predictive, answer_text_for_qna
    """
    predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
    
    try:
        # Create prompt
        prompt = create_prediction_prompt(user_query, agent_report, question_type)
        
        # Get LLM response
        response = get_chat_response(
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        import json
        import re
        
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
        else:
            result = json.loads(response)
        
        # Validate structure
        if "is_answer_present" not in result:
            result["is_answer_present"] = False
        
        # Ensure correct structure - always list for metrics, always string for answer
        if result.get("predicted_metrics_and_values_for_predictive") is None:
            result["predicted_metrics_and_values_for_predictive"] = []
        elif not isinstance(result.get("predicted_metrics_and_values_for_predictive"), list):
            result["predicted_metrics_and_values_for_predictive"] = []
        
        if result.get("answer_text_for_qna") is None:
            result["answer_text_for_qna"] = ""
        elif not isinstance(result.get("answer_text_for_qna"), str):
            result["answer_text_for_qna"] = str(result.get("answer_text_for_qna", ""))
        
        return result
    
    except Exception as e:
        print(f"Error generating prediction: {e}")
        
        # Return default structure
        return {
            "is_answer_present": False,
            "predicted_metrics_and_values_for_predictive": [],
            "answer_text_for_qna": ""
        }


def generate_predictions_for_questions(
    questions: List[Dict],
    all_reports: Dict[str, Optional[str]]
) -> List[Dict]:
    """
    Generate predictions for a list of questions from agent reports.
    Returns format matching ground truth structure.
    
    Args:
        questions: List of question dicts with unique_id, complete_question, question_type
        all_reports: Dict of {unique_id: report_text}
    
    Returns:
        List of dicts with structure:
        {
            "unique_id": "...",
            "complete_question": "...",
            "atleast_one_successful_execution": bool,
            "is_answer_present": bool,
            "predictive_or_qna": "predictive"/"qna",
            "predicted_metrics_and_values_for_predictive": [...],
            "answer_text_for_qna": "..."
        }
    """
    results = []
    
    for question in questions:
        print(question)
        
        unique_id = question.get('unique_id')
        complete_question = question.get('complete_question')
        question_type = question.get('question_type', 'qna')
        
        # Get agent report for this question
        agent_report = all_reports.get(unique_id)
        
        # Check if we have a report
        has_report = agent_report is not None and len(agent_report.strip()) > 0
        
        if not has_report:
            # No report available
            llm_result = {
                "is_answer_present": False,
                "predicted_metrics_and_values_for_predictive": [],
                "answer_text_for_qna": ""
            }
        else:
            # Generate prediction from report
            llm_result = generate_prediction(complete_question, agent_report, question_type)
        
        # Determine predictive_or_qna
        predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
        
        # Build final prediction matching ground truth format
        prediction = {
            "unique_id": unique_id,
            "complete_question": complete_question,
            "atleast_one_successful_execution": has_report,
            "is_answer_present": llm_result.get("is_answer_present", False),
            "predictive_or_qna": predictive_or_qna,
            "predicted_metrics_and_values_for_predictive": llm_result.get("predicted_metrics_and_values_for_predictive"),
            "answer_text_for_qna": llm_result.get("answer_text_for_qna")
        }
        
        results.append(prediction)
    
    print(f"Generated predictions for {len(results)} questions")
    
    return results
