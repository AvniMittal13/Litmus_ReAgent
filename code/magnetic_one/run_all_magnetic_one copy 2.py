import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import venv

from autogen_ext.auth.azure import AzureTokenProvider
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from autogen_agentchat.ui import Console
from autogen_ext.teams.magentic_one import MagenticOne


load_dotenv()
print(os.getenv("OPENAI_BASE_URL", "gpt-4.1"),)


# Task mapping
TASK_MAPPING = {
    "1": "01_Code_Generation",
    "2": "02_Math_Reasoning", 
    "3": "03_QA_VQA",
    "4": "04_Classification_NLI",
    "5": "05_Text_Summarization",
    "6": "06_Machine_Translation"
}

TASK_NAMES = {
    "01_Code_Generation": "code_generation",
    "02_Math_Reasoning": "math_reasoning",
    "03_QA_VQA": "question_answering", 
    "04_Classification_NLI": "text_classification",
    "05_Text_Summarization": "text_summarization",
    "06_Machine_Translation": "machine_translation"
}

SCENARIO_MAPPING = {
    "scenario1": "GT_available",
    "scenario2": "Context_available", 
    "scenario3": "Baseline_comparison",
    "scenario4": "Performance_analysis",
    "scenario5": "Cross_lingual_evaluation"
}

SCENARIO_DESCRIPTIONS = {
    "1": ("scenario1", "GT_available - Ground truth available for evaluation"),
    "2": ("scenario2", "Context_available - Contextual information provided"),
    "3": ("scenario3", "Baseline_comparison - Compare against baseline models"),
    "4": ("scenario4", "Performance_analysis - Analyze performance metrics"),
    "5": ("scenario5", "Cross_lingual_evaluation - Cross-language evaluation")
}

