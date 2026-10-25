"""
Module for LLM-based ground truth generation using cached responses.
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add root directory to path to import utils
# Ground_truth_generator_v2 is in final_testing_codes/GET_GTS_FINAL/ground_truth_generator_v2
# Need to go up 3 levels to reach litmus_agent root
root_dir = str(Path(__file__).resolve().parents[3])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utils.aoai_chat import get_chat_response


def create_ground_truth_prompt(user_query: str, cached_responses: Dict[str, Optional[str]], question_type: str) -> str:
    """
    Create LLM prompt for ground truth generation matching the format from generate_ground_truths.py.
    
    Args:
        user_query: The original user question
        cached_responses: Dict of {web_query: response}
        question_type: Type of question (predictive/qna)
    
    Returns:
        Formatted prompt string
    """
    # Combine all cached responses
    web_search_responses = []
    for web_query, response in cached_responses.items():
        if response:
            web_search_responses.append(response)
    
    if not web_search_responses:
        websearch_text = "No web search results available."
    else:
        websearch_text = "\n\n=== WEB SEARCH RESPONSE ===\n\n".join(web_search_responses)
        if len(websearch_text) > 40000:
            websearch_text = websearch_text[:40000] + "\n\n[TRUNCATED DUE TO LENGTH...]"
    
    # Determine predictive or qna
    predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
    
    prompt = f"""Extract ground truth answer from web search and crawl agent responses.

USER QUERY: {user_query}
QUERY TYPE: {predictive_or_qna}

WEB SEARCH & CRAWL AGENT RESPONSES:
{websearch_text}

INSTRUCTIONS:

1. DETERMINE is_answer_present:
   - Set to true ONLY if web search responses contain a relevant, clear answer to the user query
   - Set to false if no answer found or responses are unclear/irrelevant

2. FOR PREDICTIVE QUERIES:
   - Extract ALL performance metrics mentioned (e.g., accuracy, pass@1, pass@k, BLEU, ROUGE, F1, precision, recall, etc.)
   - For EACH metric found, create an object with:
     * metric_name: exact name of the metric (string, e.g., "pass@1", "accuracy", "BLEU")
     * value: original value AS STATED in the response (string, keep original format like "61.25", "0.85", "85.5")
     * value_in_100_range: numeric value scaled to 0-100 range (float, NO percentage signs or symbols)
   - Scaling rules for value_in_100_range:
     * If value is percentage (e.g., "61.25%"): extract number → 61.25
     * If value is decimal 0-1 (e.g., "0.85"): multiply by 100 → 85.0
     * If value already 0-100 (e.g., "85.5"): use as-is → 85.5
     * If other range: convert proportionally to 0-100
   - ground_truth_metrics_and_values_for_predictive MUST be a LIST of objects (can be empty list if no metrics found)

3. FOR QNA QUERIES:
   - Extract CONCISE answer value(s) from web search responses:
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
     * Provide BOTH ground_truth_metrics_and_values_for_predictive (with list of metrics)
     * AND answer_text_for_qna (with concise value)
   - Example: "Which model performs best?" → metrics: [{...}] AND answer_text_for_qna: "GPT-4". For questions like what are the metrics etc, compare related questions - you might need to compare which model is best or which language is best, the answer should be the best prefroming model/language and the predicitve metrics should be the best performing value for the metrics for answering the particular question.

If answer for EXACT LANGUAGE-TASK-MODEL is found, only then is_answer_present should be true, else give false Please!!
     
OUTPUT FORMAT (strict JSON, no markdown, no explanation):

For PREDICTIVE only:
{{
  "is_answer_present": true,
  "ground_truth_metrics_and_values_for_predictive": [
    {{
      "metric_name": "pass@1",
      "value": "61.25",
      "value_in_100_range": 61.25
    }}
  ],
  "answer_text_for_qna": ""
}}

For QNA only:
{{
  "is_answer_present": true,
  "ground_truth_metrics_and_values_for_predictive": [],
  "answer_text_for_qna": "GPT-4"
}}

