
import os
import pandas as pd
import numpy as np
import pickle
import json
from typing import List, Dict, Tuple
from openai import AzureOpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import glob
from pathlib import Path

# Configuration: Skip processing if pickle file already exists
# Set to False to always regenerate embeddings, True to skip existing ones
SKIP_IF_PKL_EXISTS = True

load_dotenv()

client_embedding = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDING"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY_EMBEDDING"),
    api_version="2025-01-01-preview"
)


def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Retrieve the OpenAI embedding for a single piece of text.
    """
    try:
        resp = client_embedding.embeddings.create(input=[text], model=model)
        return resp.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding for text: {e}")
        return None


class EmbeddingManager:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.all_embeddings_data = {}  # Dict with csv_file as key and embeddings list as value
        
    def create_text_for_embedding(self, row: pd.Series) -> str:
        """
        Create text for embedding by concatenating Description + Models + Languages
        """
        description = str(row.get('Description', ''))
        models = str(row.get('Models', ''))
        languages = str(row.get('Languages', ''))
        
        # Create a comprehensive text for embedding
        text = f"Description: {description}\n\nModels: {models}\n\nLanguages: {languages}"
        return text.strip()
    
    def process_csv_files(self, force_regenerate=False):
        """
        Process all CSV files in subfolders and generate embeddings
        Save separate pickle file for each CSV in its folder
        
        Args:
            force_regenerate (bool): If True, regenerate embeddings even if pkl files exist
        """
        print("Starting to process CSV files...")
        
        if force_regenerate:
            print("Force regeneration enabled - will recreate all embeddings")
        
        # Find all CSV files in subfolders
        csv_pattern = str(self.base_dir / "*" / "*.csv")
        csv_files = glob.glob(csv_pattern)
        
        print(f"Found {len(csv_files)} CSV files")
        
        total_processed = 0
        skipped_count = 0
        
        for csv_file in csv_files:
            print(f"\nProcessing: {csv_file}")
            
            # Get the folder path for this CSV
            csv_path = Path(csv_file)
            csv_folder = csv_path.parent
            csv_name = csv_path.stem
            
            # Check if pickle file already exists (if enabled and not forcing regeneration)
            pkl_file = csv_folder / f"{csv_name}_embeddings.pkl"
            if not force_regenerate and SKIP_IF_PKL_EXISTS and pkl_file.exists():
                print(f"  Pickle file already exists: {pkl_file}")
                print(f"  Skipping {csv_file} (embeddings already generated)")
                skipped_count += 1
                
                # Still load existing embeddings for combined operations if needed
                try:
                    with open(pkl_file, 'rb') as f:
                        existing_embeddings = pickle.load(f)
                    self.all_embeddings_data[csv_file] = existing_embeddings
                    print(f"  Loaded {len(existing_embeddings)} existing embeddings")
                except Exception as e:
                    print(f"  Warning: Could not load existing embeddings: {e}")
                continue
            
            try:
                df = pd.read_csv(csv_file)
                
                # Check if required columns exist
                required_cols = ['Task', 'Languages', 'Models', 'URL', 'Description']
                if not all(col in df.columns for col in required_cols):
                    print(f"Skipping {csv_file}: Missing required columns")
                    print(f"Available columns: {list(df.columns)}")
                    continue
                
                # Initialize embeddings list for this CSV
                csv_embeddings = []
                
                # Process each row
                for idx, row in df.iterrows():
                    # Create text for embedding
                    embedding_text = self.create_text_for_embedding(row)
                    
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
                            'source_file': csv_file,
                            'row_index': idx,
                            'embedding_text': embedding_text
                        }
                        
                        csv_embeddings.append(embedding_data)
                        total_processed += 1
                    else:
                        print(f"  Failed to generate embedding for row {idx + 1}")
                
                # Save embeddings for this CSV file
                if csv_embeddings:
                    self.save_csv_embeddings(csv_embeddings, csv_folder, csv_name)
                    
                # Store in all_embeddings_data for combined operations if needed
                self.all_embeddings_data[csv_file] = csv_embeddings
                        
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
                continue
        
        print(f"\nTotal embeddings generated: {total_processed}")
        if skipped_count > 0:
            print(f"Total CSV files skipped (already had embeddings): {skipped_count}")
        return total_processed
    
    def save_csv_embeddings(self, embeddings_data: List[Dict], csv_folder: Path, csv_name: str):
        """
        Save embeddings for a specific CSV file in its own folder
        """
        try:
            # Create pickle file path in the same folder as the CSV
            pkl_file = csv_folder / f"{csv_name}_embeddings.pkl"
            
            with open(pkl_file, 'wb') as f:
                pickle.dump(embeddings_data, f)
            print(f"  Embeddings saved to {pkl_file}")
            
            # Also save metadata as JSON for easy inspection
            json_file = csv_folder / f"{csv_name}_embeddings.json"
            metadata = []
            for item in embeddings_data:
                metadata_item = {k: v for k, v in item.items() if k != 'embedding'}
                metadata_item['embedding_dim'] = len(item['embedding']) if item['embedding'] else 0
                metadata.append(metadata_item)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"  Metadata saved to {json_file}")
            
        except Exception as e:
            print(f"  Error saving embeddings for {csv_name}: {e}")
    
    def save_embeddings(self):
        """
        Save all embeddings to a combined file (legacy method)
        """
        # Combine all embeddings from all CSV files
        all_embeddings = []
        for csv_file, embeddings in self.all_embeddings_data.items():
            all_embeddings.extend(embeddings)
        
        if not all_embeddings:
            print("No embeddings to save")
            return
            
        try:
            combined_file = self.base_dir / "all_embeddings_combined.pkl"
            with open(combined_file, 'wb') as f:
                pickle.dump(all_embeddings, f)
            print(f"Combined embeddings saved to {combined_file}")
            
            # Also save metadata as JSON for easy inspection
            metadata_file = self.base_dir / "all_embeddings_combined.json"
            metadata = []
            for item in all_embeddings:
                metadata_item = {k: v for k, v in item.items() if k != 'embedding'}
                metadata_item['embedding_dim'] = len(item['embedding']) if item['embedding'] else 0
                metadata.append(metadata_item)
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"Combined metadata saved to {metadata_file}")
            
        except Exception as e:
            print(f"Error saving combined embeddings: {e}")
    
    def load_embeddings(self, embeddings_file: str = None):
        """
        Load embeddings from file (supports both individual and combined files)
        """
        if embeddings_file:
            # Load specific file
            try:
                with open(embeddings_file, 'rb') as f:
                    embeddings_data = pickle.load(f)
                print(f"Loaded {len(embeddings_data)} embeddings from {embeddings_file}")
                return embeddings_data
            except Exception as e:
                print(f"Error loading embeddings from {embeddings_file}: {e}")
                return None
        else:
            # Load all individual CSV embedding files
            self.all_embeddings_data = {}
            total_loaded = 0
            
            csv_pattern = str(self.base_dir / "*" / "*_embeddings.pkl")
            pkl_files = glob.glob(csv_pattern)
            
            for pkl_file in pkl_files:
                try:
                    with open(pkl_file, 'rb') as f:
                        embeddings_data = pickle.load(f)
                    self.all_embeddings_data[pkl_file] = embeddings_data
                    total_loaded += len(embeddings_data)
                    print(f"Loaded {len(embeddings_data)} embeddings from {pkl_file}")
                except Exception as e:
                    print(f"Error loading {pkl_file}: {e}")
            
            print(f"Total embeddings loaded: {total_loaded}")
            return total_loaded > 0
    
    def search_embeddings(self, query_text: str, top_k: int = 3, specific_csv: str = None) -> List[Dict]:
        """
        Search for similar embeddings and return top_k results with URLs
        Can search in all embeddings or specific CSV embeddings
        """
        # Determine which embeddings to search
        if specific_csv and specific_csv in self.all_embeddings_data:
            search_data = self.all_embeddings_data[specific_csv]
            print(f"Searching in {specific_csv} ({len(search_data)} embeddings)")
        else:
            # Combine all embeddings
            search_data = []
            for csv_file, embeddings in self.all_embeddings_data.items():
                search_data.extend(embeddings)
            print(f"Searching in all embeddings ({len(search_data)} total)")
        
        if not search_data:
            print("No embeddings loaded. Please load or generate embeddings first.")
            return []
        
        # Generate embedding for query
        query_embedding = get_embedding(query_text)
        if query_embedding is None:
            print("Failed to generate embedding for query")
            return []
        
        # Calculate similarities
        similarities = []
        for i, item in enumerate(search_data):
            if item['embedding'] is not None:
                similarity = cosine_similarity(
                    [query_embedding], 
                    [item['embedding']]
                )[0][0]
                similarities.append((i, similarity))
        
        # Sort by similarity and get top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for i, (idx, sim_score) in enumerate(similarities[:top_k]):
            result = {
                'rank': i + 1,
                'similarity_score': sim_score,
                'url': search_data[idx]['url'],
                'task': search_data[idx]['task'],
                'languages': search_data[idx]['languages'],
                'models': search_data[idx]['models'],
                'description': search_data[idx]['description'][:200] + "..." if len(search_data[idx]['description']) > 200 else search_data[idx]['description'],
                'source_file': search_data[idx]['source_file']
            }
            results.append(result)
        
        return results
    
    def get_statistics(self):
        """
        Get statistics about the embeddings
        """
        if not self.all_embeddings_data:
            return None
        
        # Combine all embeddings for statistics
        all_embeddings = []
        for csv_file, embeddings in self.all_embeddings_data.items():
            all_embeddings.extend(embeddings)
        
        stats = {
            'total_embeddings': len(all_embeddings),
            'unique_tasks': len(set(item['task'] for item in all_embeddings)),
            'unique_urls': len(set(item['url'] for item in all_embeddings)),
            'csv_files_processed': len(self.all_embeddings_data),
            'embeddings_per_csv': {csv_file: len(embeddings) for csv_file, embeddings in self.all_embeddings_data.items()}
        }
        
        return stats


def main():
    """
    Main function to create and save embeddings
    """
    # Initialize embedding manager
    manager = EmbeddingManager(base_dir=".")  # Current directory (all_final_csvs_finall)
    
    print("=== Research Paper Embeddings Generator ===")
    print("This will process all CSV files in subfolders and generate embeddings")
    print("for Description + Models + Languages content.")
    print("Each CSV will have its own pickle file saved in its folder.")
    if SKIP_IF_PKL_EXISTS:
        print("Configuration: Will skip CSV files that already have corresponding .pkl files")
    else:
        print("Configuration: Will regenerate embeddings even if .pkl files exist")
    print()
    
    # Process CSV files and generate embeddings
    processed_count = manager.process_csv_files()
    
    if processed_count > 0 or manager.all_embeddings_data:
        # Save combined embeddings as well (optional)
        manager.save_embeddings()
        
        # Show statistics
        stats = manager.get_statistics()
        if stats:
            print(f"\n=== Statistics ===")
            print(f"Total embeddings: {stats['total_embeddings']}")
            print(f"Unique tasks: {stats['unique_tasks']}")
            print(f"Unique URLs: {stats['unique_urls']}")
            print(f"CSV files processed: {stats['csv_files_processed']}")
            
            print(f"\n=== Embeddings per CSV ===")
            for csv_file, count in stats['embeddings_per_csv'].items():
                print(f"  {Path(csv_file).name}: {count} embeddings")
            
            # Example search
            print(f"\n=== Example Search ===")
            print("Performing example search for 'python code generation'...")
            results = manager.search_embeddings("python code generation", top_k=3)
            
            for result in results:
                print(f"\nRank {result['rank']} (Similarity: {result['similarity_score']:.4f})")
                print(f"Task: {result['task']}")
                print(f"URL: {result['url']}")
                print(f"Languages: {result['languages']}")
                print(f"Models: {result['models']}")
                print(f"Source: {Path(result['source_file']).name}")
                print(f"Description: {result['description']}")
    else:
        print("No embeddings were generated or loaded. Please check your CSV files.")


def main_force_regenerate():
    """
    Main function to create and save embeddings with forced regeneration
    """
    # Initialize embedding manager
    manager = EmbeddingManager(base_dir=".")  # Current directory (all_final_csvs_finall)
    
    print("=== Research Paper Embeddings Generator (FORCE REGENERATE) ===")
    print("This will process all CSV files in subfolders and generate embeddings")
    print("for Description + Models + Languages content.")
    print("Each CSV will have its own pickle file saved in its folder.")
    print("Configuration: FORCE REGENERATE - Will recreate all embeddings even if .pkl files exist")
    print()
    
    # Process CSV files and generate embeddings with force regeneration
    processed_count = manager.process_csv_files(force_regenerate=True)
    
    if processed_count > 0:
        # Save combined embeddings as well (optional)
        manager.save_embeddings()
        
        # Show statistics
        stats = manager.get_statistics()
        print(f"\n=== Statistics ===")
        print(f"Total embeddings: {stats['total_embeddings']}")
        print(f"Unique tasks: {stats['unique_tasks']}")
        print(f"Unique URLs: {stats['unique_urls']}")
        print(f"CSV files processed: {stats['csv_files_processed']}")
        
        print(f"\n=== Embeddings per CSV ===")
        for csv_file, count in stats['embeddings_per_csv'].items():
            print(f"  {Path(csv_file).name}: {count} embeddings")
        
        # Example search
        print(f"\n=== Example Search ===")
        print("Performing example search for 'python code generation'...")
        results = manager.search_embeddings("python code generation", top_k=3)
        
        for result in results:
            print(f"\nRank {result['rank']} (Similarity: {result['similarity_score']:.4f})")
            print(f"Task: {result['task']}")
            print(f"URL: {result['url']}")
            print(f"Languages: {result['languages']}")
            print(f"Models: {result['models']}")
            print(f"Source: {Path(result['source_file']).name}")
            print(f"Description: {result['description']}")
    else:
        print("No embeddings were generated. Please check your CSV files.")


def search_interface(query: str, top_k: int = 3, specific_csv: str = None):
    """
    Simple interface function for searching embeddings
    """
    manager = EmbeddingManager()
    
    if not manager.load_embeddings():
        print("No embeddings found. Please run main() first to generate embeddings.")
        return []
    
    return manager.search_embeddings(query, top_k, specific_csv)


def load_specific_csv_embeddings(csv_folder: str, csv_name: str):
    """
    Load embeddings for a specific CSV file
    """
    pkl_file = Path(csv_folder) / f"{csv_name}_embeddings.pkl"
    
    try:
        with open(pkl_file, 'rb') as f:
            embeddings_data = pickle.load(f)
        print(f"Loaded {len(embeddings_data)} embeddings from {pkl_file}")
        return embeddings_data
    except Exception as e:
        print(f"Error loading embeddings from {pkl_file}: {e}")
        return None


if __name__ == "__main__":
    main()