class MagneticOneRunner:
    def __init__(self):
        print("Initializing MagneticOne Runner...")
        
        # Create the token provider
        # try:
        #     self.token_provider = AzureTokenProvider(
        #         DefaultAzureCredential(),
        #         "https://cognitiveservices.azure.com/.default",
        #     )
        # except Exception as e:
        #     print(f"Warning: Could not create token provider: {e}")
        #     self.token_provider = None

        try:
            from autogen_ext.auth.azure import AzureTokenProvider
            _token_provider = AzureTokenProvider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default",
            )
            self.model_client = AzureOpenAIChatCompletionClient(
                azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4.1"),
                model=os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4.1"),
                api_version=os.getenv("OPENAI_API_VERSION", "2025-01-01-preview"),
                azure_endpoint=os.getenv("OPENAI_BASE_URL", "https://YOUR_AZURE_OPENAI_ENDPOINT.openai.azure.com/"),
                azure_ad_token_provider=_token_provider,
            )
            print("✅ Model client initialized successfully (Azure AD token auth)")
        except Exception as e:
            print(f"❌ Failed to initialize model client: {e}")
            raise

        # Setup code executor with virtual environment
        self.work_dir = Path("magnetic_one_coding_ijcai")
        self.work_dir.mkdir(exist_ok=True)

        self.venv_dir = "./venv"
        venv_builder = venv.EnvBuilder(with_pip=True)
        self.venv_context = venv_builder.ensure_directories(self.venv_dir)

        self.local_executor = LocalCommandLineCodeExecutor(
            work_dir=self.work_dir, 
            virtual_env_context=self.venv_context
        )
        print("✅ Code executor initialized with virtual environment")

        # Update the questions directory path
        self.generated_questions_dir = Path("./generated_questions")
        self.results_dir = Path("./final_testing_codes\\FINAL_RUS\\Magentic_one_final")
        
        # Create results directory if it doesn't exist
        self.results_dir.mkdir(exist_ok=True)
        print(f"✅ Results will be saved to: {self.results_dir.absolute()}")
        print(f"✅ Questions will be loaded from: {self.generated_questions_dir.absolute()}")

    def display_scenario_info(self):
        """Display available scenarios with descriptions"""
        print("\n" + "="*60)
        print("Available Scenarios:")
        print("="*60)
        for num, (scenario_id, description) in SCENARIO_DESCRIPTIONS.items():
            print(f"{num}. {description}")
        print("="*60)

    def get_scenario_selection(self):
        """Get user's scenario selection"""
        print("\nSelect scenarios to process:")
        print("  - Enter specific numbers (e.g., '1,3,5')")
        print("  - Enter 'all' to process all scenarios")
        
        while True:
            try:
                choice = input("\nScenario selection: ").strip().lower()
                
                if choice == 'all':
                    return list(SCENARIO_DESCRIPTIONS.keys())
                
                # Parse comma-separated numbers
                selected = [s.strip() for s in choice.split(',')]
                
                # Validate all selections
                invalid = [s for s in selected if s not in SCENARIO_DESCRIPTIONS]
                if invalid:
                    print(f"Invalid scenario(s): {', '.join(invalid)}. Please enter numbers 1-5.")
                    continue
                
                return selected
                
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)

    def display_task_menu(self):
        """Display available tasks for selection"""
        print("\n" + "="*60)
        print("Available Tasks:")
        print("="*60)
        print("1. Code Generation (50 questions)")
        print("2. Math Reasoning (40 questions)")
        print("3. Question Answering (50 questions)")
        print("4. Text Classification (50 questions)")
        print("5. Text Summarization (50 questions)")
        print("6. Machine Translation (50 questions)")
        print("7. Rerun failed questions only")
        print("8. Show error statistics")
        print("0. Exit")
        print("="*60)

    def get_task_selection(self):
        """Get user's task selection"""
        while True:
            try:
                choice = input("\nSelect a task (1-8) or 0 to exit: ").strip()
                if choice == "0":
                    print("Exiting...")
                    sys.exit(0)
                elif choice == "7":
                    return "rerun_errors"
                elif choice == "8":
                    return "show_stats"
                elif choice in TASK_MAPPING:
                    return TASK_MAPPING[choice]
                else:
                    print("Invalid choice. Please enter a number between 0-8.")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)

    def find_question_files(self, task_id, selected_scenarios=None):
        """Find all JSON files for the selected task and scenarios
        
        Args:
            task_id: Task identifier
            selected_scenarios: List of scenario numbers (e.g., ['1', '3', '5']) or None for all
        """
        question_files = []
        pattern = f"{task_id}_questions_scenario*.json"
        
        for file_path in self.generated_questions_dir.glob(pattern):
            # If specific scenarios selected, filter by them
            if selected_scenarios:
                # Extract scenario number from filename (e.g., 'scenario1' -> '1')
                scenario_match = file_path.stem.split('_')[-1]  # Gets 'scenario1', 'scenario2', etc.
                scenario_num = scenario_match.replace('scenario', '')  # Gets '1', '2', etc.
                
                if scenario_num in selected_scenarios:
                    question_files.append(file_path)
            else:
                question_files.append(file_path)
        
        question_files.sort()  # Sort to ensure consistent ordering
        return question_files

    def check_for_errors_in_results(self, task_name, scenario_name):
        """Check for existing results with errors that need to be rerun"""
        error_questions = []
        
        scenario_folder = self.results_dir / task_name / scenario_name
        if not scenario_folder.exists():
            return error_questions
        
        # Check each question folder for errors in metadata.json
        for question_folder in scenario_folder.iterdir():
            if question_folder.is_dir():
                metadata_file = question_folder / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        # Check if there was an error (success=False or error is not None)
                        if not metadata.get('success', True) or metadata.get('error') is not None:
                            error_questions.append({
                                'question_id': metadata.get('question_id'),
                                'question_text': metadata.get('question_text'),
                                'error': metadata.get('error'),
                                'folder_path': question_folder
                            })
                    except Exception as e:
                        print(f"    ⚠️ Error reading metadata from {metadata_file}: {e}")
        
        return error_questions

    def should_rerun_question(self, task_name, scenario_name, question_id):
        """Check if a question should be rerun based on existing results"""
        question_folder = self.results_dir / task_name / scenario_name / question_id
        metadata_file = question_folder / "metadata.json"
        
        if not metadata_file.exists():
            return True  # No existing result, should run
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Rerun if there was an error (success=False or error is not None)
            return not metadata.get('success', True) or metadata.get('error') is not None
        except Exception as e:
            print(f"    ⚠️ Error reading metadata from {metadata_file}: {e}")
            return True  # If can't read metadata, assume should rerun

    def show_error_statistics(self, task_id):
        """Show statistics about errors for a specific task"""
        task_name = TASK_NAMES[task_id]
        task_folder = self.results_dir / task_name
        
        if not task_folder.exists():
            print(f"No results found for task: {task_name}")
            return
        
        print(f"\n📊 Error Statistics for {task_name}")
        print("="*60)
        
        total_questions = 0
        total_errors = 0
        scenario_stats = {}
        
        # Check each scenario
        for scenario_folder in task_folder.iterdir():
            if scenario_folder.is_dir():
                scenario_name = scenario_folder.name
                scenario_questions = 0
                scenario_errors = 0
                error_types = {}
                
                # Check each question in this scenario
                for question_folder in scenario_folder.iterdir():
                    if question_folder.is_dir():
                        metadata_file = question_folder / "metadata.json"
                        if metadata_file.exists():
                            try:
                                with open(metadata_file, 'r', encoding='utf-8') as f:
                                    metadata = json.load(f)
                                
                                scenario_questions += 1
                                total_questions += 1
                                
                                if not metadata.get('success', True) or metadata.get('error') is not None:
                                    scenario_errors += 1
                                    total_errors += 1
                                    
                                    # Categorize error type
                                    error_msg = metadata.get('error', '')
                                    if 'RateLimitError' in error_msg or '429' in error_msg:
                                        error_types['Rate Limit'] = error_types.get('Rate Limit', 0) + 1
                                    elif 'timeout' in error_msg.lower():
                                        error_types['Timeout'] = error_types.get('Timeout', 0) + 1
                                    elif 'connection' in error_msg.lower():
                                        error_types['Connection'] = error_types.get('Connection', 0) + 1
                                    else:
                                        error_types['Other'] = error_types.get('Other', 0) + 1
                                        
                            except Exception as e:
                                print(f"    ⚠️ Error reading {metadata_file}: {e}")
                
                scenario_stats[scenario_name] = {
                    'total': scenario_questions,
                    'errors': scenario_errors,
                    'error_types': error_types
                }
        
        # Display results
        print(f"Total Questions: {total_questions}")
        print(f"Total Errors: {total_errors}")
        print(f"Success Rate: {((total_questions - total_errors) / total_questions * 100):.1f}%" if total_questions > 0 else "No data")
        print()
        
        for scenario_name, stats in scenario_stats.items():
            print(f"📁 {scenario_name}:")
            print(f"  Questions: {stats['total']}, Errors: {stats['errors']}")
            if stats['error_types']:
                for error_type, count in stats['error_types'].items():
                    print(f"    - {error_type}: {count}")
            print()
        
        print("="*60)

    def load_questions_from_file(self, file_path):
        """Load questions from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('questions', [])
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []

    async def run_magnetic_one_for_question(self, question_data):
        """Run MagneticOne for a single question"""
        try:
            print("    🔄 Initializing MagneticOne...")
            m1 = MagenticOne(
                client=self.model_client,
                code_executor=self.local_executor
            )
            
            task = question_data.get('complete_question', '')
            if not task:
                return None, "No question found"
            
            print(f"    🤖 Running MagneticOne...")

            task = f"""
