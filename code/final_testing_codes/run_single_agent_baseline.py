#!/usr/bin/env python3
"""
Runner script for the Single LLM Agent baseline.
Runs the single agent (with iterative tool-calling) on all 1500 questions
from generated_questions/ and saves results to FINAL_RUS/SINGLE_AGENT_BASELINE/.
"""

import json
import os
import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

MAX_QUESTIONS_PER_JSON = 50
QUESTIONS_PER_SCENARIO = 50


class SingleAgentRunner:
    """Iterate over all generated questions and run the SingleAgent baseline."""

    TASKS = {
        1: "01_Code_Generation",
        2: "02_Math_Reasoning",
        3: "03_QA_VQA",
        4: "04_Classification_NLI",
        5: "05_Text_Summarization",
        6: "06_Machine_Translation",
    }

    SCENARIOS = [1, 2, 3, 4, 5]

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.questions_dir = self.base_dir / "generated_questions"
        self.db_base_dir = self.base_dir / "all_final_csvs_finall"
        self.responses_dir = (
            self.base_dir / "final_testing_codes" / "FINAL_RUS" / "SINGLE_AGENT_BASELINE"
        )
        self.progress_file = self.responses_dir / "progress.json"
        self.log_file = self.responses_dir / "run_log.txt"

        self.responses_dir.mkdir(parents=True, exist_ok=True)
        self.progress = self._load_progress()

    # ── logging / progress ─────────────────────────────────────────────

    def _load_progress(self):
        if self.progress_file.exists():
            try:
                return json.loads(self.progress_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "completed": 0,
            "failed": 0,
            "skipped": 0,
            "total": 0,
            "question_status": {},
            "last_updated": datetime.now().isoformat(),
        }

    def _save_progress(self):
        self.progress["last_updated"] = datetime.now().isoformat()
        self.progress_file.write_text(
            json.dumps(self.progress, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

    # ── DB path ────────────────────────────────────────────────────────

    def _get_db_path(self, task_name):
        task_dir = self.db_base_dir / task_name
        for pattern in [
            f"combined_{task_dir.name.lower()}_embeddings.pkl",
            f"reduced_combined_{task_dir.name.lower()}_embeddings.pkl",
        ]:
            p = task_dir / pattern
            if p.exists():
                return str(p)
        return str(task_dir / f"combined_{task_dir.name.lower()}_embeddings.pkl")

    # ── question loading ───────────────────────────────────────────────

    def _load_questions(self, task_name, scenario):
        fname = f"{task_name}_questions_scenario{scenario}.json"
        fpath = self.questions_dir / fname
        if not fpath.exists():
            self.log(f"  File missing: {fname}")
            return []
        data = json.loads(fpath.read_text(encoding="utf-8"))
        raw = data.get("questions", []) if isinstance(data, dict) else data
        out = []
        for q in raw[:MAX_QUESTIONS_PER_JSON]:
            if isinstance(q, dict) and "unique_id" in q and "complete_question" in q:
                out.append(q)
        self.log(f"  Loaded {len(out)} questions from {fname}")
        return out

    # ── skip logic ─────────────────────────────────────────────────────

    def _should_run(self, uid, task_name, scenario):
        qdir = self.responses_dir / task_name / "ScenarioPair_1" / uid
        if not qdir.exists():
            return True
        if (qdir / "error.txt").exists():
            return True
        meta = qdir / "question_metadata.json"
        if meta.exists():
            try:
                return json.loads(meta.read_text(encoding="utf-8")).get("status") != "completed"
            except Exception:
                return True
        return False

    # ── process one question ───────────────────────────────────────────

    def _process(self, question, task_name, scenario):
        uid = question["unique_id"]
        text = question["complete_question"]
        key = f"{task_name}_S{scenario}_{uid}"

        if not self._should_run(uid, task_name, scenario):
            self.log(f"  Skip (done): {uid}")
            self.progress["skipped"] += 1
            return

        qdir = self.responses_dir / task_name / "ScenarioPair_1" / uid
        qdir.mkdir(parents=True, exist_ok=True)

        # Working dir for code execution lives inside the question dir
        work_dir = str(qdir / "generated_files")
        os.makedirs(work_dir, exist_ok=True)

        try:
            from agents.single_agent.single_agent import SingleAgent

            agent = SingleAgent(working_dir=work_dir)

            formatted = (
                "Run the following Question without asking any clarifications. "
                "Assume answers/responses to the questions and continue.\n"
                "Use code execution to perform predictive analysis by training "
                "intelligent regressors wherever required.\n\n"
                f"Question: {text}"
            )

            start = time.time()
            response = agent.run(formatted)
            elapsed = time.time() - start

            # Save response
            (qdir / "response.md").write_text(response, encoding="utf-8")

            # Save intermediates (tool log)
            intermediates = agent.get_intermediates()
            (qdir / "intermediates.json").write_text(
                json.dumps(intermediates, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            # Save full conversation
            try:
                conv = []
                for m in agent.messages:
                    if isinstance(m, dict):
                        conv.append(m)
                    else:
                        conv.append({"_raw": str(m)})
                (qdir / "conversation.json").write_text(
                    json.dumps(conv, indent=2, ensure_ascii=False, default=str),
                    encoding="utf-8",
                )
            except Exception:
                pass

            # Save metadata
            (qdir / "question_metadata.json").write_text(
                json.dumps(
                    {
                        "unique_id": uid,
                        "complete_question": text,
                        "task_name": task_name,
                        "scenario": scenario,
                        "db_path": os.environ.get("DB_PATH", ""),
                        "full_question_data": question,
                        "processing_time_seconds": elapsed,
                        "total_tool_calls": intermediates["total_tool_calls"],
                        "timestamp": datetime.now().isoformat(),
                        "status": "completed",
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            self.progress["question_status"][key] = {"status": "completed", "time": elapsed}
            self.progress["completed"] += 1
            self.log(f"  Done: {uid} ({elapsed:.1f}s, {intermediates['total_tool_calls']} tool calls)")

        except Exception as e:
            self.log(f"  FAIL: {uid} – {e}")
            self.progress["question_status"][key] = {"status": "failed", "error": str(e)}
            self.progress["failed"] += 1
            try:
                (qdir / "error.txt").write_text(
                    f"Error: {e}\nQuestion: {text}\n{traceback.format_exc()}",
                    encoding="utf-8",
                )
            except Exception:
                pass

    # ── main run ───────────────────────────────────────────────────────

    def run(self, selected_task=None):
        """
        Run the baseline.  If *selected_task* is given (e.g. "01_Code_Generation"),
        only that task is processed; otherwise all tasks are processed.
        For each scenario, only the first QUESTIONS_PER_SCENARIO questions are run.
        """
        self.log("=== SINGLE AGENT BASELINE – Starting ===")

        tasks_to_run = (
            {k: v for k, v in self.TASKS.items() if v == selected_task}
            if selected_task
            else self.TASKS
        )

        # Collect questions – limited to QUESTIONS_PER_SCENARIO per scenario
        all_qs = []
        for task_num, task_name in tasks_to_run.items():
            db_path = self._get_db_path(task_name)
            for scenario in self.SCENARIOS:
                qs = self._load_questions(task_name, scenario)
                for q in qs[:QUESTIONS_PER_SCENARIO]:
                    q["_task"] = task_name
                    q["_scenario"] = scenario
                    q["_db_path"] = db_path
                all_qs.extend(qs[:QUESTIONS_PER_SCENARIO])

        self.progress["total"] = len(all_qs)
        self.progress["completed"] = 0
        self.progress["failed"] = 0
        self.progress["skipped"] = 0
        self.log(f"Total questions: {len(all_qs)}")

        for i, q in enumerate(all_qs, 1):
            task_name = q["_task"]
            scenario = q["_scenario"]
            os.environ["DB_PATH"] = q["_db_path"]

            self.log(f"\n--- [{i}/{len(all_qs)}] {task_name} S{scenario} {q['unique_id']} ---")
            try:
                self._process(q, task_name, scenario)
            except KeyboardInterrupt:
                self.log("Interrupted.")
                break
            except Exception as e:
                self.log(f"  Unexpected: {e}")
                self.progress["failed"] += 1

            self._save_progress()
            time.sleep(1)

        self.log("\n=== SUMMARY ===")
        self.log(f"Total: {self.progress['total']}")
        self.log(f"Completed: {self.progress['completed']}")
        self.log(f"Failed: {self.progress['failed']}")
        self.log(f"Skipped: {self.progress['skipped']}")
        self._save_progress()


def select_task():
    """Let user pick a task or run all."""
    tasks = SingleAgentRunner.TASKS
    print("\n=== Select Task ===")
    print("  0. ALL tasks")
    for num, name in tasks.items():
        print(f"  {num}. {name}")
    print("====================")
    while True:
        try:
            choice = int(input("Select task (0-6): ").strip())
            if choice == 0:
                return None  # all tasks
            if choice in tasks:
                return tasks[choice]
        except ValueError:
            pass
        print("Invalid choice.")


def main():
    print("=" * 60)
    print("  SINGLE AGENT BASELINE")
    print("  One LLM + tools (db_search, expert_rag, code_exec)")
    print(f"  {QUESTIONS_PER_SCENARIO} questions per scenario")
    print("=" * 60)

    selected_task = select_task()

    if selected_task:
        n_qs = len(SingleAgentRunner.SCENARIOS) * QUESTIONS_PER_SCENARIO
        print(f"\n  Task     : {selected_task}")
        print(f"  Scenarios: {SingleAgentRunner.SCENARIOS}")
        print(f"  Questions: {n_qs} ({QUESTIONS_PER_SCENARIO} per scenario)")
    else:
        n_qs = len(SingleAgentRunner.TASKS) * len(SingleAgentRunner.SCENARIOS) * QUESTIONS_PER_SCENARIO
        print(f"\n  Tasks    : ALL ({len(SingleAgentRunner.TASKS)})")
        print(f"  Scenarios: {SingleAgentRunner.SCENARIOS}")
        print(f"  Questions: {n_qs} ({QUESTIONS_PER_SCENARIO} per scenario)")

    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    runner = SingleAgentRunner()
    try:
        runner.run(selected_task=selected_task)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Fatal: {e}")
        traceback.print_exc()

    print(f"\nResults in: {runner.responses_dir}")


if __name__ == "__main__":
    main()
