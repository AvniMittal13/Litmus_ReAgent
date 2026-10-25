"""
Module to generate web search queries using LLM when intermediates are not available.
"""
import sys
import json
import re
from pathlib import Path
from typing import List

# Hyperparameter: Number of search queries to generate per question
NUM_QUERIES_TO_GENERATE = 10

root_dir = str(Path(__file__).resolve().parents[3])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utils.aoai_chat import get_chat_response


def generate_web_search_queries(user_question: str, num_queries: int = None) -> List[str]:
    """
    Generate web search queries using LLM to help answer the user's question.
    
    Args:
        user_question: The original user question
        num_queries: Number of queries to generate (defaults to NUM_QUERIES_TO_GENERATE)
    
    Returns:
        List of web search queries (or fewer if generation fails)
    """
    if num_queries is None:
        num_queries = NUM_QUERIES_TO_GENERATE
    
    prompt = f"""Generate {num_queries} diverse and specific web search queries that would help find information to answer this question:

QUESTION: {user_question}

Requirements:
1. Generate exactly {num_queries} search queries
2. Each query should be specific and focused on different aspects (models, benchmarks, papers, datasets, performance metrics)
3. Queries should be suitable for academic/technical search (e.g., arXiv, papers, documentation)
4. Include specific technical terms, model names, benchmark names when relevant
5. Return ONLY a JSON array of strings, no additional text

Example output format (for {num_queries} queries):
["query 1", "query 2", ..., "query {num_queries}"]

Output (JSON array only):"""

    try:
        # Get LLM response
        response = get_chat_response(
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Try to parse as JSON
        # First, try to extract JSON array from response
        json_match = re.search(r'\[.*?\]', response, re.DOTALL)
        if json_match:
            queries = json.loads(json_match.group(0))
            if isinstance(queries, list):
                # Ensure all items are strings and limit to num_queries
                queries = [str(q).strip() for q in queries if q][:num_queries]
                return queries
        
        # If that fails, try parsing entire response
        queries = json.loads(response)
        if isinstance(queries, list):
            queries = [str(q).strip() for q in queries if q][:num_queries]
            return queries
        
        print(f"Warning: Unexpected response format from LLM: {response[:100]}")
        return []
    
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse LLM response as JSON: {e}")
        print(f"Response was: {response[:200]}")
        return []
    except Exception as e:
        print(f"Warning: Error generating web search queries: {e}")
        return []


def generate_queries_for_questions(questions_dict: dict, empty_query_ids: List[str]) -> dict:
    """
    Generate web search queries for multiple questions using LLM.
    
    Args:
        questions_dict: Dict mapping query_id to question object (with 'complete_question' field)
        empty_query_ids: List of query_ids that need generated queries
    
    Returns:
        Dict of {query_id: List[str]} with generated queries
    """
    generated_queries = {}
    
    for query_id in empty_query_ids:
        question_obj = questions_dict.get(query_id)
        if not question_obj:
            print(f"Warning: No question found for query_id {query_id}")
            generated_queries[query_id] = []
            continue
        
        complete_question = question_obj.get('complete_question')
        if not complete_question:
            print(f"Warning: No complete_question for query_id {query_id}")
            generated_queries[query_id] = []
            continue
        
        # Generate queries
        queries = generate_web_search_queries(complete_question)
        generated_queries[query_id] = queries
        
        if queries:
            print(f"  Generated {len(queries)} queries for: {complete_question[:60]}...")
        else:
            print(f"  Failed to generate queries for: {complete_question[:60]}...")
    
    return generated_queries
