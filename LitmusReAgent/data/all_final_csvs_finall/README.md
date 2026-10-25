# Research Paper Embeddings System

This system processes CSV files containing research paper information and generates embeddings for semantic search. **Each CSV file gets its own separate pickle file saved in the same folder.**

## Overview

The system reads CSV files from subfolders, extracts information about research papers (Task, Languages, Models, URL, Description), and creates embeddings from the combined Description + Models + Languages text. Each CSV file gets its own embedding file saved in the same directory, making it easy to manage embeddings per dataset.

## Files

- `create_and_save_embeddings.py` - Main script for generating and saving embeddings (separate files per CSV)
- `search_embeddings.py` - Command-line interface for searching embeddings (supports specific CSV or all)
- `csv_embedding_utils.py` - Utility script for managing individual CSV embeddings
- `generate_embeddings.bat` - Windows batch file to run embedding generation
- `requirements_embeddings.txt` - Python dependencies
- `README.md` - This file

## File Structure After Processing

```
all_final_csvs_finall/
├── 01_Code_Generation/
│   ├── combined_01_code_generation.csv
│   ├── combined_01_code_generation_embeddings.pkl
│   └── combined_01_code_generation_embeddings.json
├── 02_Math_Reasoning/
│   ├── combined_02_math_reasoning.csv
│   ├── combined_02_math_reasoning_embeddings.pkl
│   └── combined_02_math_reasoning_embeddings.json
└── ...
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements_embeddings.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file with your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_ENDPOINT_EMBEDDING=your_endpoint_here
   AZURE_OPENAI_API_KEY_EMBEDDING=your_api_key_here
   ```

## Usage

### Generate Embeddings

**Option 1: Run the Python script directly**
```bash
python create_and_save_embeddings.py
```

**Option 2: Use the batch file (Windows)**
```bash
generate_embeddings.bat
```

This will:
- Scan all subfolders for CSV files
- Process each CSV file with columns: Task, Languages, Models, URL, Description
- Generate embeddings for each row (combining Description + Models + Languages)
- Save separate embedding files for each CSV in their respective folders:
  - `{csv_name}_embeddings.pkl` - Binary embedding data
  - `{csv_name}_embeddings.json` - Human-readable metadata
- Also save a combined file with all embeddings: `all_embeddings_combined.pkl`

### Search Embeddings

**Search in all embeddings:**
```bash
python search_embeddings.py "python code generation" 3
```

**Search in specific CSV embeddings:**
```bash
python search_embeddings.py "multilingual math reasoning" 5 --csv combined_01_code_generation
```

**List available embedding files:**
```bash
python search_embeddings.py --list
```

### Manage Individual CSV Embeddings

**List all CSV files and their embedding status:**
```bash
python csv_embedding_utils.py list
```

**Search in specific CSV only:**
```bash
python csv_embedding_utils.py search 01_Code_Generation combined_01_code_generation "python code" 5
```

**Regenerate embeddings for a specific CSV:**
```bash
python csv_embedding_utils.py regen 01_Code_Generation/combined_01_code_generation.csv
```

**Programmatic search in all embeddings:**
```python
from create_and_save_embeddings import search_interface

# Search for top 3 results across all embeddings
results = search_interface("machine learning benchmarks", top_k=3)

for result in results:
    print(f"URL: {result['url']}")
    print(f"Task: {result['task']}")
    print(f"Similarity: {result['similarity_score']}")
```

**Load and search specific CSV embeddings:**
```python
from create_and_save_embeddings import load_specific_csv_embeddings, EmbeddingManager

# Load embeddings for a specific CSV
embeddings = load_specific_csv_embeddings("01_Code_Generation", "combined_01_code_generation")

# Or use the manager for more advanced operations
manager = EmbeddingManager()
manager.load_embeddings()  # Load all embeddings

# Search in specific CSV
results = manager.search_embeddings("deep learning", top_k=5, 
                                   specific_csv="01_Code_Generation/combined_01_code_generation.csv")
```

## Expected CSV Format

Each CSV file should have these columns:
- **Task**: The type of task (e.g., "Code Generation", "Math Reasoning")
- **Languages**: Programming or natural languages involved
- **Models**: AI models used or evaluated
- **URL**: Link to the research paper or resource
- **Description**: Detailed description of the research

Example:
```csv
Task,Languages,Models,URL,Description
Code Generation,"Python, Java","GPT-4, Claude-3",https://example.com,"Description of the research..."
```

## Output Files

**Per CSV files:**
- `{csv_name}_embeddings.pkl` - Binary file containing embeddings and metadata for that specific CSV
- `{csv_name}_embeddings.json` - Human-readable metadata file for that specific CSV

**Combined files:**
- `all_embeddings_combined.pkl` - Binary file containing all embeddings from all CSVs
- `all_embeddings_combined.json` - Human-readable metadata for all embeddings
- Console output showing processing progress and statistics

## Search Results Format

Each search result includes:
- **rank**: Position in results (1, 2, 3...)
- **similarity_score**: Cosine similarity score (0.0 to 1.0)
- **url**: Link to the research paper
- **task**: Research task type
- **languages**: Languages involved
- **models**: AI models mentioned
- **description**: Truncated description
- **source_file**: Which CSV file the result came from

## Benefits of Separate Pickle Files

1. **Faster Loading**: Load only the embeddings you need for specific datasets
2. **Better Organization**: Each dataset has its own embedding file in its folder
3. **Easier Management**: Regenerate embeddings for specific CSVs without affecting others
4. **Selective Search**: Search within specific domains or across all domains
5. **Reduced Memory Usage**: Load only what you need for targeted searches

## Performance Notes

- Embedding generation can take time depending on the number of CSV rows
- The system uses Azure OpenAI's text-embedding-ada-002 model
- Embeddings are cached in pickle format for fast loading
- Search is performed using cosine similarity

## Troubleshooting

1. **Missing environment variables**: Ensure your .env file contains the correct Azure OpenAI credentials
2. **CSV format issues**: Check that your CSV files have the required columns
3. **Memory issues**: For large datasets, consider processing files in batches
4. **No search results**: Ensure embeddings have been generated and saved properly

## Examples

### Generate embeddings for all CSV files:
```bash
python create_and_save_embeddings.py
```

### Search for Python-related research:
```bash
python search_embeddings.py "python programming evaluation" 5
```

### Search for multilingual benchmarks:
```bash
python search_embeddings.py "multilingual language model benchmark" 3
```
