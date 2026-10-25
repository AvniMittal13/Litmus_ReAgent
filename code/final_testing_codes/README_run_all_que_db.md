# Task and Scenario Based Question Processor

## Overview

The `run_all_que_db.py` script allows you to run MainAgent for questions from specific tasks and scenarios with configurable database paths and organized output structure.

## Features

### Task Selection (6 options):
1. **01_Code_Generation** - Code generation tasks
2. **02_Math_Reasoning** - Mathematical reasoning tasks  
3. **03_QA_VQA** - Question answering and visual QA tasks
4. **04_Classification_NLI** - Classification and natural language inference tasks
5. **05_Text_Summarization** - Text summarization tasks
6. **06_Machine_Translation** - Machine translation tasks

### Scenario Pairs (2 options):
1. **Scenarios 1 and 2** - First scenario pair
2. **Scenarios 3, 4 and 5** - Second scenario pair

### Case Types (2 options):
1. **Reduced** - Uses reduced dataset (smaller, faster processing)
2. **Combined** - Uses full combined dataset (complete data, longer processing)

## Directory Structure

### Input:
- **Questions**: `generate_questions/generated_questions/`
  - Format: `{TaskName}_questions_scenario{N}.json`
  - Example: `01_Code_Generation_questions_scenario1.json`

- **Database Files**: `all_final_csvs_finall/{TaskName}/`
  - Reduced: `reduced_combined_{taskname}_embeddings.pkl`
  - Combined: `combined_{taskname}_embeddings.pkl`

### Output:
- **Responses**: `final_testing_codes/task_scenario_responses/`
  - Structure: `{TaskName}/ScenarioPair_{N}/{QuestionID}/`
  - Files per question:
    - `response.md` - Agent's response
    - `question_metadata.json` - Question details and processing info
    - `error.txt` - Error info (if processing failed)

## Environment Variables

The script automatically sets the `DB_PATH` environment variable to the complete path of the selected task's database file:

- **Reduced case**: `/path/to/all_final_csvs_finall/{TaskName}/reduced_combined_{taskname}_embeddings.pkl`
- **Combined case**: `/path/to/all_final_csvs_finall/{TaskName}/combined_{taskname}_embeddings.pkl`

## Usage

### 1. Basic Usage
```bash
cd final_testing_codes
python run_all_que_db.py
```

### 2. Interactive Selection Process
The script will prompt you to:
1. Select a task (1-6)
2. Select a scenario pair (1-2) 
3. Select a case type (reduced/combined)
4. Confirm configuration before processing

### 3. Example Session
```
=== Available Tasks ===
1. 01_Code_Generation
2. 02_Math_Reasoning
3. 03_QA_VQA
4. 04_Classification_NLI
5. 05_Text_Summarization
6. 06_Machine_Translation

Select task (1-6): 1

=== Scenario Pairs ===
1. Scenarios 1 and 2
2. Scenarios 3, 4 and 5

Select scenario pair (1-2): 1

=== Case Types ===
1. Reduced
2. Combined

Select case type (1-2): 1

=== Configuration Summary ===
Selected Task: 01_Code_Generation
Scenario Pair: 1 (Scenarios: [1, 2])
Case Type: reduced

Proceed with this configuration? (y/n): y
```

## Processing Details

### What happens during processing:
1. **Database Setup**: Sets `DB_PATH` environment variable
2. **Question Loading**: Loads questions from relevant JSON files
3. **Agent Processing**: 
   - Initializes fresh MainAgent for each question
   - Processes question with formatted prompt
   - Saves response and metadata
   - Cleans up agent to free memory
4. **Progress Tracking**: Saves progress after each question
5. **Error Handling**: Captures and saves error information

### Progress and Logging:
- **Progress File**: `final_testing_codes/task_scenario_progress.json`
- **Log File**: `final_testing_codes/task_scenario_log.txt`
- **Session History**: Tracks all completed sessions

## File Verification

### Available Database Files:
- ✅ 01_Code_Generation (both reduced and combined)
- ✅ 02_Math_Reasoning (both reduced and combined)
- ✅ 03_QA_VQA (both reduced and combined)
- ✅ 04_Classification_NLI (both reduced and combined)
- ✅ 05_Text_Summarization (both reduced and combined)
- ✅ 06_Machine_Translation (combined only, reduced not available)

### Question Files Available:
All tasks have question files for scenarios 1, 2, 3, 4, and 5 (except 02_Math_Reasoning is missing scenario 3).

## Testing

### Test the menu system:
```bash
python test_menu.py
```

### Test database paths:
```bash
python test_db_paths.py
```

## Error Handling

The script includes comprehensive error handling:
- Missing database files (falls back to alternative naming)
- Missing question files (logs warnings)
- Agent initialization failures
- Processing errors (saved to error.txt)
- Progress preservation across interruptions

## Notes

- Each question is processed with a fresh MainAgent instance to prevent memory issues
- Processing can be interrupted (Ctrl+C) and resumed later
- All responses are saved immediately to prevent data loss
- Environment variables are set automatically based on selections
- The script supports both reduced and combined datasets for different processing needs

## Troubleshooting

### Common Issues:
1. **Import Errors**: Ensure all dependencies are installed and agents module is accessible
2. **Missing Files**: Check that database and question files exist in expected locations
3. **Memory Issues**: Script uses fresh agent instances to minimize memory usage
4. **Path Issues**: Script uses absolute paths to avoid navigation problems

### For Support:
Check the log file (`task_scenario_log.txt`) for detailed error information and processing history.
