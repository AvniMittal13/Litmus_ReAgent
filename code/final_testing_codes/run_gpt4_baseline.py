#!/usr/bin/env python3
"""
Baseline GPT-4.1 Script - Direct model evaluation on questions
Runs GPT-4.1 directly on questions using only user query + system instruction.
No agents, no web search, no code execution - pure model knowledge.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import traceback
import time
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
MAX_QUESTIONS_PER_JSON = 50

# Holistic system instruction combining research expertise
SYSTEM_INSTRUCTION = """You are an expert multilingual language researcher with PhD-level knowledge in machine learning model development, especially for low-resource language scenarios.

Your expertise includes:
- Deep knowledge of NLP benchmarks, datasets, and evaluation metrics across languages
- Understanding of model architectures (transformers, LLMs, code generation models, etc.)
- Familiarity with multilingual and cross-lingual transfer learning
- Knowledge of performance patterns across different language families
- Understanding of evaluation metrics like BLEU, ROUGE, accuracy, F1, ChrF, COMET, etc.

When answering questions about model performance:
1. Use your internal knowledge of published benchmarks, papers, and known results
2. If exact numbers are not known, provide reasonable estimates based on:
   - Similar models' performance on related tasks
   - Language family characteristics (high-resource vs low-resource)
   - Model size and architecture patterns
   - Known trends in multilingual NLP research

3. Structure your response as a research report with:
   - Direct answer to the question with specific metrics/values
   - Confidence level in your answer
   - Reasoning based on your knowledge
   - Related findings that support your answer

4. For predictive questions, provide your best estimate with justification based on:
   - Model capabilities and training data
   - Language resource availability
   - Cross-lingual transfer patterns
   - Published benchmarks on similar tasks/languages

