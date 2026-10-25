# LITMUS-ReAgent

This repository contains the code and data for **Litmus (Re)Agent: A Benchmark and Agentic System for Predictive Evaluation of Multilingual Models** ([arXiv:2604.08970](https://arxiv.org/abs/2604.08970)). Litmus (Re)Agent builds on [LITMUS++](#citation) (IJCNLP-AACL 2025 System Demonstrations).

A multi-agent system for predicting how well LLMs perform across languages, tasks and models, with a focus on low-resource languages. For each question, the system gathers evidence from a curated database of research papers, follows expert research guidance, and, when no benchmark reports the number directly, collects features and trains small predictive models in generated code.

```
├── code/                          # original project code (unchanged)
│   ├── agents/                    # the multi-agent system (+ ablation variants)
│   ├── final_testing_codes/       # runners for the system, ablations and baseline
│   │   └── GET_GTS_FINAL/         # ground-truth generation, prediction extraction, MAE/accuracy
│   ├── final_evals/               # LLM-judge and agent-level evaluation scripts
│   ├── knowledge/                 # expert-knowledge corpus used by the RAG agent
│   └── utils/                     # Azure OpenAI chat + embedding helpers
└── data/
    ├── all_final_csvs_finall/        # paper database (CSVs, embeddings, scraped content)
    ├── generated_questions_filtered/ # the benchmark: 1,500 questions + their ground truths
    └── Ground_truths/                # extended ground-truth set (2,035 questions)
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
cp .env.example .env   # fill in Azure OpenAI endpoint/deployment and Firecrawl keys
```

Authentication uses `OPENAI_API_KEY` if set, otherwise Azure AD (`az login` / `DefaultAzureCredential`). Embeddings must use `text-embedding-ada-002`, because the precomputed paper embeddings were built with it.

### Put the data where the code expects it

The code is the original, unchanged project code, so it reads data from the locations it used originally (relative to `code/`). Link (or copy) `data/` into place once:

```bash
cd code
ln -s ../data/all_final_csvs_finall all_final_csvs_finall
ln -s ../data/all_final_csvs_finall/scraped_content.json scraped_content.json
ln -s ../data/generated_questions_filtered generated_questions
mkdir -p final_testing_codes/GET_GTS_FINAL
ln -s ../../../data/generated_questions_filtered/ground_truths final_testing_codes/GET_GTS_FINAL/Ground_truths_5
mkdir -p final_testing_codes/FINAL_RUS   # output folder the runners expect to exist
```

On Windows, copy the same folders to the same places, e.g. `Copy-Item -Recurse ..\data\all_final_csvs_finall .`.

> The original code was run on **Windows**. Two paths are written with backslashes and resolve relative to the current directory: `./final_testing_codes\GET_GTS_FINAL\Ground_truths_5` (in the runners) and `./knowledge\knowledge_2.md` (in `agents/custom_agents/expert_knowledge.py`). On macOS/Linux, add links with those literal names so they resolve without touching the code:
> ```bash
> ln -s final_testing_codes/GET_GTS_FINAL/Ground_truths_5 'final_testing_codes\GET_GTS_FINAL\Ground_truths_5'
> ln -s knowledge/knowledge_2.md 'knowledge\knowledge_2.md'
> ```

## Running

Run all commands from `code/`:

| Command | What it runs |
|---|---|
| `python final_testing_codes/run_all_que_db.py` | **Full LITMUS-ReAgent** (MainAgent) |
| `python final_testing_codes/run_all_que_db_thought.py` | A single ThoughtAgent without the MainAgent layer |
| `python -m final_testing_codes.run_ablation_no_coder` | Ablation: no coder agent |
| `python -m final_testing_codes.run_ablation_no_expert` | Ablation: no expert-knowledge agent |
| `python final_testing_codes/run_gpt4_baseline.py` | Direct LLM baseline (no tools) |

`run_all_que_db.py` is interactive. It asks for a **task** (1–6), a **scenario pair** and a **paper DB variant**:
- `reduced`: `reduced_combined_<task>_embeddings.pkl` (smaller paper set)
- `combined`: `combined_<task>_embeddings.pkl` (full paper set)

It sets `DB_PATH` for the selected task, loads up to `MAX_QUESTIONS_PER_JSON = 50` questions with ground truth per file from `GET_GTS_FINAL/Ground_truths_5`, and is resumable. Already-completed question folders are skipped. Outputs go to `final_testing_codes/FINAL_RUS/<run>_responses/<Task>/ScenarioPair_<n>/<question_id>/`, with the final response, the full conversation hierarchy, per-agent intermediates and the generated code files.

## Evaluation

### MAE / accuracy against ground truth (`final_testing_codes/GET_GTS_FINAL/`)
See `final_testing_codes/GET_GTS_FINAL/README.md`. Set the input/output folders in each package's `config.py`, then run from `code/`:

```bash
# 1. extract the predicted values from the agent reports (response.md)
python -m final_testing_codes.GET_GTS_FINAL.evaluation_performance_metrics_v2.main
# 2. MAE for predictive questions, accuracy for QnA questions
python -m final_testing_codes.GET_GTS_FINAL.mae_accuracy_evaluation.evaluator
```

For the ablation runs, use `evaluation_performance_metrics_v2.run_ablation_extraction` and `mae_accuracy_evaluation.run_ablation_eval` (`--ablation no_coder | no_expert_knowledge`). `ground_truth_generator_v2` is the pipeline that produced the ground truths, included for transparency. The ground truths themselves are already in `data/`.

### Report- and agent-level metrics (`final_evals/`)
These read response folders produced by the runners; pass the folders as arguments.

| Script | Measures |
|---|---|
| `accuracy_metric.py` | Extracts the final predicted value from two reports and compares them (LLM-judge) |
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

### `data/generated_questions_filtered/`: the benchmark
`<task>_questions_scenario<1-5>.json`: 30 files × 50 = **1,500 questions**, the set used in the experiments. Each question has `unique_id, complete_question, task, models, languages, question_type`.
- `ground_truths/`: the ground truths for exactly these 1,500 questions (identical to the original `GET_GTS_FINAL/Ground_truths_5`). Each entry has `unique_id, complete_question, predictive_or_qna, ground_truth_metrics_and_values_for_predictive, answer_text_for_qna, is_answer_present, atleast_one_successful_execution`.
- `diagrams/`: benchmark statistics figures.

### `data/Ground_truths/`
Extended ground-truth set in the same format: 30 files, 2,035 questions (1,065 predictive, 970 QnA). It contains all 1,500 benchmark questions with identical entries, plus 535 more.

## Notes on this release

- **All project code is copied verbatim** from the original project, with the same file names, folder structure and logic. Only the following files were not part of the uploaded sources and were added:
  - `code/utils/`: **reconstructed**. The original helper module was missing. It was rewritten to match the interface the code calls (`model_config`, `client`, `get_gpt_output`, `get_chat_response`, `get_structured_response`, `embedding_client`, `openai_embedding_function`).
  - `code/knowledge/knowledge_2.md`: **recovered** from the project's LightRAG index (*"LLM Performance Prediction Playbook"*). It is the expert-knowledge corpus the RAG agent was indexing, but it may differ in small details from the exact file used in the experiments.
  - `code/requirements.txt`, `code/.env.example`.
- Some config defaults point to the folder names used in the original experiments (e.g. `final_results/magnetic_one_1_responses`). Edit `config.py` to point at your own runs, as in the original workflow.
- Not included: experiment outputs and intermediate logs, the question-generation pipeline, the Magentic-One / single-agent / original-LITMUS++ baselines, and visualization scripts.

## Citation

If you use this code or data, please cite:

```bibtex
@article{mittal2026litmus,
  title={Litmus (Re) Agent: A Benchmark and Agentic System for Predictive Evaluation of Multilingual Models},
  author={Mittal, Avni and Kumar, Shanu and Dandapat, Sandipan and Choudhury, Monojit},
  journal={arXiv preprint arXiv:2604.08970},
  year={2026}
}

@inproceedings{mittal2025litmus++,
  title={LITMUS++: An Agentic System for Predictive Analysis of Low-Resource Languages Across Tasks and Models},
  author={Mittal, Avni and Kumar, Shanu and Dandapat, Sandipan and Choudhury, Monojit},
  booktitle={Proceedings of The 14th International Joint Conference on Natural Language Processing and The 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics: System Demonstrations},
  pages={47--54},
  year={2025}
}
```
