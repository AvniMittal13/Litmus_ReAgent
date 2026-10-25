"""
Module to extract web search queries from intermediates files.
"""
import json
from pathlib import Path
from typing import List
from .config import INTERMEDIATE_FILE_PATTERNS


def extract_queries_from_intermediates(query_folder: Path) -> List[str]:
    """
    Extract all web search queries from intermediates files.
    
    Args:
        query_folder: Path to the query_id folder
    
    Returns:
        List of web search queries extracted from tool_invocations
    """
    queries = []
    
    if not query_folder.exists():
        print(f"Warning: Query folder does not exist: {query_folder}")
        return queries
    
    # Check if intermediates subfolder exists
    intermediates_folder = query_folder / "intermediates"
    
    if intermediates_folder.exists() and intermediates_folder.is_dir():
        # Search for intermediates files inside the subfolder
        intermediate_files = []
        for pattern in INTERMEDIATE_FILE_PATTERNS:
            intermediate_files.extend(intermediates_folder.glob(pattern))
    else:
        # Search in the main query folder
        intermediate_files = []
        for pattern in INTERMEDIATE_FILE_PATTERNS:
            intermediate_files.extend(query_folder.glob(pattern))
    
    if not intermediate_files:
        print(f"Warning: No intermediates files found in {query_folder}")
        return queries
    
    # Process each intermediates file
    for intermediate_file in intermediate_files:
        try:
            with open(intermediate_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract tool_invocations
            tool_invocations = data.get('tool_invocations', [])
            
            # Extract query from each invocation
            for invocation in tool_invocations:
                if isinstance(invocation, dict) and 'query' in invocation:
                    query = invocation['query']
                    if query and isinstance(query, str):
                        queries.append(query)
        
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse {intermediate_file.name}: {e}")
            continue
        except Exception as e:
            print(f"Warning: Error processing {intermediate_file.name}: {e}")
            continue
    
    return queries


def extract_all_queries(query_folders: dict) -> dict:
    """
    Extract queries for multiple query_id folders.
    
    Args:
        query_folders: Dict of {query_id: Path or None}
    
    Returns:
        Dict of {query_id: List[str]} where list contains web search queries
    """
    results = {}
    
    for query_id, folder in query_folders.items():
        if folder is None:
            results[query_id] = []
            continue
        
        queries = extract_queries_from_intermediates(folder)
        results[query_id] = queries
        
        if not queries:
            print(f"Warning: No queries extracted for {query_id}")
    
    return results