Answer the following question by searching on the web and gathering detailed data taxonomy. If data is not availabe directly then perform predictive analysis by training regression models using code execution. Gather the feature information for regression models from web search.

Question : {task}
"""
            
            result = await Console(m1.run_stream(task=task))
            
            if result and result.messages:
                return result.messages[-1].content, None
            else:
                return None, "No result generated"
                
        except Exception as e:
            return None, str(e)

    def save_result(self, task_name, scenario_name, question_id, question_text, result, error=None):
        """Save the result to the appropriate folder structure"""
        # Create folder structure: taskname/scenario_name/question_id/
        task_folder = self.results_dir / task_name
        scenario_folder = task_folder / scenario_name
        question_folder = scenario_folder / question_id
        question_folder.mkdir(parents=True, exist_ok=True)
        
        # Create report.md file with the final response
        report_file = question_folder / "report.md"
        
        # Create JSON metadata file
        metadata_file = question_folder / "metadata.json"
        
        # Prepare metadata
        metadata = {
            "question_id": question_id,
            "question_text": question_text,
            "task": task_name,
            "scenario": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "success": error is None,
            "error": error
        }
        
        try:
            # Save the main response as report.md
            with open(report_file, 'w', encoding='utf-8') as f:
                # f.write(f"# MagneticOne Response Report\n\n")
                # f.write(f"**Question ID:** {question_id}\n\n")
                # f.write(f"**Task:** {task_name}\n\n")
                 # f.write(f"**Scenario:** {scenario_name}\n\n")
                # f.write(f"**Timestamp:** {datetime.now().isoformat()}\n\n")
                f.write(f"## Question\n\n{question_text}\n\n")
                
                if error:
                    f.write(f"## Error\n\n```\n{error}\n```\n\n")
                    f.write("## Response\n\nNo response generated due to error.\n")
                else:
                    f.write(f"## Response\n\n{result}\n")
            
            # Save metadata as JSON
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"    💾 Report saved to: {report_file}")
            print(f"    📋 Metadata saved to: {metadata_file}")
            return True
            
        except Exception as e:
            print(f"    ❌ Error saving result for {question_id}: {e}")
            return False

    async def process_task(self, task_id, max_questions_per_scenario=None, rerun_errors_only=False, batch_size=10, selected_scenarios=None):
        """Process all questions for a selected task incrementally across scenarios
        
        Args:
            task_id: Task identifier
            max_questions_per_scenario: Limit questions per scenario (for testing)
            rerun_errors_only: Only process questions with errors
            batch_size: Number of questions to process from each scenario before moving to next (default: 10)
            selected_scenarios: List of scenario numbers to process (e.g., ['1', '3', '5']) or None for all
        """
        task_name = TASK_NAMES[task_id]
        print(f"\nProcessing task: {task_name}")
        if rerun_errors_only:
            print("🔄 RERUN MODE: Only processing questions with errors")
        print(f"📦 BATCH MODE: Processing {batch_size} questions per scenario incrementally")
        
        if selected_scenarios:
            scenario_names = [SCENARIO_DESCRIPTIONS[num][1].split(' - ')[0] for num in selected_scenarios]
            print(f"📋 SCENARIOS: {', '.join(scenario_names)}")
        else:
            print("📋 SCENARIOS: All scenarios")
        
        print("="*60)
        
        # Find all question files for this task
        question_files = self.find_question_files(task_id, selected_scenarios)
        
        if not question_files:
            print(f"No question files found for task: {task_id}")
            return
        
        print(f"Found {len(question_files)} scenario files for this task")
        
        total_questions = 0
        processed_questions = 0
        errors = 0
        skipped_questions = 0
        rerun_questions = 0
        
        # Load and prepare all scenarios first
        scenario_data = []
        for file_path in question_files:
            print(f"\n📁 Loading file: {file_path.name}")
            
            # Extract scenario from filename
            scenario_num = file_path.stem.split('_')[-1]  # Gets 'scenario1', 'scenario2', etc.
            scenario_name = SCENARIO_MAPPING.get(scenario_num, scenario_num)
            
            # Load questions from file
            questions = self.load_questions_from_file(file_path)
            
            # Filter questions based on mode
            if rerun_errors_only:
                # Only process questions that have errors
                error_question_ids = {eq['question_id'] for eq in self.check_for_errors_in_results(task_name, scenario_name)}
                questions = [q for q in questions if q.get('unique_id') in error_question_ids]
                print(f"  🔄 Found {len(questions)} questions with errors to rerun")
            else:
                # Filter out questions that already have successful results
                if not max_questions_per_scenario:
                    questions_to_process = []
                    for question in questions:
                        question_id = question.get('unique_id', '')
                        if self.should_rerun_question(task_name, scenario_name, question_id):
                            questions_to_process.append(question)
                        else:
                            skipped_questions += 1
                    questions = questions_to_process
            
            # Limit questions if specified (for testing)
            if max_questions_per_scenario:
                questions = questions[:max_questions_per_scenario]
                print(f"  🧪 Test mode: limiting to {max_questions_per_scenario} questions")
            
            if len(questions) > 0:
                scenario_data.append({
                    'scenario_name': scenario_name,
                    'questions': questions,
                    'current_index': 0
                })
                print(f"  📊 Loaded {len(questions)} questions for {scenario_name}")
            else:
                print(f"  ℹ️ No questions to process in {scenario_name}")
        
        if skipped_questions > 0:
            print(f"\n⏭️ Total skipped (already successful): {skipped_questions}")
        
        if not scenario_data:
            print("\n❌ No questions to process across all scenarios")
            return
        
        # Process questions in batches across all scenarios
        print(f"\n🔄 Starting incremental processing across {len(scenario_data)} scenarios...")
        batch_num = 0
        
        while any(s['current_index'] < len(s['questions']) for s in scenario_data):
            batch_num += 1
            print(f"\n{'='*60}")
            print(f"📦 BATCH #{batch_num} - Processing up to {batch_size} questions per scenario")
            print(f"{'='*60}")
            
            # Process batch_size questions from each scenario
            for scenario_info in scenario_data:
                scenario_name = scenario_info['scenario_name']
                questions = scenario_info['questions']
                start_idx = scenario_info['current_index']
                
                if start_idx >= len(questions):
                    continue  # This scenario is done
                
                end_idx = min(start_idx + batch_size, len(questions))
                batch_questions = questions[start_idx:end_idx]
                
                print(f"\n📁 {scenario_name} - Processing questions {start_idx+1} to {end_idx} of {len(questions)}")
                
                # Process each question in this batch
                for i, question_data in enumerate(batch_questions, start=start_idx+1):
                    question_id = question_data.get('unique_id', f'unknown_{i}')
                    question_text = question_data.get('complete_question', '')
                    
                    # Check if this is a rerun
                    is_rerun = self.results_dir.joinpath(task_name, scenario_name, question_id, "metadata.json").exists()
                    if is_rerun:
                        rerun_questions += 1
                        print(f"\n  [{i}/{len(questions)}] 🔄 RERUNNING Question ID: {question_id}")
                    else:
                        print(f"\n  [{i}/{len(questions)}] Question ID: {question_id}")
                    
                    print(f"    ❓ Question: {question_text[:100]}...")
                    
                    try:
                        # Run MagneticOne for this question
                        result, error = await self.run_magnetic_one_for_question(question_data)
                        
                        # Save result
                        if self.save_result(task_name, scenario_name, question_id, question_text, result, error):
                            if error:
                                print(f"    ❌ Error: {error}")
                                errors += 1
                            else:
                                print(f"    ✅ Completed successfully")
                                processed_questions += 1
                        else:
                            print(f"    ❌ Failed to save result")
                            errors += 1
                            
                    except Exception as e:
                        print(f"    ❌ Exception: {e}")
                        self.save_result(task_name, scenario_name, question_id, question_text, None, str(e))
                        errors += 1
                    
                    total_questions += 1
                    
                    # Small delay to avoid overwhelming the system
                    await asyncio.sleep(2)
                
                # Update the current index for this scenario
                scenario_info['current_index'] = end_idx
            
            # Show progress after each batch round
            remaining_questions = sum(len(s['questions']) - s['current_index'] for s in scenario_data)
            print(f"\n📊 Batch #{batch_num} Complete - Remaining questions: {remaining_questions}")
        
        # Summary
        print(f"\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Task: {task_name}")
        if rerun_errors_only:
            print("Mode: Rerun errors only")
        print(f"Batch size: {batch_size} questions per scenario")
        print(f"Total batches processed: {batch_num}")
        print(f"Total questions processed: {total_questions}")
        print(f"Successfully completed: {processed_questions}")
        print(f"Errors: {errors}")
        if not rerun_errors_only:
            print(f"Skipped (already successful): {skipped_questions}")
        if rerun_questions > 0:
            print(f"Rerun attempts: {rerun_questions}")
        print(f"Results saved in: {self.results_dir / task_name}")
        print(f"Structure: {task_name}/scenario_name/question_id/report.md")
        print("="*60)

    async def run(self, test_mode=False):
        """Main execution function"""
        print("MagneticOne Batch Question Processor")
        print("="*60)
        
        # Display available scenarios
        self.display_scenario_info()
        
        if test_mode:
            print("\n🧪 RUNNING IN TEST MODE - Only processing 2 questions per scenario")
        
        while True:
            self.display_task_menu()
            selected_task = self.get_task_selection()
            
            if selected_task == "show_stats":
                print("\n📊 SHOW ERROR STATISTICS")
                print("Select which task to show statistics for:")
                for key, task_id in TASK_MAPPING.items():
                    task_name = TASK_NAMES[task_id]
                    print(f"{key}. {task_name}")
                
                while True:
                    try:
                        stats_choice = input("\nSelect task to show stats (1-6): ").strip()
                        if stats_choice in TASK_MAPPING:
                            selected_task = TASK_MAPPING[stats_choice]
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1-6.")
                    except KeyboardInterrupt:
                        print("\nExiting...")
                        sys.exit(0)
                
                self.show_error_statistics(selected_task)
                
            elif selected_task == "rerun_errors":
                print("\n🔄 RERUN ERRORS MODE")
                print("This will rerun all questions that previously failed with errors.")
                
                # Show available tasks for rerun
                print("\nSelect which task to rerun errors for:")
                for key, task_id in TASK_MAPPING.items():
                    task_name = TASK_NAMES[task_id]
                    print(f"{key}. {task_name}")
                
                while True:
                    try:
                        rerun_choice = input("\nSelect task to rerun errors (1-6): ").strip()
                        if rerun_choice in TASK_MAPPING:
                            selected_task = TASK_MAPPING[rerun_choice]
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1-6.")
                    except KeyboardInterrupt:
                        print("\nExiting...")
                        sys.exit(0)
                
                task_name = TASK_NAMES[selected_task]
                print(f"\nSelected task for error rerun: {task_name}")
                
                confirmation = input(f"Confirm rerunning ONLY failed questions for '{task_name}'? (y/n): ").strip().lower()
                if confirmation in ['y', 'yes']:
                    # Ask for scenario selection
                    selected_scenarios = self.get_scenario_selection()
                    print(f"\nSelected scenarios: {', '.join(selected_scenarios)}")
                    
                    # Ask for batch size
                    batch_size_input = input("Enter batch size (questions per scenario per round, default=10): ").strip()
                    batch_size = int(batch_size_input) if batch_size_input.isdigit() else 10
                    await self.process_task(selected_task, max_questions_per_scenario=None, rerun_errors_only=True, batch_size=batch_size, selected_scenarios=selected_scenarios)
                else:
                    print("Operation cancelled.")
            else:
                task_name = TASK_NAMES[selected_task]
                print(f"\nSelected task: {task_name}")
                
                if test_mode:
                    confirmation = input(f"Run TEST MODE for '{task_name}' (2 questions per scenario)? (y/n): ").strip().lower()
                else:
                    confirmation = input(f"Confirm processing questions for '{task_name}' (will skip successful ones)? (y/n): ").strip().lower()
                
                if confirmation in ['y', 'yes']:
                    # Ask for scenario selection
                    selected_scenarios = self.get_scenario_selection()
                    print(f"\nSelected scenarios: {', '.join(selected_scenarios)}")
                    
                    max_questions = 2 if test_mode else None
                    # Ask for batch size (unless in test mode)
                    if not test_mode:
                        batch_size_input = input("Enter batch size (questions per scenario per round, default=10): ").strip()
                        batch_size = int(batch_size_input) if batch_size_input.isdigit() else 10
                    else:
                        batch_size = 10  # Default for test mode
                    await self.process_task(selected_task, max_questions_per_scenario=max_questions, rerun_errors_only=False, batch_size=batch_size, selected_scenarios=selected_scenarios)
                else:
                    print("Operation cancelled.")
            
            continue_choice = input("\nProcess another task? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                break


def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MagneticOne Runner")
    parser.add_argument('--task', type=str, help='Task number (1-6)')
    parser.add_argument('--scenarios', type=str, default='all', help='Scenarios: "all" or comma-separated like "1,2,3"')
    parser.add_argument('--batch-size', type=int, default=10, help='Batch size (default: 10)')
    parser.add_argument('--auto', action='store_true', help='Run non-interactively')
    parser.add_argument('--test', '-t', action='store_true', help='Test mode (2 questions per scenario)')
    
    args = parser.parse_args()
    
    try:
        runner = MagneticOneRunner()
        
        if args.auto and args.task:
            # Non-interactive mode
            task_id = TASK_MAPPING.get(args.task)
            if not task_id:
                print(f"Invalid task number: {args.task}")
                sys.exit(1)
            
            if args.scenarios == 'all':
                selected_scenarios = list(SCENARIO_DESCRIPTIONS.keys())
            else:
                selected_scenarios = [s.strip() for s in args.scenarios.split(',')]
            
            max_questions = 2 if args.test else None
            print(f"\nAuto mode: Task={task_id}, Scenarios={selected_scenarios}, Batch={args.batch_size}")
            asyncio.run(runner.process_task(task_id, max_questions_per_scenario=max_questions, batch_size=args.batch_size, selected_scenarios=selected_scenarios))
        else:
            asyncio.run(runner.run(test_mode=args.test))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
