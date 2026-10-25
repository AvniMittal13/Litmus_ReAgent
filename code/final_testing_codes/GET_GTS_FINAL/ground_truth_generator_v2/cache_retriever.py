"""
Module to load query_cache.pkl and retrieve cached responses using embedding similarity.
"""
import pickle
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity
from . import config
from .config import QUERY_CACHE_PATH

# Add root directory to path to import utils
root_dir = str(Path(__file__).resolve().parents[3])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import get_embedding from the same module used in db_search_and_scrape_optimized
try:
    from agents.tools.db_search_and_scrape_optimized import get_embedding
except ImportError:
    print("Warning: Could not import get_embedding, falling back to local implementation")
    # Fallback implementation if import fails
    def get_embedding(text: str) -> List[float]:
        """Fallback - this should not be used in production"""
        import os
        from openai import AzureOpenAI
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
        from dotenv import load_dotenv
        load_dotenv()
        
        _token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDING"),
            azure_ad_token_provider=_token_provider,
            api_version="2025-01-01-preview"
        )
        try:
            resp = client.embeddings.create(input=[text], model="text-embedding-ada-002")
            return resp.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None


def load_query_cache() -> List[Dict]:
    """
    Load the query cache from pickle file.
    
    Returns:
        List of dicts with structure: {
            'query': str,
            'embedding': List[float],
            'response': str
        }
    """
    cache_path = Path(QUERY_CACHE_PATH)
    
    if not cache_path.exists():
        raise FileNotFoundError(f"Query cache not found: {QUERY_CACHE_PATH}")
    
    try:
        with open(cache_path, 'rb') as f:
            cache = pickle.load(f)
        
        if not isinstance(cache, list):
            raise ValueError(f"Expected cache to be a list, got {type(cache)}")
        
        return cache
    
    except Exception as e:
        raise RuntimeError(f"Failed to load query cache: {e}")


def find_cached_response(query: str, cache: List[Dict], threshold: float = 0.90) -> Optional[str]:
    """
    Find cached response for a query using embedding similarity.
    Uses cosine similarity with threshold, same as db_search_and_scrape_optimized.
    
    Args:
        query: The web search query to look for
        cache: The loaded query cache
        threshold: Similarity threshold (default 0.90 for stricter matching)
    
    Returns:
        Cached response string if similarity > threshold, None otherwise
    """
    # Get embedding for the query
    query_embedding = get_embedding(query)
    
    if not query_embedding:
        print(f"Warning: Could not generate embedding for query: {query}")
        return None
    
    best_match = None
    best_similarity = 0.0
    
    for entry in cache:
        if isinstance(entry, dict) and entry.get('embedding') is not None:
            try:
                similarity = cosine_similarity(
                    [query_embedding],
                    [entry['embedding']]
                )[0][0]
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = entry
            except Exception as e:
                print(f"Warning: Error calculating similarity: {e}")
                continue
    
    if best_similarity >= threshold:
        print(f"  [CACHE HIT] Found cached response with {best_similarity:.4f} similarity")
        return best_match['response']
    
    return None


def get_cached_responses(queries: List[str], cache: List[Dict]) -> Dict[str, Optional[str]]:
    """
    Get cached responses for multiple queries using embedding similarity.
    
    Args:
        queries: List of web search queries
        cache: The loaded query cache
    
    Returns:
        Dict of {query: response or None}
    """
    results = {}
    
    for query in queries:
        response = find_cached_response(query, cache)
        results[query] = response
        
        if response is None:
            print(f"  [NO CACHE] No cached response found for query: {query[:80]}...")
    
    return results


def get_all_cached_responses_for_questions(extracted_queries: dict) -> dict:
    """
    Get cached responses for all questions.
    
    Args:
        extracted_queries: Dict of {query_id: List[str]} with web search queries
    
    Returns:
        Dict of {query_id: Dict[str, Optional[str]]} with cached responses
    """
    # Load cache once
    cache = load_query_cache()
    
    results = {}
    
    for query_id, queries in extracted_queries.items():
        if not queries:
            results[query_id] = {}
            continue
        
        cached_responses = get_cached_responses(queries, cache)
        results[query_id] = cached_responses
    
    return results


