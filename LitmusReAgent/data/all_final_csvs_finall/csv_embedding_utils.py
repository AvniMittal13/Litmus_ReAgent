#!/usr/bin/env python3
"""
Utility script for managing individual CSV embeddings.
Provides functions to load, search, and manage embeddings for specific CSV files.
"""

import sys
import os
from pathlib import Path
from create_and_save_embeddings import EmbeddingManager, load_specific_csv_embeddings

def list_csv_embeddings():
    """List all CSV files and their corresponding embedding files"""
    base_dir = Path(".")
    
    print("CSV Files and their Embedding Status:")
    print("=" * 60)
    
    # Find all CSV files in subfolders
    csv_files = list(base_dir.glob("*/*.csv"))
    
    for csv_file in csv_files:
        csv_name = csv_file.stem
        folder_name = csv_file.parent.name
        
        # Check if embedding file exists
        pkl_file = csv_file.parent / f"{csv_name}_embeddings.pkl"
        json_file = csv_file.parent / f"{csv_name}_embeddings.json"
        
        status = "✅" if pkl_file.exists() else "❌"
        
        print(f"{status} {folder_name}/{csv_name}")
        if pkl_file.exists():
            try:
                embeddings = load_specific_csv_embeddings(csv_file.parent, csv_name)
                if embeddings:
                    print(f"    📊 {len(embeddings)} embeddings")
                    print(f"    📁 {pkl_file}")
                    if json_file.exists():
                        print(f"    📄 {json_file}")
            except Exception as e:
                print(f"    ⚠️  Error loading: {e}")
        else:
            print(f"    📁 Expected: {pkl_file}")
        print()

def search_specific_csv(csv_folder, csv_name, query, top_k=3):
    """Search embeddings for a specific CSV file"""
    print(f"Searching in {csv_folder}/{csv_name} for: '{query}'")
    print("=" * 50)
    
    # Load embeddings for specific CSV
    embeddings = load_specific_csv_embeddings(csv_folder, csv_name)
    
    if not embeddings:
        print("No embeddings found for this CSV file.")
        return
    
    # Create a temporary manager for search
    manager = EmbeddingManager()
    manager.all_embeddings_data = {f"{csv_folder}/{csv_name}.csv": embeddings}
    
    # Perform search
    results = manager.search_embeddings(query, top_k)
    
    if not results:
        print("No results found.")
        return
    
    for result in results:
        print(f"\n🔗 Rank {result['rank']} (Similarity: {result['similarity_score']:.4f})")
        print(f"📋 Task: {result['task']}")
        print(f"🌐 URL: {result['url']}")
        print(f"🗣️  Languages: {result['languages']}")
        print(f"🤖 Models: {result['models']}")
        print(f"📄 Description: {result['description']}")
        print("-" * 50)

def regenerate_embeddings_for_csv(csv_file_path):
    """Regenerate embeddings for a specific CSV file"""
    csv_path = Path(csv_file_path)
    
    if not csv_path.exists():
        print(f"CSV file not found: {csv_file_path}")
        return
    
    print(f"Regenerating embeddings for: {csv_path}")
    
    # Create a manager and process just this file
    manager = EmbeddingManager()
    
    # Temporarily modify the process to handle single file
    import pandas as pd
    from create_and_save_embeddings import get_embedding
    
    try:
        df = pd.read_csv(csv_path)
        
        # Check if required columns exist
        required_cols = ['Task', 'Languages', 'Models', 'URL', 'Description']
        if not all(col in df.columns for col in required_cols):
            print(f"Missing required columns. Available: {list(df.columns)}")
            return
        
        csv_embeddings = []
        csv_folder = csv_path.parent
        csv_name = csv_path.stem
        
        print(f"Processing {len(df)} rows...")
        
        # Process each row
        for idx, row in df.iterrows():
            # Create text for embedding
            embedding_text = manager.create_text_for_embedding(row)
            
            # Generate embedding
            print(f"  Generating embedding for row {idx + 1}/{len(df)}")
            embedding = get_embedding(embedding_text)
            
            if embedding is not None:
                # Store embedding with metadata
                embedding_data = {
                    'embedding': embedding,
                    'url': row.get('URL', ''),
                    'task': row.get('Task', ''),
                    'languages': row.get('Languages', ''),
                    'models': row.get('Models', ''),
                    'description': row.get('Description', ''),
                    'source_file': str(csv_path),
                    'row_index': idx,
                    'embedding_text': embedding_text
                }
                
                csv_embeddings.append(embedding_data)
            else:
                print(f"  Failed to generate embedding for row {idx + 1}")
        
        # Save embeddings
        if csv_embeddings:
            manager.save_csv_embeddings(csv_embeddings, csv_folder, csv_name)
            print(f"Successfully saved {len(csv_embeddings)} embeddings")
        else:
            print("No embeddings were generated")
            
    except Exception as e:
        print(f"Error processing {csv_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print("CSV Embedding Management Utility")
        print("=" * 40)
        print("Usage:")
        print("  python csv_embedding_utils.py list")
        print("  python csv_embedding_utils.py search <folder> <csv_name> <query> [top_k]")
        print("  python csv_embedding_utils.py regen <csv_file_path>")
        print()
        print("Examples:")
        print("  python csv_embedding_utils.py list")
        print("  python csv_embedding_utils.py search 01_Code_Generation combined_01_code_generation 'python code' 5")
        print("  python csv_embedding_utils.py regen 01_Code_Generation/combined_01_code_generation.csv")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_csv_embeddings()
    
    elif command == "search":
        if len(sys.argv) < 5:
            print("Usage: python csv_embedding_utils.py search <folder> <csv_name> <query> [top_k]")
            return
        
        folder = sys.argv[2]
        csv_name = sys.argv[3]
        query = sys.argv[4]
        top_k = int(sys.argv[5]) if len(sys.argv) > 5 else 3
        
        search_specific_csv(folder, csv_name, query, top_k)
    
    elif command == "regen":
        if len(sys.argv) < 3:
            print("Usage: python csv_embedding_utils.py regen <csv_file_path>")
            return
        
        csv_file_path = sys.argv[2]
        regenerate_embeddings_for_csv(csv_file_path)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: list, search, regen")

if __name__ == "__main__":
    main()
