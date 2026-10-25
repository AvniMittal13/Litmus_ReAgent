"""
Ground Truth Generator V2 - Modular Implementation

This package generates ground truth JSONs by:
1. Loading questions from generated_questions
2. Finding query_id folders across multiple response directories
3. Extracting web search queries from intermediates
4. Retrieving cached responses from query_cache.pkl
5. Using LLM to generate ground truths
6. Saving one JSON per task-scenario combination
"""

__version__ = "2.0.0"