# ============================================================
# Active DB Search Functions (for reprocessing failed questions)
# ============================================================

def perform_active_db_search(query: str, db_path: Path) -> Optional[str]:
    """
    Perform actual db search + scrape when cache miss.
    Uses existing functions from db_search_and_scrape_unoptim.py
    
    Args:
        query: The search query
        db_path: Path to the combined pkl database
    
    Returns:
        Formatted scraped content string, or None if failed
    """
    try:
        from agents.tools.db_search_and_scrape_unoptim import (
            load_embeddings_from_pkl,
            search_similar_embeddings,
            scrape_url_with_firecrawl
        )
        
        # Get embedding for query
        query_embedding = get_embedding(query)
        if not query_embedding:
            return None
        
        # Load embeddings from combined pkl
        embeddings_data = load_embeddings_from_pkl(str(db_path))
        if not embeddings_data:
            return None

        # Search for similar embeddings (top 8)
        results = search_similar_embeddings(query_embedding, embeddings_data, top_k=8)
        if not results:
            return None
        
        # Scrape URLs and collect content
        scraped_contents = []
        for result in results:
            url = result.get('url')
            if not url:
                continue
            
            print(f"    [ACTIVE SEARCH] Fetching: {url[:60]}...")
            content = scrape_url_with_firecrawl(url)
            
            if content.get('success') and content.get('markdown'):
                scraped_contents.append({
                    'url': url,
                    'similarity': result.get('similarity_score', 0),
                    'content': content['markdown'][:15000],  # Limit content size
                    'task': result.get('task', ''),
                    'description': result.get('description', '')
                })
                print(f"      ✅ Got content ({len(content['markdown'])} chars)")
            else:
                print(f"      ❌ No content")
            
            # Only sleep if NOT from cache (Firecrawl has its own delay)
            # No need to sleep here since scraped_content.json is pre-cached
        
        if not scraped_contents:
            return None
        
        # Format as response string
        formatted = f"Active DB Search Results for: {query}\n\n"
        for i, item in enumerate(scraped_contents):
            formatted += f"--- Result {i+1} (Similarity: {item['similarity']:.4f}) ---\n"
            formatted += f"URL: {item['url']}\n"
            formatted += f"Task: {item['task']}\n"
            formatted += f"Description: {item['description']}\n"
            formatted += f"Content:\n{item['content']}\n\n"
        
        return formatted
    
    except Exception as e:
        print(f"    [ACTIVE SEARCH ERROR] {e}")
        return None


def get_cached_or_search_response(query: str, cache: List[Dict], db_path: Path = None) -> Optional[str]:
    """
    Try cache first, then active db search if enabled and cache miss.
    
    Args:
        query: The search query
        cache: The loaded query cache
        db_path: Path to combined pkl database (for active search)
    
    Returns:
        Response string or None
    """
    # 1. Try cache first (existing logic)
    cached = find_cached_response(query, cache)
    if cached:
        return cached
    
    # 2. If cache miss and active search enabled
    if config.USE_ACTIVE_DB_SEARCH and db_path and db_path.exists():
        print(f"  [CACHE MISS] Performing active DB search for: {query[:60]}...")
        return perform_active_db_search(query, db_path)
    
    return None


def get_all_responses_with_active_search(extracted_queries: dict, task: str) -> dict:
    """
    Get responses for all questions, using active search on cache miss.
    
    Args:
        extracted_queries: Dict of {query_id: List[str]} with web search queries
        task: Task name (for getting correct db path)
    
    Returns:
        Dict of {query_id: Dict[str, Optional[str]]} with responses
    """
    # Load cache once
    cache = load_query_cache()
    
    # Get db path for this task
    db_path = config.get_combined_db_path(task)
    if db_path:
        print(f"Using combined DB: {db_path}")
    else:
        print(f"Warning: No combined DB found for task {task}")
    
    results = {}
    
    for query_id, queries in extracted_queries.items():
        if not queries:
            results[query_id] = {}
            continue
        
        query_results = {}
        for query in queries:
            response = get_cached_or_search_response(query, cache, db_path)
            query_results[query] = response
            
            if response is None:
                print(f"  [NO RESULT] {query[:80]}...")
        
        results[query_id] = query_results
    
    return results