Always provide a concrete numerical answer or estimate when asked about performance metrics.
Be specific and quantitative in your responses."""


class GPT4BaselineProcessor:
    """Process questions using direct GPT-4.1 calls."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.gt_dir = Path(r"./final_testing_codes\GET_GTS_FINAL\Ground_truths_5")
        self.responses_dir = self.base_dir / "final_testing_codes" / "FINAL_RUS" / "gpt4_baseline_final_responses"
        self.progress_file = self.base_dir / "final_testing_codes" / "FINAL_RUS" / "gpt4_baseline_final_progress.json"
        self.log_file = self.base_dir / "final_testing_codes" / "FINAL_RUS" / "gpt4_baseline_final_log.txt"
        
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
            1: [1, 2, 3, 4, 5],  # Scenarios 1 and 2
            2: [3, 4, 5]  # Scenarios 3, 4 and 5
        }
        
        # Ensure directories exist
        self.responses_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize OpenAI client
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
        _token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        self.client = AzureOpenAI(
            azure_ad_token_provider=_token_provider,
            api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("OPENAI_BASE_URL")
        )
        self.model = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4")
        
        # Load progress
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.create_new_progress()
        return self.create_new_progress()
    
    def create_new_progress(self):
        """Create new progress tracking."""
        return {
            "completed_questions": 0,
            "failed_questions": 0,
            "skipped_questions": 0,
            "question_status": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_progress(self):
        """Save progress to file."""
        self.progress["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2)
    
    def log(self, message):
        """Log message to console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + "\n")
        except:
            pass
    
    def call_gpt4(self, user_query: str) -> str:
        """Call GPT-4.1 with the user query."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.log(f"Error calling GPT-4: {e}")
            raise
    
    def get_question_files(self, task_name: str, scenarios: list) -> list:
        """Get ground truth JSON files for given task and scenarios."""
        files = []
        for scenario_num in scenarios:
            file_path = self.gt_dir / f"{task_name}_scenario_{scenario_num}_ground_truths.json"
            if file_path.exists():
                files.append((file_path, scenario_num))
            else:
                self.log(f"GT file not found: {file_path}")
        return files
    
    def load_questions(self, file_path: Path) -> list:
        """Load questions from GT file - only those where ground truth is present."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Filter to only include questions where ground truth is present
        questions_with_gt = [
            q for q in data 
            if q.get('is_answer_present', False) == True
        ]
        
        self.log(f"Found {len(questions_with_gt)} questions with GT out of {len(data)} total")
        return questions_with_gt[:MAX_QUESTIONS_PER_JSON]
    
    def should_process_question(self, unique_id: str, task_name: str, scenario_pair_num: int) -> bool:
        """Check if question needs to be processed."""
        question_dir = self.responses_dir / task_name / f"ScenarioPair_{scenario_pair_num}" / unique_id
        
        if not question_dir.exists():
            return True
        
        metadata_file = question_dir / "question_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                if metadata.get('status') == 'completed':
                    return False
            except:
                pass
        
        error_file = question_dir / "error.txt"
        if error_file.exists():
            return True
        
        return False
    
    def process_question(self, question_info: dict, task_name: str, scenario_pair_num: int, scenario_num: int):
        """Process a single question."""
        unique_id = question_info['unique_id']
        complete_question = question_info['complete_question']
        
        if not self.should_process_question(unique_id, task_name, scenario_pair_num):
            self.log(f"Skipping completed question: {unique_id}")
            self.progress['skipped_questions'] += 1
            return True
        
        self.log(f"Processing: {unique_id}")
        self.log(f"Question: {complete_question}")
        
        # Create response directory
        question_dir = self.responses_dir / task_name / f"ScenarioPair_{scenario_pair_num}" / unique_id
        question_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            start_time = time.time()
            
            # Call GPT-4 directly
            response = self.call_gpt4(complete_question)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Save metadata
            metadata = {
                "unique_id": unique_id,
                "complete_question": complete_question,
                "file": f"{task_name}_questions_scenario{scenario_num}.json",
                "task_name": task_name,
                "scenario_pair": scenario_pair_num,
                "full_question_data": question_info,
                "processing_time_seconds": processing_time,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "model_used": self.model
            }
            
            with open(question_dir / "question_metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Save response as response.md (matching original structure)
            with open(question_dir / "response.md", 'w', encoding='utf-8') as f:
                f.write(response)
            
            self.progress['completed_questions'] += 1
            self.log(f"Completed {unique_id} in {processing_time:.2f}s")
            
            # Remove error file if exists from previous failed attempt
            error_file = question_dir / "error.txt"
            if error_file.exists():
                error_file.unlink()
            
            return True
            
        except Exception as e:
            self.log(f"Error processing {unique_id}: {e}")
            self.log(traceback.format_exc())
            
            # Save error
            with open(question_dir / "error.txt", 'w', encoding='utf-8') as f:
                f.write(f"Error: {str(e)}\n\n{traceback.format_exc()}")
            
            self.progress['failed_questions'] += 1
            return False
    
    def run_task_scenario(self, task_num: int, scenario_pair_num: int):
        """Run all questions for a task and scenario pair."""
        task_name = self.tasks[task_num]
        scenarios = self.scenario_pairs[scenario_pair_num]
        
        self.log(f"\n{'='*60}")
        self.log(f"Processing Task: {task_name}")
        self.log(f"Scenario Pair: {scenario_pair_num} (Scenarios: {scenarios})")
        self.log(f"{'='*60}")
        
        question_files = self.get_question_files(task_name, scenarios)
        
        if not question_files:
            self.log(f"No question files found for {task_name}")
            return
        
        total_processed = 0
        
        for file_path, scenario_num in question_files:
            self.log(f"\nLoading questions from: {file_path.name}")
            questions = self.load_questions(file_path)
            self.log(f"Found {len(questions)} questions")
            
            for i, question in enumerate(questions):
                self.log(f"\n--- Question {i+1}/{len(questions)} (Scenario {scenario_num}) ---")
                success = self.process_question(question, task_name, scenario_pair_num, scenario_num)
                total_processed += 1
                self.save_progress()
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
        
        self.log(f"\nCompleted processing {total_processed} questions for {task_name}")
    
    def run_all(self):
        """Run all tasks and all scenario pairs."""
        self.log("\n" + "="*70)
        self.log("GPT-4.1 BASELINE - Processing ALL Tasks and Scenarios")
        self.log("="*70)
        
        for task_num in self.tasks.keys():
            for scenario_pair_num in self.scenario_pairs.keys():
                self.run_task_scenario(task_num, scenario_pair_num)
        
        self.log("\n" + "="*70)
        self.log("FINAL SUMMARY")
        self.log("="*70)
        self.log(f"Completed: {self.progress['completed_questions']}")
        self.log(f"Failed: {self.progress['failed_questions']}")
        self.log(f"Skipped: {self.progress['skipped_questions']}")
    
    def interactive_run(self):
        """Interactive mode to select task and scenario."""
        print("\n=== GPT-4.1 Baseline Evaluation ===")
        print("\nAvailable Tasks:")
        for num, name in self.tasks.items():
            print(f"  {num}. {name}")
        print("  0. Run ALL tasks")
        
        task_choice = int(input("\nSelect task (0-6): ").strip())
        
        print("\nScenario Pairs:")
        print("  1. Scenarios 1 and 2")
        print("  2. Scenarios 3, 4 and 5")
        print("  0. Run ALL scenario pairs")
        
        scenario_choice = int(input("\nSelect scenario pair (0-2): ").strip())
        
        if task_choice == 0 and scenario_choice == 0:
            self.run_all()
        elif task_choice == 0:
            for task_num in self.tasks.keys():
                self.run_task_scenario(task_num, scenario_choice)
        elif scenario_choice == 0:
            for scenario_pair_num in self.scenario_pairs.keys():
                self.run_task_scenario(task_choice, scenario_pair_num)
        else:
            self.run_task_scenario(task_choice, scenario_choice)


def main():
    processor = GPT4BaselineProcessor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            processor.run_all()
        else:
            print("Usage: python run_gpt4_baseline_final.py [--all]")
            print("  --all : Run all tasks and scenarios")
            print("  (no args) : Interactive mode")
    else:
        processor.interactive_run()


if __name__ == "__main__":
    main()