For BOTH (when metrics exist AND there's a concise answer):
{{
  "is_answer_present": true,
  "ground_truth_metrics_and_values_for_predictive": [
    {{
      "metric_name": "pass@1",
      "value": "82.5",
      "value_in_100_range": 82.5
    }}
  ],
  "answer_text_for_qna": "GPT-4"
}}

CRITICAL RULES:
- Use ONLY information from web search responses above
- value_in_100_range must be NUMERIC ONLY (no %, no strings, just float)
- value keeps original format as string
- answer_text_for_qna must be CONCISE (model name, language, number, etc.) - NO full sentences
- If both metrics and concise answer exist, provide BOTH
- ground_truth_metrics_and_values_for_predictive is always a LIST ([] if empty, never null)
- answer_text_for_qna is always a STRING ("" if empty, never null)
- Output valid JSON only
"""
    
    return prompt


def generate_ground_truth(user_query: str, cached_responses: Dict[str, Optional[str]], question_type: str) -> Dict:
    """
    Generate ground truth using LLM based on cached web search responses.
    Returns format matching generate_ground_truths.py
    
    Args:
        user_query: The original user question
        cached_responses: Dict of {web_query: response}
        question_type: Type of question (predictive/qna)
    
    Returns:
        Dict with is_answer_present, ground_truth_metrics_and_values_for_predictive, answer_text_for_qna
    """
    predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
    
    try:
        # Create prompt
        prompt = create_ground_truth_prompt(user_query, cached_responses, question_type)
        
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
        # This allows BOTH to be present when applicable
        if result.get("ground_truth_metrics_and_values_for_predictive") is None:
            result["ground_truth_metrics_and_values_for_predictive"] = []
        elif not isinstance(result.get("ground_truth_metrics_and_values_for_predictive"), list):
            result["ground_truth_metrics_and_values_for_predictive"] = []
        
        if result.get("answer_text_for_qna") is None:
            result["answer_text_for_qna"] = ""
        elif not isinstance(result.get("answer_text_for_qna"), str):
            result["answer_text_for_qna"] = str(result.get("answer_text_for_qna", ""))
        
        return result
    
    except Exception as e:
        print(f"Error generating ground truth: {e}")
        
        # Return default structure - always list and string, not null
        return {
            "is_answer_present": False,
            "ground_truth_metrics_and_values_for_predictive": [],
            "answer_text_for_qna": ""
        }


def generate_ground_truths_for_questions(
    questions: List[Dict],
    all_cached_responses: Dict[str, Dict[str, Optional[str]]]
) -> List[Dict]:
    """
    Generate ground truths for a list of questions.
    Returns format matching generate_ground_truths.py
    
    Args:
        questions: List of question dicts with unique_id, query, question_type
        all_cached_responses: Dict of {query_id: {web_query: response}}
    
    Returns:
        List of dicts with structure:
        {
            "unique_id": "...",
            "complete_question": "...",
            "atleast_one_successful_execution": bool,
            "is_answer_present": bool,
            "predictive_or_qna": "predictive"/"qna",
            "ground_truth_metrics_and_values_for_predictive": [...] or None,
            "answer_text_for_qna": "..." or None
        }
    """
    results = []
    
    for question in questions:

        print(question)

        unique_id = question.get('unique_id')
        complete_question = question.get('complete_question')
        question_type = question.get('question_type', 'qna')
        
        # Get cached responses for this question
        cached_responses = all_cached_responses.get(unique_id, {})
        
        # Check if we have any cached responses
        has_responses = any(response is not None for response in cached_responses.values())
        
        # Generate ground truth
        llm_result = generate_ground_truth(complete_question, cached_responses, question_type)
        
        # Determine predictive_or_qna - but question can have BOTH answers
        predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
        
        # Check if we have both types of answers
        has_metrics = llm_result.get("ground_truth_metrics_and_values_for_predictive") and len(llm_result.get("ground_truth_metrics_and_values_for_predictive", [])) > 0
        has_text_answer = llm_result.get("answer_text_for_qna") and llm_result.get("answer_text_for_qna", "").strip() != ""
        
        # If both exist, keep original type but note both are present
        # The data structure supports both simultaneously
        
        # Build final ground truth matching the format from generate_ground_truths.py
        ground_truth = {
            "unique_id": unique_id,
            "complete_question": complete_question,
            "atleast_one_successful_execution": has_responses,
            "is_answer_present": llm_result.get("is_answer_present", False),
            "predictive_or_qna": predictive_or_qna,
            "ground_truth_metrics_and_values_for_predictive": llm_result.get("ground_truth_metrics_and_values_for_predictive"),
            "answer_text_for_qna": llm_result.get("answer_text_for_qna")
        }
        
        # Add to results
        results.append(ground_truth)
    
    return results
