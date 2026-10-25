# LITMUS-ReAgent

A multi-agent system for predicting how well LLMs perform across languages, tasks and models, with a focus on low-resource languages. For each question, the system gathers evidence from a curated database of research papers, follows expert research guidance, and, when no benchmark reports the number directly, collects features and trains small predictive models in generated code.

```
LitmusReAgent/
├── code/
│   ├── agents/         # the multi-agent system (+ ablation variants)
│   ├── runners/        # scripts that run the system / baselines over the benchmark
│   ├── evaluation/     # LLM-judge and agent-level evaluation scripts
│   ├── knowledge/      # expert-knowledge corpus used by the RAG agent
│   └── utils/          # Azure OpenAI chat + embedding helpers
└── data/
    ├── all_final_csvs_finall/   # paper database (CSVs, embeddings, scraped content)
    └── Ground_truths/           # benchmark questions with ground-truth answers
```

## Architecture

**MainAgent** (`agents/main_agent_db.py`) orchestrates one user query:

1. **Expert Knowledge Agent**: RAG over `knowledge/knowledge_2.md` returns research guidance for the query.
2. **Thought Creator Agent**: proposes up to 3 distinct *thought paths* (research hypotheses / strategies).
3. One **ThoughtAgent** per thought path runs **in parallel**.
4. **Response Analyzer Agent**: merges the thought agents' findings into the final answer.

**ThoughtAgent** (`agents/thought_agent_db.py`) is an AutoGen group chat:

| Agent | Role |
|---|---|
| `research_planner_agent` | Drives the chat and decides which agent acts next |
| `expert_knowledge_agent` | RAG-based research guidance |
| `websearch_and_crawl_agent` | Embedding search over the paper DB, then scrapes the matched papers (`tools/db_search_and_scrape.py`) |
| `coder_agent` → `code_executor_agent` | Writes and locally executes Python (e.g. lang2vec/URIEL features + XGBoost regressors) |
| `send_user_msg_agent` | Emits the thought path's final response |

**Ablations** (same structure, one component removed):
- `main_agent_db_no_coder.py` / `thought_agent_db_no_coder.py`: no coder/executor
- `main_agent_db_no_expert.py` / `thought_agent_db_no_expert.py`: no expert-knowledge agent

## Setup

```bash
cd code
pip install -r requirements.txt
cp .env.example .env   # fill in Azure OpenAI endpoint/deployment (+ Firecrawl key)
```

Authentication uses `OPENAI_API_KEY` if set, otherwise Azure AD (`az login` / `DefaultAzureCredential`). Embeddings must use `text-embedding-ada-002`, because the precomputed paper embeddings were built with it.

## Running

Run all commands from `code/`:

| Script | What it runs |
|---|---|
| `python runners/run_litmus_reagent.py` | **Full LITMUS-ReAgent** (MainAgent) |
| `python runners/run_thought_agent_only.py` | A single ThoughtAgent without the MainAgent layer |
| `python -m runners.run_ablation_no_coder` | Ablation: no coder agent |
| `python -m runners.run_ablation_no_expert` | Ablation: no expert-knowledge agent |
| `python runners/run_gpt4_baseline.py` | Direct LLM baseline (no tools) |

`run_litmus_reagent.py` is interactive. It asks for a **task** (1–6), a **scenario group** (1–2 or 3–5) and a **paper DB variant**:
- `reduced`: `reduced_combined_<task>_embeddings.pkl` (smaller paper set)
- `combined`: `combined_<task>_embeddings.pkl` (full paper set)

It sets `DB_PATH` for the selected task, loads up to `MAX_QUESTIONS_PER_JSON = 50` questions per ground-truth file, and is resumable. Already-completed question folders are skipped. Outputs go to `code/outputs/<run>/<Task>/ScenarioPair_<n>/<question_id>/`, with the final response, the full conversation hierarchy, per-agent intermediates and the generated code files.

## Evaluation

The scripts in `code/evaluation/` read response folders produced by the runners. Pass input/output folders as arguments; the defaults point to the original experiment folders.

| Script | Measures |
|---|---|
| `accuracy_metric.py` | Extracts the final predicted value and compares it to ground truth (LLM-judge) |
| `run_text_metrics_configurable.py` | Report-quality metrics across multiple response folders |
| `hallucination_metric.py` | Whether cited papers exist in the paper DB |
| `evaluate_tool_relevance.py` | Relevance of DB search / crawl tool calls |
| `evaluate_thought_creator.py` | Quality and diversity of generated thought paths |
| `evaluate_coder_agent.py` / `evaluate_generated_code.py` | Code execution success and methodology quality |

## Data

### `data/all_final_csvs_finall/`
Curated research-paper database, one folder per task: `01_Code_Generation`, `02_Math_Reasoning`, `03_QA_VQA`, `04_Classification_NLI`, `05_Text_Summarization`, `06_Machine_Translation`.
- `combined_<task>.csv` / `reduced_combined_<task>.csv`: papers with `Task, Languages, Models, URL, Description`
- `*_embeddings.pkl` / `.json`: ada-002 embeddings of Description + Models + Languages (what `DB_PATH` points to)
- `scraped_content.json`: cached full-text scrapes of the 152 paper URLs, so Firecrawl is only called on a cache miss
- `*_language_model(s)_mapping.*`, `language_statistics.csv`, `model_statistics.csv`, `statistics_output/`: per-task language/model coverage
- Helper scripts to rebuild embeddings and the scrape cache (`create_and_save_embeddings.py`, `scrape_and_save_all_urls.py`, …); see the README in that folder

### `data/Ground_truths/`
`<task>_scenario_<1-5>_ground_truths.json`: 30 files, 2,035 questions in total (1,065 predictive, 970 QnA). Each entry has:
`unique_id, complete_question, predictive_or_qna, ground_truth_metrics_and_values_for_predictive, answer_text_for_qna, is_answer_present, atleast_one_successful_execution`.

## Notes on this release

- **`code/utils/` is reconstructed.** The original helper module was not in the uploaded sources. It was rewritten to match the interface the code calls (`model_config`, `client`, `get_gpt_output`, `get_chat_response`, `get_structured_response`, `embedding_client`, `openai_embedding_function`).
- **`code/knowledge/knowledge_2.md` was recovered** from the project's LightRAG index (*"LLM Performance Prediction Playbook"*). It is the expert-knowledge corpus the RAG agent was indexing, but it may differ in small details from the exact file used in the experiments.
- **Paths were adapted** to this layout (data under `../data`, outputs under `code/outputs`). Firecrawl keys were unified to `FIRECRAWL_API_KEY`. Agent logic and prompts are unchanged.
- The experiments evaluated **1,500 questions (50 per task×scenario file)**, a subset of the 2,035 in `data/Ground_truths`. The runner takes the first 50 per file, which is not necessarily the same subset.
- Not included: experiment outputs and intermediate logs, the question-generation pipeline, the Magentic-One / single-agent / original-LITMUS baselines, and visualization scripts.
