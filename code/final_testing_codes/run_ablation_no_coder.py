#!/usr/bin/env python3
"""
Ablation study: Run MainAgent WITHOUT coder_agent / code_executor_agent
on 10 Code Generation prompts across scenarios 1-5.

Usage:
    venv\\Scripts\\Activate.ps1; python -m final_testing_codes.run_ablation_no_coder
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import traceback
import time

# Configuration
MAX_QUESTIONS_PER_JSON = 50
QUESTIONS_PER_SCENARIO = 10  # 10 questions per scenario

# Add the parent directory to the path to import agents
sys.path.append(str(Path(__file__).parent.parent))

from agents.main_agent_db_no_coder import MainAgent


class AblationNoCoderProcessor:
    """
    Ablation: process Code Generation questions using MainAgent without coder_agent.
    """
    
    @staticmethod
    def sanitize_filename(name):
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        name = name.rstrip('. ')
        if len(name) > 200:
            name = name[:200]
        return name
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.gt_dir = self.base_dir / "final_testing_codes" / "GET_GTS_FINAL" / "Ground_truths_5"
        self.questions_dir = self.base_dir / "generated_questions"
        self.db_base_dir = self.base_dir / "all_final_csvs_finall"
        
        # Output dirs specific to this ablation
        self.responses_base_dir = self.base_dir / "final_testing_codes" / "ABLATION_RUNS" / "no_coder" / "01_Code_Generation"
        self.progress_file = self.base_dir / "final_testing_codes" / "ABLATION_RUNS" / "no_coder" / "ablation_progress.json"
        self.log_file = self.base_dir / "final_testing_codes" / "ABLATION_RUNS" / "no_coder" / "ablation_log.txt"
        
        # Ensure directories exist
        self.responses_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Task config — Code Generation only
        self.task_name = "01_Code_Generation"
        self.scenarios = [1, 3, 5]
        
        self.progress = self.load_progress()
        self.main_agent = None
    
    def load_progress(self):
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.create_new_progress()
    
    def create_new_progress(self):
        return {
            "ablation": "no_coder",
            "task": self.task_name,
            "total_questions": 0,
            "completed_questions": 0,
            "failed_questions": 0,
            "skipped_questions": 0,
            "question_status": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_progress(self):
        self.progress["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Error saving progress: {e}")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [ABLATION no_coder] {message}"
        print(log_message)
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + "\n")
        except Exception:
            pass
    
    def get_db_path(self):
        task_dir = self.db_base_dir / self.task_name
        pkl_file = f"combined_{task_dir.name.lower()}_embeddings.pkl"
        db_path = task_dir / pkl_file
        if not db_path.exists():
            alt = task_dir / f"reduced_combined_{task_dir.name.lower()}_embeddings.pkl"
            if alt.exists():
                return str(alt)
        return str(db_path)
    
    def get_question_files(self):
        """Get ground truth files for Code Generation across all scenarios."""
        question_files = []
        for scenario in self.scenarios:
            filename = f"{self.task_name}_scenario_{scenario}_ground_truths.json"
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
            
            if not isinstance(data, list):
                self.log(f"Warning: {json_file.name} is not a list format")
                return []
            
            questions_with_gt = [
                q for q in data 
                if q.get('is_answer_present', False) == True
            ]
            
            self.log(f"Found {len(questions_with_gt)} questions with GT out of {len(data)} total in {json_file.name}")
            
            questions = []
            for question in questions_with_gt[:MAX_QUESTIONS_PER_JSON]:
                if isinstance(question, dict) and 'unique_id' in question and 'complete_question' in question:
                    questions.append({
                        'unique_id': question['unique_id'],
                        'complete_question': question['complete_question'],
                        'file': json_file.name,
                        'scenario': scenario_num,
                        'full_data': question
                    })
            
            self.log(f"Loaded {len(questions)} questions from {json_file.name}")
            return questions
            
        except Exception as e:
            self.log(f"Error loading questions from {json_file}: {e}")
            return []
    
    def should_recompute(self, unique_id, scenario):
        question_dir = self.responses_base_dir / f"Scenario_{scenario}" / unique_id
        if not question_dir.exists():
            return True
        if (question_dir / "error.txt").exists():
            return True
        meta = question_dir / "question_metadata.json"
        if meta.exists():
            try:
                with open(meta, 'r', encoding='utf-8') as f:
                    if json.load(f).get("status") == "completed":
                        return False
            except Exception:
                return True
        return True
    
    def initialize_agent(self, working_dir=None):
        try:
            self.log("Initializing fresh MainAgent (no coder) ...")
            self.main_agent = MainAgent(base_working_dir=working_dir)
            self.log("MainAgent ready")
            return True
        except Exception as e:
            self.log(f"MainAgent init failed: {e}\n{traceback.format_exc()}")
            return False
    
    def process_question(self, question_info, scenario):
        unique_id = question_info['unique_id']
        complete_question = question_info['complete_question']
        session_key = f"no_coder_{self.task_name}_S{scenario}_{unique_id}"
        
        if not self.should_recompute(unique_id, scenario):
            self.log(f"Skipping completed: {unique_id}")
            self.progress['skipped_questions'] += 1
            return True
        
        self.log(f"Processing {unique_id}")
        response_dir = self.responses_base_dir / f"Scenario_{scenario}" / unique_id
        response_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if not self.initialize_agent(working_dir=str(response_dir)):
                raise RuntimeError("MainAgent init failed")
            
            start = time.time()
            formatted = (
                "Run the following Question without asking any clarifications. "
                "Assume answers/responses to the questions and continue\n"
                "Perform analysis by collecting data via web search and expert knowledge "
                "and synthesize a well-reasoned prediction.\n\n"
                f"Question: {complete_question}"
            )
            response = self.main_agent.run(formatted)
            elapsed = time.time() - start
            
            # Save response
            (response_dir / "response.md").write_text(response, encoding="utf-8")
            
            # Save conversation hierarchy
            try:
                hierarchy = self.main_agent.get_conversation_hierarchy()
                (response_dir / "conversation_hierarchy.json").write_text(
                    json.dumps(hierarchy, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            except Exception:
                hierarchy = {}
            
            # Save intermediates
            try:
                intermediates_dir = response_dir / "intermediates"
                intermediates_dir.mkdir(exist_ok=True)
                for agent_name, adata in hierarchy.get("thought_agents", {}).items():
                    inters = adata.get("intermediates", {})
                    if inters:
                        safe = self.sanitize_filename(agent_name)
                        (intermediates_dir / f"{safe}_intermediates.json").write_text(
                            json.dumps(inters, ensure_ascii=False, indent=2), encoding="utf-8"
                        )
            except Exception:
                pass
            
            self.main_agent = None
            
            # Save metadata
            (response_dir / "question_metadata.json").write_text(json.dumps({
                'unique_id': unique_id,
                'complete_question': complete_question,
                'file': question_info['file'],
                'task_name': self.task_name,
                'scenario': scenario,
                'ablation': 'no_coder',
                'db_path': os.environ.get('DB_PATH', ''),
                'full_question_data': question_info['full_data'],
                'processing_time_seconds': elapsed,
                'timestamp': datetime.now().isoformat(),
                'status': 'completed'
            }, indent=2, ensure_ascii=False), encoding="utf-8")
            
            self.progress['question_status'][session_key] = {
                'status': 'completed',
                'timestamp': datetime.now().isoformat(),
                'processing_time': elapsed
            }
            self.progress['completed_questions'] += 1
            self.log(f"Completed {unique_id} in {elapsed:.2f}s")
            return True
            
        except Exception as e:
            self.log(f"Error processing {unique_id}: {e}\n{traceback.format_exc()}")
            self.main_agent = None
            
            self.progress['question_status'][session_key] = {
                'status': 'failed',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            self.progress['failed_questions'] += 1
            
            try:
                (response_dir / "error.txt").write_text(
                    f"Error: {e}\nTraceback:\n{traceback.format_exc()}", encoding="utf-8"
                )
            except Exception:
                pass
            
            return False
    
    def run(self):
        self.log("=" * 60)
        self.log("ABLATION STUDY: Remove Coder Agent")
        self.log(f"Task: {self.task_name}")
        self.log(f"Questions per scenario: {QUESTIONS_PER_SCENARIO}, Scenarios: {self.scenarios}")
        self.log("=" * 60)
        
        # Set DB path
        db_path = self.get_db_path()
        os.environ['DB_PATH'] = db_path
        self.log(f"DB_PATH = {db_path}")
        
        # Collect questions per scenario (10 per scenario)
        all_questions = []
        question_files = self.get_question_files()
        for qf, scenario in question_files:
            qs = self.load_questions_from_file(qf, scenario)
            all_questions.extend(qs[:QUESTIONS_PER_SCENARIO])
            self.log(f"Taking {min(len(qs), QUESTIONS_PER_SCENARIO)} questions from scenario {scenario}")
        
        if not all_questions:
            self.log("No questions found. Exiting.")
            return
        
        # Reset counters for this run
        self.progress['total_questions'] = len(all_questions)
        self.progress['completed_questions'] = 0
        self.progress['failed_questions'] = 0
        self.progress['skipped_questions'] = 0
        self.log(f"Processing {len(all_questions)} questions across {len(question_files)} scenarios")
        
        for i, qinfo in enumerate(all_questions, 1):
            self.log(f"\n--- Question {i}/{len(all_questions)} ---")
            try:
                self.process_question(qinfo, qinfo['scenario'])
            except KeyboardInterrupt:
                self.log("Interrupted by user.")
                break
            except Exception as e:
                self.log(f"Unexpected error: {e}")
                self.progress['failed_questions'] += 1
            
            self.save_progress()
            time.sleep(1)
        
        # Summary
        self.log("\n" + "=" * 60)
        self.log("ABLATION SUMMARY: no_coder")
        self.log(f"Total: {self.progress['total_questions']}")
        self.log(f"Completed: {self.progress['completed_questions']}")
        self.log(f"Failed: {self.progress['failed_questions']}")
        self.log(f"Skipped: {self.progress['skipped_questions']}")
        self.log("=" * 60)
        self.save_progress()


if __name__ == "__main__":
    processor = AblationNoCoderProcessor()
    try:
        processor.run()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
