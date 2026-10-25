#!/usr/bin/env python3
"""
Search interface for precomputed embeddings.
Use this script to search through the embeddings after they've been created.
Now supports searching in specific CSV files or all embeddings.
"""

import sys
import os
from pathlib import Path
from create_and_save_embeddings import search_interface, load_specific_csv_embeddings, EmbeddingManager

def list_available_embeddings():
    """List all available embedding files"""
    base_dir = Path(".")
    pkl_files = list(base_dir.glob("*/*_embeddings.pkl"))
    
    if not pkl_files:
        print("No embedding files found.")
        return []
    
    print("Available embedding files:")
    for i, pkl_file in enumerate(pkl_files, 1):
        csv_name = pkl_file.stem.replace("_embeddings", "")
        folder_name = pkl_file.parent.name
        print(f"  {i}. {folder_name}/{csv_name}")
    
    return pkl_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_embeddings.py <query> [top_k] [--csv csv_name]")
        print("\nOptions:")
        print("  --csv CSV_NAME    Search only in specific CSV embeddings")
        print("  --list           List all available embedding files")
        print("\nExamples:")
        print("  python search_embeddings.py 'python code generation' 3")
        print("  python search_embeddings.py 'multilingual math reasoning' 5")
        print("  python search_embeddings.py 'machine learning' 3 --csv combined_01_code_generation")
        print("  python search_embeddings.py --list")
        return
    
    # Handle --list option
    if sys.argv[1] == "--list":
        list_available_embeddings()
        return
    
    query = sys.argv[1]
    top_k = 3
    specific_csv = None
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--csv" and i + 1 < len(sys.argv):
            specific_csv = sys.argv[i + 1]
            i += 2
        elif sys.argv[i].isdigit():
            top_k = int(sys.argv[i])
            i += 1
        else:
            i += 1
    
    print(f"Searching for: '{query}' (top {top_k} results)")
    if specific_csv:
        print(f"Searching in: {specific_csv}")
    else:
        print("Searching in: all embeddings")
    print("=" * 50)
    
    # Initialize manager and load embeddings
    manager = EmbeddingManager()
    
    if not manager.load_embeddings():
        print("No embeddings found. Please run create_and_save_embeddings.py first.")
        return
    
    # Perform search
    results = manager.search_embeddings(query, top_k, specific_csv)
    
    if not results:
        print("No results found.")
        return
    
    for result in results:
        print(f"\n🔗 Rank {result['rank']} (Similarity: {result['similarity_score']:.4f})")
        print(f"📋 Task: {result['task']}")
        print(f"🌐 URL: {result['url']}")
        print(f"🗣️  Languages: {result['languages']}")
        print(f"🤖 Models: {result['models']}")
        print(f"📁 Source: {Path(result['source_file']).name}")
        print(f"📄 Description: {result['description']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
