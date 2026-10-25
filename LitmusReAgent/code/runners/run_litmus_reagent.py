

#!/usr/bin/env python3
"""
Main testing script to run MainAgent for questions from specific tasks and scenarios
with configurable database paths and organized output structure.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import traceback
import time
import shutil

# Configuration: Number of questions to process from each JSON file
MAX_QUESTIONS_PER_JSON = 50

# Add the parent directory to the path to import agents
sys.path.append(str(Path(__file__).parent.parent))

from agents.main_agent_db import MainAgent


class TaskScenarioProcessor:
    """
    Process questions from specific task and scenario combinations using MainAgent.
    """
    
    @staticmethod
    def sanitize_filename(name):
        """Remove invalid characters from filename for Windows compatibility."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        name = name.rstrip('. ')
        if len(name) > 200:
            name = name[:200]
        return name
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.gt_dir = self.base_dir.parent / "data" / "Ground_truths"
        self.questions_dir = self.base_dir / "generated_questions"
        self.responses_base_dir = self.base_dir / "outputs" / "litmus_reagent_1_responses"
        self.progress_file = self.base_dir / "outputs" / "litmus_reagent_1_progress.json"
        self.log_file = self.base_dir / "outputs" / "litmus_reagent_1_log.txt"
        self.db_base_dir = self.base_dir.parent / "data" / "all_final_csvs_finall"
        
        # This will be set during runtime based on case type
        self.current_responses_dir = self.responses_base_dir
        
        # Task mappings
        self.tasks = {
            1: "01_Code_Generation",
            2: "02_Math_Reasoning", 
            3: "03_QA_VQA",
            4: "04_Classification_NLI",
            5: "05_Text_Summarization",
            6: "06_Machine_Translation"
        }
        
        # Scenario pair mappings
        self.scenario_pairs = {
            1: [1, 2],  # Scenarios 1, 2, 3, 4 and 5
            2: [3, 4, 5]  # Scenarios 3, 4 and 5
            # 2: [2,3]
        }
        
        # Ensure directories exist
        self.responses_base_dir.mkdir(parents=True, exist_ok=True)
        (self.base_dir / "outputs").mkdir(parents=True, exist_ok=True)
        
        # Initialize progress tracking
        self.progress = self.load_progress()
        
        # MainAgent will be initialized fresh for each question
        self.main_agent = None
    
    def set_responses_directory(self, case_type):
        """Set the appropriate responses directory based on case type."""
        if case_type == "combined":
            self.current_responses_dir = self.base_dir / "outputs" / "task_scenario_new_final_2_responses_combined"
        else:
            self.current_responses_dir = self.responses_base_dir
        
        # Ensure the directory exists
        self.current_responses_dir.mkdir(parents=True, exist_ok=True)
        self.log(f"Set responses directory to: {self.current_responses_dir}")
        
    def load_progress(self):
        """Load progress from file or create new progress tracking."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.log(f"Error loading progress: {e}")
                return self.create_new_progress()
        else:
            return self.create_new_progress()
    
    def create_new_progress(self):
        """Create new progress tracking structure."""
        return {
            "current_session": {
                "task": None,
                "scenario_pair": None,
                "case_type": None,
                "db_path": None,
                "started_at": None
            },
            "total_questions": 0,
            "completed_questions": 0,
            "failed_questions": 0,
            "skipped_questions": 0,
            "question_status": {},
            "session_history": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def save_progress(self):
        """Save progress to file."""
        self.progress["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Error saving progress: {e}")
    
    def log(self, message):
        """Log message to both console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + "\n")
        except Exception:
            pass
    
    def display_task_options(self):
        """Display available task options."""
        print("\n=== Available Tasks ===")
        for task_num, task_name in self.tasks.items():
            print(f"{task_num}. {task_name}")
        print("========================")
    
    def display_scenario_options(self):
        """Display available scenario pair options."""
        print("\n=== Scenario Pairs ===")
        print("1. Scenarios 1 and 2")
        print("2. Scenarios 3, 4 and 5") 
        print("=======================")
    
    def display_case_options(self):
        """Display case type options."""
        print("\n=== Case Types ===")
        print("1. Reduced")
        print("2. Combined")
        print("===================")
    
    def select_task(self):
        """Let user select a task."""
        self.display_task_options()
        while True:
            try:
                choice = int(input("\nSelect task (1-6): ").strip())
                if choice in self.tasks:
                    return choice, self.tasks[choice]
                else:
                    print("Invalid choice. Please select 1-6.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_scenario_pair(self):
        """Let user select a scenario pair."""
        self.display_scenario_options()
        while True:
            try:
                choice = int(input("\nSelect scenario pair (1-2): ").strip())
                if choice in self.scenario_pairs:
                    return choice, self.scenario_pairs[choice]
                else:
                    print("Invalid choice. Please select 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_case_type(self):
        """Let user select case type (reduced or combined)."""
        self.display_case_options()
        while True:
            try:
                choice = int(input("\nSelect case type (1-2): ").strip())
                if choice == 1:
                    return "reduced"
                elif choice == 2:
                    return "combined"
                else:
                    print("Invalid choice. Please select 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_db_path(self, task_name, case_type):
        """Get the database path for the selected task and case type."""
        task_dir = self.db_base_dir / task_name
        
        # Generate the correct file name based on the actual naming pattern
        if case_type == "reduced":
            pkl_file = f"reduced_combined_{task_dir.name.lower()}_embeddings.pkl"
        else:  # combined
            pkl_file = f"combined_{task_dir.name.lower()}_embeddings.pkl"
        
        db_path = task_dir / pkl_file
        
        if not db_path.exists():
            self.log(f"Warning: Database file not found at {db_path}")
            # Try alternative naming patterns
            if case_type == "reduced":
                # Try without "combined" in the name
                alt_pkl_file = f"reduced_{task_dir.name.lower()}_embeddings.pkl"
            else:
                # Try without "combined" prefix
                alt_pkl_file = f"{task_dir.name.lower()}_embeddings.pkl"
            
            alt_db_path = task_dir / alt_pkl_file
            if alt_db_path.exists():
                self.log(f"Using alternative database file: {alt_db_path}")
                return str(alt_db_path)
            else:
                self.log(f"Alternative database file also not found: {alt_db_path}")
                self.log(f"Returning original path anyway: {db_path}")
                return str(db_path)  # Return original path anyway
        
        return str(db_path)
    
    def set_db_path_env(self, db_path):
        """Set the DB_PATH environment variable."""
        os.environ['DB_PATH'] = db_path
        self.log(f"Set DB_PATH environment variable to: {db_path}")
    
    def get_question_files(self, task_name, scenarios):
        """Get ground truth files for the specified task and scenarios."""
        question_files = []
        for scenario in scenarios:
            filename = f"{task_name}_scenario_{scenario}_ground_truths.json"
            file_path = self.gt_dir / filename
            if file_path.exists():
                question_files.append((file_path, scenario))
                self.log(f"Found GT file: {filename}")
            else:
                self.log(f"Warning: GT file not found: {filename}")
        
        return question_files
    
    def load_questions_from_file(self, json_file, scenario_num):
        """Load questions from GT file - only those where ground truth is present."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # GT files are a list directly, not with a 'questions' key
            if not isinstance(data, list):
                self.log(f"Warning: {json_file.name} is not a list format")
                return []
            
            # Filter to only include questions where ground truth is present
            questions_with_gt = [
                q for q in data 
                if q.get('is_answer_present', False) == True
            ]
            
            self.log(f"Found {len(questions_with_gt)} questions with GT out of {len(data)} total in {json_file.name}")
            
            questions = []
            processed_count = 0
            
            for question in questions_with_gt:
                if processed_count >= MAX_QUESTIONS_PER_JSON:
                    self.log(f"Limiting to first {MAX_QUESTIONS_PER_JSON} questions from {json_file.name}")
                    break
                    
                if isinstance(question, dict) and 'unique_id' in question and 'complete_question' in question:
                    questions.append({
                        'unique_id': question['unique_id'],
                        'complete_question': question['complete_question'],
                        'file': json_file.name,
                        'scenario': scenario_num,
                        'full_data': question
                    })
                    processed_count += 1
                else:
                    self.log(f"Warning: Question missing unique_id or complete_question in {json_file.name}")
            
            self.log(f"Loaded {len(questions)} questions with GT from {json_file.name} (limited to {MAX_QUESTIONS_PER_JSON})")
            return questions
            
        except Exception as e:
            self.log(f"Error loading questions from {json_file}: {e}")
            return []
    
    def initialize_agent(self, working_dir=None):
        """Initialize a fresh MainAgent instance with optional working directory."""
        try:
            self.log("Initializing fresh MainAgent...")
            self.main_agent = MainAgent(base_working_dir=working_dir)
            self.log("MainAgent initialized successfully")
            return True
        except Exception as e:
            self.log(f"Failed to initialize MainAgent: {e}")
            self.log(f"Traceback: {traceback.format_exc()}")
            return False
    
    def create_response_directory(self, task_name, scenario_pair_num, question_id):
        """Create directory structure for storing responses."""
        # Create: task_scenario_new_final_1_responses/TaskName/ScenarioPair_X/QuestionID/
        task_dir = self.current_responses_dir / task_name
        scenario_dir = task_dir / f"ScenarioPair_{scenario_pair_num}"
        question_dir = scenario_dir / question_id
        
        question_dir.mkdir(parents=True, exist_ok=True)
        return question_dir
    
    def should_recompute_question(self, unique_id, task_name, scenario_pair_num, session_key):
        """
        Determine if a question needs to be recomputed based on:
        1. Whether the queryid named folder exists
        2. If folder exists, check if it was successfully completed or failed
        3. Recompute if: folder doesn't exist OR previous attempt failed
        """
        # Check if the question folder exists
        task_dir = self.current_responses_dir / task_name
        scenario_dir = task_dir / f"ScenarioPair_{scenario_pair_num}"
        question_dir = scenario_dir / unique_id
        
        if not question_dir.exists():
            self.log(f"Question {unique_id} folder does not exist, will compute")
            return True
        
        # Folder exists, check if it was successful or failed
        metadata_file = question_dir / "question_metadata.json"
        error_file = question_dir / "error.txt"
        
        # If error.txt exists, it was a failed attempt - recompute
        if error_file.exists():
            self.log(f"Question {unique_id} previously failed (error.txt found), will recompute")
            return True
        
        # Check metadata for status
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    status = metadata.get('status', 'unknown')
                    if status == 'completed':
                        self.log(f"Question {unique_id} previously completed successfully, skipping")
                        return False
                    else:
                        self.log(f"Question {unique_id} has status '{status}', will recompute")
                        return True
            except Exception as e:
                self.log(f"Error reading metadata for {unique_id}: {e}, will recompute")
                return True
        
        # Folder exists but no clear success indicator - skip to be safe
        self.log(f"Question {unique_id} folder exists but status unclear, skipping")
        return False
    
    def process_question(self, question_info, task_name, scenario_pair_num):
        """Process a single question using a fresh MainAgent instance."""
        unique_id = question_info['unique_id']
        complete_question = question_info['complete_question']
        
        # Check if this question needs to be recomputed
        session_key = f"{task_name}_{scenario_pair_num}_{unique_id}"
        should_recompute = self.should_recompute_question(unique_id, task_name, scenario_pair_num, session_key)
        
        if not should_recompute:
            self.log(f"Skipping already completed question: {unique_id}")
            self.progress['skipped_questions'] += 1
            return True
        
        self.log(f"Processing question: {unique_id}")
        self.log(f"Question: {complete_question}")
        
        try:
            # Create response directory for this question first
            response_dir = self.create_response_directory(task_name, scenario_pair_num, unique_id)
            
            # Initialize fresh MainAgent with this question's response directory as working dir
            if not self.initialize_agent(working_dir=str(response_dir)):
                self.log(f"Failed to initialize MainAgent for question: {unique_id}")
                raise Exception("MainAgent initialization failed")
            
            # Run MainAgent
            start_time = time.time()
            formatted_question = f"""
Run the following Question without asking any clarifications. Assume answers/responses to the questions and continue
Use coder agent to generate code for performing predictive analysis by training intelligent regressors wherever required.

Question: {complete_question}
"""
            response = self.main_agent.run(formatted_question)
            end_time = time.time()
            
            # Get conversation hierarchy with all intermediate outputs
            try:
                conversation_hierarchy = self.main_agent.get_conversation_hierarchy()
            except Exception as e:
                self.log(f"Warning: Could not get conversation hierarchy: {e}")
                conversation_hierarchy = {}
            
            # Save response to markdown file
            response_file = response_dir / "response.md"
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write(response)
            
            # Save conversation hierarchy
            try:
                hierarchy_file = response_dir / "conversation_hierarchy.json"
                with open(hierarchy_file, 'w', encoding='utf-8') as f:
                    json.dump(conversation_hierarchy, f, ensure_ascii=False, indent=2)
                self.log(f"Saved conversation hierarchy for {unique_id}")
            except Exception as e:
                self.log(f"Warning: Could not save conversation hierarchy: {e}")
            
            # Groupchat logs are already in response_dir/groupchat_logs/
            # because GroupChat saves them directly to the custom log directory
            # Just log confirmation
            try:
                groupchat_logs_dir = response_dir / "groupchat_logs"
                if groupchat_logs_dir.exists():
                    log_files = list(groupchat_logs_dir.glob("groupchat_log_*.json"))
                    if log_files:
                        self.log(f"Found {len(log_files)} groupchat logs for {unique_id}")
            except Exception as e:
                self.log(f"Warning: Could not count groupchat logs: {e}")
            
            # Save intermediates (RAG queries and tool invocations)
            try:
                intermediates_dir = response_dir / "intermediates"
                intermediates_dir.mkdir(parents=True, exist_ok=True)
                
                thought_agents = conversation_hierarchy.get("thought_agents", {})
                for agent_name, agent_data in thought_agents.items():
                    intermediates = agent_data.get("intermediates", {})
                    if intermediates:
                        safe_agent_name = self.sanitize_filename(agent_name)
                        intermediates_file = intermediates_dir / f"{safe_agent_name}_intermediates.json"
                        with open(intermediates_file, 'w', encoding='utf-8') as f:
                            json.dump(intermediates, f, ensure_ascii=False, indent=2)
                        self.log(f"Saved intermediates for {agent_name}")
                
                if thought_agents:
                    self.log(f"Saved intermediates for {len(thought_agents)} agents for {unique_id}")
            except Exception as e:
                self.log(f"Warning: Could not save intermediates: {e}")
            
            # Generated files are already in response_dir/generated_files/{agent_name}/
            # because we set custom working directories for each thought agent
            # Just log confirmation
            try:
                generated_files_dir = response_dir / "generated_files"
                if generated_files_dir.exists():
                    total_files = sum(1 for _ in generated_files_dir.rglob('*') if _.is_file())
                    if total_files > 0:
                        self.log(f"Found {total_files} generated files in output directory for {unique_id}")
            except Exception as e:
                self.log(f"Warning: Could not count generated files: {e}")
            
            # Clean up the agent after use to free memory
            self.main_agent = None
            
            # Save question metadata
            metadata_file = response_dir / "question_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'unique_id': unique_id,
                    'complete_question': complete_question,
                    'file': question_info['file'],
                    'task_name': task_name,
                    'scenario_pair': scenario_pair_num,
                    'db_path': os.environ.get('DB_PATH', ''),
                    'full_question_data': question_info['full_data'],
                    'processing_time_seconds': end_time - start_time,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'completed'
                }, f, indent=2, ensure_ascii=False)
            
            # Update progress
            self.progress['question_status'][session_key] = {
                'status': 'completed',
                'file': question_info['file'],
                'task_name': task_name,
                'scenario_pair': scenario_pair_num,
                'timestamp': datetime.now().isoformat(),
                'processing_time': end_time - start_time
            }
            self.progress['completed_questions'] += 1
            
            self.log(f"Successfully processed question: {unique_id} (took {end_time - start_time:.2f}s)")
            return True
            
        except Exception as e:
            self.log(f"Error processing question {unique_id}: {e}")
            self.log(f"Traceback: {traceback.format_exc()}")
            
            # Clean up agent even on error
            self.main_agent = None
            
            # Update progress for failed question
            self.progress['question_status'][session_key] = {
                'status': 'failed',
                'file': question_info['file'],
                'task_name': task_name,
                'scenario_pair': scenario_pair_num,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            self.progress['failed_questions'] += 1
            
            # Try to save error info
            try:
                response_dir = self.create_response_directory(task_name, scenario_pair_num, unique_id)
                error_file = response_dir / "error.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Error processing question: {unique_id}\n")
                    f.write(f"Question: {complete_question}\n")
                    f.write(f"Task: {task_name}\n")
                    f.write(f"Scenario Pair: {scenario_pair_num}\n")
                    f.write(f"DB Path: {os.environ.get('DB_PATH', '')}\n")
                    f.write(f"Error: {e}\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"Traceback:\n{traceback.format_exc()}")
            except Exception:
                pass
            
            return False
    
    def collect_questions_for_session(self, task_name, scenarios):
        """Collect all questions for the current session."""
        question_files = self.get_question_files(task_name, scenarios)
        all_questions = []
        
        self.log(f"Configuration: Processing maximum {MAX_QUESTIONS_PER_JSON} questions per JSON file")
        
        for question_file, scenario_num in question_files:
            self.log(f"Loading questions from: {question_file.name}")
            questions = self.load_questions_from_file(question_file, scenario_num)
            all_questions.extend(questions)
            self.log(f"Added {len(questions)} questions from {question_file.name}")
        
        self.log(f"Total questions collected for session: {len(all_questions)}")
        return all_questions
    
    def run_session(self, task_num, task_name, scenario_pair_num, scenarios, case_type):
        """Run a complete session for the selected task and scenario pair."""
        self.log(f"Starting session for Task: {task_name}, Scenario Pair: {scenario_pair_num}, Case: {case_type}")
        
        # Set up database path
        db_path = self.get_db_path(task_name, case_type)
        self.set_db_path_env(db_path)
        
        # Set up the appropriate responses directory based on case type
        self.set_responses_directory(case_type)
        
        # Update current session info
        self.progress['current_session'] = {
            "task": task_name,
            "task_num": task_num,
            "scenario_pair": scenario_pair_num,
            "scenarios": scenarios,
            "case_type": case_type,
            "db_path": db_path,
            "started_at": datetime.now().isoformat()
        }
        
        # Collect all questions for this session
        all_questions = self.collect_questions_for_session(task_name, scenarios)
        
        if not all_questions:
            self.log("No questions found for this session.")
            return False
        
        # Update total questions count for this session
        self.progress['total_questions'] = len(all_questions)
        self.log(f"Total questions to process in this session: {len(all_questions)}")
        
        # Reset session counters
        self.progress['completed_questions'] = 0
        self.progress['failed_questions'] = 0
        self.progress['skipped_questions'] = 0
        
        # Process each question
        for i, question_info in enumerate(all_questions, 1):
            self.log(f"\n--- Processing question {i}/{len(all_questions)} ---")
            
            try:
                self.process_question(question_info, task_name, scenario_pair_num)
            except KeyboardInterrupt:
                self.log("Processing interrupted by user.")
                break
            except Exception as e:
                self.log(f"Unexpected error processing question {question_info['unique_id']}: {e}")
                self.progress['failed_questions'] += 1
            
            # Save progress after each question
            self.save_progress()
            
            # Add small delay to prevent overwhelming the system
            time.sleep(1)
        
        # Session summary
        self.log("\n--- Session Summary ---")
        self.log(f"Task: {task_name}")
        self.log(f"Scenario Pair: {scenario_pair_num} (Scenarios: {scenarios})")
        self.log(f"Case Type: {case_type}")
        self.log(f"Database Path: {db_path}")
        self.log(f"Total questions: {self.progress['total_questions']}")
        self.log(f"Completed: {self.progress['completed_questions']}")
        self.log(f"Failed: {self.progress['failed_questions']}")
        self.log(f"Skipped: {self.progress['skipped_questions']}")
        
        # Add to session history
        session_record = {
            "task": task_name,
            "task_num": task_num,
            "scenario_pair": scenario_pair_num,
            "scenarios": scenarios,
            "case_type": case_type,
            "db_path": db_path,
            "started_at": self.progress['current_session']['started_at'],
            "completed_at": datetime.now().isoformat(),
            "total_questions": self.progress['total_questions'],
            "completed_questions": self.progress['completed_questions'],
            "failed_questions": self.progress['failed_questions'],
            "skipped_questions": self.progress['skipped_questions']
        }
        
        self.progress['session_history'].append(session_record)
        self.save_progress()
        
        return True
    
    def display_session_info(self):
        """Display current session information."""
        if self.progress['current_session']['task']:
            print("\n=== Current Session Info ===")
            session = self.progress['current_session']
            print(f"Task: {session['task']}")
            print(f"Scenario Pair: {session['scenario_pair']}")
            print(f"Case Type: {session['case_type']}")
            print(f"Database Path: {session['db_path']}")
            print(f"Started: {session['started_at']}")
            print("=============================")
        
        if self.progress['session_history']:
            print(f"\n=== Previous Sessions: {len(self.progress['session_history'])} ===")
            for i, session in enumerate(self.progress['session_history'][-3:], 1):  # Show last 3
                print(f"{i}. {session['task']} - Pair {session['scenario_pair']} - {session['case_type']} "
                      f"({session['completed_questions']}/{session['total_questions']} completed)")


def main():
    """Main function to run the task scenario processor."""
    processor = TaskScenarioProcessor()
    
    print("=== Task and Scenario Based Question Processor ===")
    print(f"Configuration: Processing maximum {MAX_QUESTIONS_PER_JSON} questions per JSON file")
    
    # Display any existing session info
    processor.display_session_info()
    
    # User selections
    task_num, task_name = processor.select_task()
    scenario_pair_num, scenarios = processor.select_scenario_pair()
    case_type = processor.select_case_type()
    
    print(f"\n=== Configuration Summary ===")
    print(f"Selected Task: {task_name}")
    print(f"Scenario Pair: {scenario_pair_num} (Scenarios: {scenarios})")
    print(f"Case Type: {case_type}")
    
    # Confirm before proceeding
    confirm = input("\nProceed with this configuration? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Exiting...")
        return
    
    # Run the session
    try:
        processor.run_session(task_num, task_name, scenario_pair_num, scenarios, case_type)
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
    
    print(f"\nProcessing complete. Check '{processor.responses_base_dir}' for responses.")
    print(f"Progress and logs saved in '{processor.base_dir / 'outputs'}'")


if __name__ == "__main__":
    main()