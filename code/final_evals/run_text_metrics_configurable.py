"""
Configurable Text Metrics Evaluation for Multiple Agent Response Folders.

This script evaluates response reports using LLM-based text quality metrics
(Predictive Plausibility, Feature Selection, Coherence, Citation Emphasis).

Supports configurable scenario pair mappings per folder:
  - "split" mode: ScenarioPair_1 (scenarios 1,2) + ScenarioPair_2 (scenarios 3,4,5)
  - "all_in_one" mode: ScenarioPair_1 contains all scenarios (1-5)

Usage examples in the docstring at bottom of file.
"""
import sys
import os
import json
import glob
import argparse
from statistics import mean
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_structured_response, get_chat_response
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
import re as _re

# ── Two parallel Azure OpenAI clients for 2x throughput ──────────────────────
_PARALLEL_ENDPOINTS = [
    "https://YOUR_RESOURCE.cognitiveservices.azure.com/",
    "https://YOUR_RESOURCE.cognitiveservices.azure.com/",
]
_token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
_parallel_clients = [
    AzureOpenAI(
        azure_endpoint=ep,
        azure_ad_token_provider=_token_provider,
        api_version=os.getenv("OPENAI_API_VERSION", "2025-01-01-preview"),
    )
    for ep in _PARALLEL_ENDPOINTS
]
_PARALLEL_MODEL = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4.1")
_client_counter = 0  # simple round-robin counter


def _get_next_client():
    """Round-robin across the parallel clients."""
    global _client_counter
    client = _parallel_clients[_client_counter % len(_parallel_clients)]
    _client_counter += 1
    return client


# ============================================================================
# CONFIGURATION: Define all folder configs here
# ============================================================================

ROOT_DIR = r"./"
FINAL_RUS = os.path.join(ROOT_DIR, "final_testing_codes", "FINAL_RUS")
QUESTIONS_FOLDER = os.path.join(ROOT_DIR, "generated_questions")

# Each folder config has:
#   "path": path to response folder
#   "scenario_mode": "split" or "all_in_one"
#     - "split": ScenarioPair_1 = scenarios 1,2; ScenarioPair_2 = scenarios 3,4,5
#     - "all_in_one": ScenarioPair_1 = all scenarios 1-5
#   "output_name": name for output subfolder
FOLDER_CONFIGS = {
    "litmus_reagent": {
        "path": os.path.join(FINAL_RUS, "litmus_reagent_1_responses"),
        "scenario_mode": "split",  # ScenarioPair_1 = {1,2}, ScenarioPair_2 = {3,4,5}
        "output_name": "litmus_reagent_1_responses",
    },
    "thought_agent": {
        "path": os.path.join(FINAL_RUS, "thought_agent_1_responses"),
        "scenario_mode": "split",  # ScenarioPair_1 = {1,2}, ScenarioPair_2 = {3,4,5}
        "output_name": "thought_agent_1_responses",
    },
    "gpt4_baseline": {
        "path": os.path.join(FINAL_RUS, "gpt4_baseline_final_responses"),
        "scenario_mode": "all_in_one",  # ScenarioPair_1 = all {1,2,3,4,5}
        "output_name": "gpt4_baseline_final_responses",
    },
    "magnetic_one": {
        "path": os.path.join(FINAL_RUS, "magnetic_one_1_responses"),
        "scenario_mode": "split",  # ScenarioPair_1 = {1,2}, ScenarioPair_2 = {3,4,5}
        "output_name": "magnetic_one_1_responses",
    },
    "single_agent_baseline": {
        "path": os.path.join(FINAL_RUS, "SINGLE_AGENT_BASELINE"),
        "scenario_mode": "all_in_one",  # ScenarioPair_1 = all {1,2,3,4,5}
        "output_name": "SINGLE_AGENT_BASELINE",
    },
    "litmus_original": {
        "path": os.path.join(FINAL_RUS, "litmus_plus_plus_orig_1_responses"),
        "scenario_mode": "split",  # ScenarioPair_1 = {1,2}, ScenarioPair_2 = {3,4,5}
        "output_name": "litmus_plus_plus_orig_1_responses",
    },
}

# Output base directory
OUTPUT_BASE = os.path.join(ROOT_DIR, "final_evals", "FINAL_OUTCOMES_FINAL", "TEXT_METRICS")


# ============================================================================
# MODELS
# ============================================================================

class CommonMetricEvaluation(BaseModel):
    class MetricDetails(BaseModel):
        metric_name: str
        score: int
        rationale: str
        indicators: list[str]

    metrics: list[MetricDetails]


# ============================================================================
# PROMPT
# ============================================================================

metric_prompt = """
You are an **expert reviewer**: a senior multilingual-NLP researcher and applied statistician with deep experience in taxonomy construction for multilingual papers, feature engineering for low-resource languages, and predictive modelling (regressors, ablations, error analysis).
Your job: **take a single input — a research report** — and produce an automatic, objective evaluation of the report along four separate axes: **Predictive plausibility**, **Feature selection**, **Coherence**, and **Citation emphasis**. For each axis you must return an **integer score 1–5** (1 = very poor, 5 = excellent) plus a short structured rationale and up to 3 concrete indicators (text spans or paraphrases from the report that justify the score). Use **only** the content present in the report; do **not** consult external sources or assume facts not stated.

---

**Input (one string):** the full report text to be graded.

**Hard output format (JSON only).**
Return **only** a single JSON object (no extra text). The object MUST contain these keys exactly:

* `predictive_plausibility`
* `feature_selection`
* `coherence`
* `citation_emphasis`
* `overall_recommendation`

Each metric object must follow this schema:

```json
{{{{
  "metric_name": "<metric_name>",
  "score": <integer 1-5>,
  "rationale": "<concise justification, max 50 words>",
  "indicators": ["<up to 3 short quotes or paraphrases from the report that support the score>"]
}}}}
```

`overall_recommendation` must be:

```json
"overall_recommendation": {{{{
  "average_score": <float, two decimals>,
  "verdict": "<one of: 'Accept', 'Minor revision', 'Major revision', 'Reject'>",
  "top_actionable_improvements": ["<up to 3 prioritized suggestions, max 12 words each>"]
}}}}
```

If a metric cannot be assessed from the report (insufficient information), set `"score": null`, give a one-line rationale explaining missing evidence, and leave `indicators` as an empty list.

---

## Scoring rubric (use this exact interpretation when assigning 1–5)

### 1) Predictive plausibility — degree to which the **predictions, prediction process, and reasoning about expected performance** are reasonable and well-justified. *(Focus on logic, assumptions, uncertainty, and sanity of claims — not numeric correctness.)*

* **5:** Clear, explicit assumptions; modeling choices justified; uncertainty quantified or discussed; plausible link from features → expected effect; error analysis or sanity checks present.
* **4:** Good justification and plausible reasoning; minor gaps (e.g., limited uncertainty discussion).
* **3:** Some plausible ideas but notable missing justifications or contradictory reasoning.
* **2:** Weak or ad-hoc predictive reasoning; unexplained leaps from features to expected outcomes.
* **1:** Implausible claims, contradictory or absent reasoning about predictions.

### 2) Feature selection — depth and expertise in choosing features for multilingual and low-resource performance analysis and prediction. *(Check: linguistically informed features, corpus measures, typology, tokenization, transfer signals, cross-lingual priors, normalization, and selection method.)*

* **5:** Expert-level rationale: features chosen with linguistic justification, interaction effects explored, selection method (e.g., LASSO, mutual info, ablation) and expected target impact described.
* **4:** Strong feature list with reasonable justifications; some missing depth about interactions or selection method.
* **3:** Useful features included but shallow rationale; key multilingual features missing or not justified.
* **2:** Feature choices appear generic or ill-suited to multilingual/low-resource specifics; little reasoning.
* **1:** No coherent feature rationale; features absent or irrelevant.

### 3) Coherence — logical organization, clarity of argument chain, consistency of terminology, and linguistic fluency of the report.

* **5:** Logical flow; claims follow from premises; clear definitions and consistent terminology; few/no language errors that impede understanding.
* **4:** Mostly coherent; minor organizational or phrasing issues.
* **3:** Fragmented arguments or occasional contradictions; several clarity issues.
* **2:** Disorganized, hard to follow, or contains contradictory statements.
* **1:** incoherent, contradictory, or unintelligible.

### 4) Citation emphasis — extent to which reasoning is **grounded in cited work** and whether claims are appropriately anchored to literature rather than being unsupported or unusual. *(Do not verify external correctness; judge whether the report *uses* citations to support key claims.)*

* **5:** Key claims and methods are tied to relevant citations; literature is used to justify design choices and contextualize assumptions.
* **4:** Many claims cited, but a few unsupported assertions remain.
* **3:** Some grounding, but important claims lack citations or rely on weak references.
* **2:** Sparse citation support; many claims unsupported.
* **1:** Virtually no citation grounding; unusual claims without references.

---

## Important Instructions

1. **Strictly follow the JSON schema.** Use integers 1–5 for `score` unless `null` as allowed. Rationales **≤ 50 words**. Indicators should be short extracts or paraphrases (≤ 20 words each).
2. When extracting indicators, quote or paraphrase the report text precisely enough to point to the evidence. Up to 3 per metric.
3. Compute `average_score` as the mean of the non-null metric scores; round to two decimals. Map average → `verdict`:

   * ≥ 4.25 → `"Accept"`
   * 3.25–4.24 → `"Minor revision"`
   * 2.5–3.24 → `"Major revision"`
   * < 2.5 → `"Reject"`
4. Provide `top_actionable_improvements` as three prioritized, short items (if fewer than three genuine items, fill remaining with concise low-priority suggestions).
5. **Do not** pad the output with commentary, explanations, or markdown. JSON object **only**.

---

### Example (for formatting reference only — do not output this example):

```json
{{
    metrics : [
    {{"metric_name": "predictive_plausibility", "score":5,"rationale":"...","indicators":["..."]}},
    {{"metric_name": "feature_selection", "score":4,"rationale":"...","indicators":["..."]}},
    {{"metric_name": "coherence", "score":3,"rationale":"...","indicators":["..."]}},
    {{"metric_name": "citation_emphasis", "score":2,"rationale":"...","indicators":["..."]}}
  ],
  "overall_recommendation":{{"average_score":3.50,"verdict":"Major revision","top_actionable_improvements":["...","...","..."]}}
}}
```

Start now. Process only the provided report text and return the JSON evaluation.

# Answer for the following report:
Report:
{report}

"""


# ============================================================================
# SCENARIO MAPPING UTILITIES
# ============================================================================

def build_question_to_scenario_map(questions_folder):
    """
    Build a mapping from question unique_id -> scenario number (1-5).
    This is loaded from generated_questions/*.json files where each file
    contains questions for a specific scenario.
    """
    uid_to_scenario = {}
    
    for question_file in glob.glob(os.path.join(questions_folder, "*.json")):
        with open(question_file, 'r', encoding='utf-8') as f:
            question_data = json.load(f)
        
        # Extract scenario number from the 'scenario' field (e.g., "scenario1" -> 1)
        scenario_str = question_data.get('scenario', '')
        scenario_num = None
        if scenario_str.startswith('scenario'):
            try:
                scenario_num = int(scenario_str.replace('scenario', ''))
            except ValueError:
                pass
        
        for question in question_data.get('questions', []):
            uid = question.get('unique_id')
            if uid and scenario_num:
                uid_to_scenario[uid] = scenario_num
    
    return uid_to_scenario


def get_scenario_label(question_id, scenario_folder, scenario_mode, uid_to_scenario):
    """
    Determine the actual scenario label for a question, based on the folder mode.
    
    For "split" mode:
      ScenarioPair_1 contains scenarios 1,2 -> label as "ScenarioPair_1"
      ScenarioPair_2 contains scenarios 3,4,5 -> label as "ScenarioPair_2"
    
    For "all_in_one" mode:
      ScenarioPair_1 contains all scenarios -> look up the actual scenario from questions mapping
      and map: scenario 1,2 -> "ScenarioPair_1", scenario 3,4,5 -> "ScenarioPair_2"
    
    This ensures consistent ScenarioPair labeling across all folders for comparison.
    """
    if scenario_mode == "split":
        # Already in the correct pair folder
        return scenario_folder
    
    elif scenario_mode == "all_in_one":
        # Need to look up the actual scenario and re-assign to the correct pair
        actual_scenario = uid_to_scenario.get(question_id)
        if actual_scenario in (1, 2):
            return "ScenarioPair_1"
        elif actual_scenario in (3, 4, 5):
            return "ScenarioPair_2"
        else:
            # Fallback if we can't determine - keep original
            return scenario_folder
    
    return scenario_folder


# ============================================================================
# EVALUATION FUNCTIONS
# ============================================================================

# Max report characters to send to LLM (~50K chars ≈ ~12K tokens)
MAX_REPORT_CHARS = 50000

def evaluate_single_report(report_text, query_id=None, task=None, scenario=None, folder_name=""):
    """Evaluate a single report and return the metrics."""
    # Truncate very long reports to avoid blowing up the context window
    original_len = len(report_text)
    if original_len > MAX_REPORT_CHARS:
        report_text = report_text[:MAX_REPORT_CHARS] + "\n\n[... TRUNCATED — report exceeded maximum length ...]"
        print(f"    [TRUNCATED] Report {query_id}: {original_len:,} -> {MAX_REPORT_CHARS:,} chars")
    
    # Use plain chat via round-robin parallel clients for 2x throughput
    fallback_prompt = (
        metric_prompt.format(report=report_text)
        + "\n\nIMPORTANT: Return ONLY the JSON object, no markdown fences, no extra text. "
        "Keep rationales under 30 words and indicators under 15 words each to stay concise."
    )
    client = _get_next_client()
    try:
        response = client.chat.completions.create(
            model=_PARALLEL_MODEL,
            messages=[{"role": "user", "content": fallback_prompt}],
        )
        raw = response.choices[0].message.content
    except Exception as e:
        raise ValueError(f"LLM call failed for query {query_id}: {e}")
    
    if not raw:
        raise ValueError(f"LLM returned empty for query {query_id}")
    
    # Clean response — strip markdown fences if present
    cleaned = str(raw).strip()
    if cleaned.startswith("```"):
        cleaned = _re.sub(r'^```(?:json)?\s*', '', cleaned)
        cleaned = _re.sub(r'\s*```$', '', cleaned)
    
    # Sanitize parsed JSON before Pydantic validation:
    # LLM sometimes returns null for score or indicators
    parsed = json.loads(cleaned)
    for metric in parsed.get("metrics", []):
        if metric.get("score") is None:
            metric["score"] = 1  # default to lowest score
        else:
            metric["score"] = int(metric["score"])
        if metric.get("rationale") is None:
            metric["rationale"] = ""
        if metric.get("indicators") is None:
            metric["indicators"] = []
    
    evaluation = CommonMetricEvaluation(**parsed)
    
    if query_id and task and scenario:
        store_individual_result(evaluation, query_id, task, scenario, folder_name, report_text)
    
    return evaluation


def store_individual_result(evaluation, query_id, task, scenario, folder_name, report_text):
    """Store individual LLM judge result for a query."""
    results_dir = os.path.join("llm_evals_scenario_task_thought", folder_name, task, scenario)
    os.makedirs(results_dir, exist_ok=True)
    
    result_data = {
        "query_id": query_id,
        "task": task,
        "scenario": scenario,
        "folder_source": folder_name,
        "original_report": report_text,
        "evaluation": {
            "metrics": [
                {
                    "metric_name": metric.metric_name,
                    "score": metric.score,
                    "rationale": metric.rationale,
                    "indicators": metric.indicators
                } for metric in evaluation.metrics
            ]
        }
    }
    
    if hasattr(evaluation, 'overall_recommendation') and evaluation.overall_recommendation:
        result_data["evaluation"]["overall_recommendation"] = {
            "average_score": evaluation.overall_recommendation.average_score,
            "verdict": evaluation.overall_recommendation.verdict,
            "top_actionable_improvements": evaluation.overall_recommendation.top_actionable_improvements
        }
    
    result_file = os.path.join(results_dir, f"{query_id}_judge_result.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)


def process_single_report_task_scenario(report_info, question_mapping, folder_name):
    """Process a single report file and return its evaluation."""
    try:
        with open(report_info['file_path'], 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        question_id = report_info['question_id']
        task = report_info['task']
        scenario = report_info['scenario']
        
        question_details = question_mapping.get(question_id, {})
        
        evaluation = evaluate_single_report(
            report_content, query_id=question_id, task=task,
            scenario=scenario, folder_name=folder_name
        )
        
        result = {
            'question_id': question_id,
            'task': task,
            'scenario': scenario,
            'question_details': question_details,
            'evaluation': evaluation,
            'processed_timestamp': datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        print(f"Error processing {report_info['file_path']}: {str(e)}")
        return None


# ============================================================================
# DATA LOADING
# ============================================================================

def load_question_mapping(questions_folder):
    """Load question mapping from generated questions folder."""
    question_mapping = {}
    
    for question_file in glob.glob(os.path.join(questions_folder, "*.json")):
        with open(question_file, 'r', encoding='utf-8') as f:
            question_data = json.load(f)
            
        task_name = question_data['task']
        scenario = question_data['scenario']
        
        for question in question_data['questions']:
            question_id = question['unique_id']
            question_mapping[question_id] = {
                'task': task_name,
                'scenario': scenario,
                'complete_question': question['complete_question'],
                'models': question.get('models', ''),
                'languages': question.get('languages', '')
            }
    
    return question_mapping


# ============================================================================
# CHECKPOINT & INTERMEDIATE SAVING
# ============================================================================

def load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
    return None


def save_checkpoint(checkpoint_file, data):
    try:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            serializable_data = json.loads(json.dumps(data, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x)))
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving checkpoint: {e}")


def save_intermediate_results(output_folder, detailed_results, processed_count, failed_count):
    intermediate_file = os.path.join(output_folder, f"intermediate_results_{processed_count}_items.json")
    
    intermediate_data = {
        'processed_count': processed_count,
        'failed_count': failed_count,
        'timestamp': datetime.now().isoformat(),
        'detailed_results': detailed_results
    }
    
    try:
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            serializable_data = json.loads(json.dumps(intermediate_data, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x)))
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        print(f"Intermediate results saved: {intermediate_file}")
    except Exception as e:
        print(f"Error saving intermediate results: {e}")


def get_progress_summary(output_folder):
    checkpoint_file = os.path.join(output_folder, "processing_checkpoint.json")
    if os.path.exists(checkpoint_file):
        checkpoint_data = load_checkpoint(checkpoint_file)
        if checkpoint_data:
            return {
                'processed': len(checkpoint_data.get('detailed_results', [])),
                'failed': checkpoint_data.get('failed_count', 0),
                'last_checkpoint': checkpoint_data.get('last_checkpoint', 'Unknown')
            }
    return {'processed': 0, 'failed': 0, 'last_checkpoint': 'None'}


# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_task_scenario_reports(reports_folder, questions_folder, output_folder,
                                  folder_name="", scenario_mode="split"):
    """
    Process all reports and calculate task and scenario-wise metrics.
    
    Args:
        reports_folder: Path to response folder (e.g., litmus_reagent_1_responses/)
        questions_folder: Path to generated_questions/
        output_folder: Where to save results
        folder_name: Label for this folder (used in outputs)
        scenario_mode: "split" or "all_in_one"
            - "split":      ScenarioPair_1 = scenarios {1,2}, ScenarioPair_2 = {3,4,5}
            - "all_in_one": ScenarioPair_1 = all scenarios {1,2,3,4,5}
    """
    os.makedirs(output_folder, exist_ok=True)
    
    checkpoint_file = os.path.join(output_folder, "processing_checkpoint.json")
    
    # Load checkpoint if it exists
    checkpoint_data = load_checkpoint(checkpoint_file)
    processed_questions = set()
    detailed_results = []
    
    if checkpoint_data:
        print(f"Found checkpoint with {len(checkpoint_data.get('detailed_results', []))} processed items")
        detailed_results = checkpoint_data.get('detailed_results', [])
        processed_questions = {result['question_id'] for result in detailed_results}
        print(f"Resuming from checkpoint with {len(processed_questions)} already processed questions")
    
    # Load question mapping
    print("Loading question mapping...")
    question_mapping = load_question_mapping(questions_folder)
    print(f"Loaded {len(question_mapping)} questions")
    
    # Build uid -> scenario number map (needed for all_in_one mode)
    uid_to_scenario = {}
    if scenario_mode == "all_in_one":
        print("Building question -> scenario number mapping (all_in_one mode)...")
        uid_to_scenario = build_question_to_scenario_map(questions_folder)
        print(f"Mapped {len(uid_to_scenario)} question IDs to scenario numbers")
    
    # Find all response.md files
    report_files = []
    for task_folder in sorted(os.listdir(reports_folder)):
        task_path = os.path.join(reports_folder, task_folder)
        if not os.path.isdir(task_path):
            continue
            
        for scenario_folder in sorted(os.listdir(task_path)):
            scenario_path = os.path.join(task_path, scenario_folder)
            if not os.path.isdir(scenario_path):
                continue
                
            for question_id in os.listdir(scenario_path):
                question_path = os.path.join(scenario_path, question_id)
                if not os.path.isdir(question_path):
                    continue
                    
                response_file = os.path.join(question_path, "response.md")
                if os.path.exists(response_file):
                    # Determine the correct scenario label
                    resolved_scenario = get_scenario_label(
                        question_id, scenario_folder, scenario_mode, uid_to_scenario
                    )
                    report_files.append({
                        'file_path': response_file,
                        'task': task_folder,
                        'scenario': resolved_scenario,
                        'question_id': question_id
                    })
    
    if not report_files:
        print(f"No response.md files found in {reports_folder}")
        return
    
    # Filter: only keep reports whose question_id exists in generated_questions
    valid_question_ids = set(question_mapping.keys())
    total_before_filter = len(report_files)
    report_files = [rf for rf in report_files if rf['question_id'] in valid_question_ids]
    skipped_extra = total_before_filter - len(report_files)
    
    if not report_files:
        print(f"No response.md files matched generated_questions in {reports_folder}")
        return
    
    print(f"\nFound {total_before_filter} total reports in {folder_name}")
    if skipped_extra > 0:
        print(f"Skipped {skipped_extra} reports not in generated_questions")
    print(f"Processing {len(report_files)} valid reports")
    print(f"Scenario mode: {scenario_mode}")
    
    # Show breakdown by task/scenario
    breakdown = defaultdict(lambda: defaultdict(int))
    for rf in report_files:
        breakdown[rf['task']][rf['scenario']] += 1
    for task in sorted(breakdown):
        for sc in sorted(breakdown[task]):
            print(f"  {task}/{sc}: {breakdown[task][sc]} reports")
    
    # Filter out already processed reports
    unprocessed_files = [rf for rf in report_files if rf['question_id'] not in processed_questions]
    print(f"\nFound {len(unprocessed_files)} unprocessed reports (skipping {len(report_files) - len(unprocessed_files)} already done)")
    
    if not unprocessed_files and detailed_results:
        print("All reports already processed. Generating final analysis...")
    else:
        processed_count = len(processed_questions)
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_report = {}
            for report_info in unprocessed_files:
                future = executor.submit(process_single_report_task_scenario, report_info, question_mapping, folder_name)
                future_to_report[future] = report_info
            
            for future in as_completed(future_to_report):
                report_info = future_to_report[future]
                try:
                    result = future.result()
                    if result:
                        detailed_results.append(result)
                        processed_count += 1
                        
                        print(f"Processed [{processed_count}]: {report_info['task']}/{report_info['scenario']}/{report_info['question_id']}")
                        
                        if processed_count % 10 == 0:
                            checkpoint_data = {
                                'detailed_results': detailed_results,
                                'last_checkpoint': datetime.now().isoformat(),
                                'processed_count': processed_count,
                                'failed_count': failed_count
                            }
                            save_checkpoint(checkpoint_file, checkpoint_data)
                            print(f"Checkpoint saved at {processed_count} processed items")
                        
                        if processed_count % 25 == 0:
                            save_intermediate_results(output_folder, detailed_results, processed_count, failed_count)
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Error processing {report_info['file_path']}: {str(e)}")
                    failed_count += 1
        
        # Final checkpoint save
        checkpoint_data = {
            'detailed_results': detailed_results,
            'last_checkpoint': datetime.now().isoformat(),
            'processed_count': processed_count,
            'failed_count': failed_count
        }
        save_checkpoint(checkpoint_file, checkpoint_data)
        save_intermediate_results(output_folder, detailed_results, processed_count, failed_count)
    
    # ============================
    # Calculate aggregated metrics
    # ============================
    print("\nCalculating aggregated metrics...")
    
    task_metrics = defaultdict(lambda: defaultdict(list))
    scenario_metrics = defaultdict(lambda: defaultdict(list))
    task_scenario_metrics = defaultdict(lambda: defaultdict(list))
    
    for result in detailed_results:
        task = result['task']
        scenario = result['scenario']
        evaluation = result['evaluation']
        
        if isinstance(evaluation, dict):
            metrics = evaluation.get('metrics', [])
        else:
            metrics = evaluation.metrics
        
        task_scenario_key = f"{task}_{scenario}"
        
        for metric in metrics:
            if isinstance(metric, dict):
                metric_name = metric.get('metric_name')
                score = metric.get('score')
            else:
                metric_name = metric.metric_name
                score = metric.score
                
            if score is not None:
                task_metrics[task][metric_name].append(score)
                scenario_metrics[scenario][metric_name].append(score)
                task_scenario_metrics[task_scenario_key][metric_name].append(score)
    
    total_processed = len(detailed_results)
    total_found = len(report_files)
    failed_count = checkpoint_data.get('failed_count', 0) if checkpoint_data else 0
    
    results = {
        'summary': {
            'total_reports': total_found,
            'processed_successfully': total_processed,
            'failed': failed_count,
            'scenario_mode': scenario_mode,
            'folder_name': folder_name,
        },
        'task_metrics': {},
        'scenario_metrics': {},
        'task_scenario_metrics': {},
        'detailed_results': detailed_results
    }
    
    # Calculate task-wise means
    for task, metrics in task_metrics.items():
        task_means = {}
        for metric_name, scores in metrics.items():
            if scores:
                task_means[metric_name] = {
                    'mean': mean(scores),
                    'count': len(scores),
                    'min': min(scores),
                    'max': max(scores),
                    'scores': sorted(scores)
                }
        if task_means:
            overall_mean = mean([m['mean'] for m in task_means.values()])
            task_means['overall_mean'] = overall_mean
        results['task_metrics'][task] = task_means
    
    # Calculate scenario-wise means
    for scenario, metrics in scenario_metrics.items():
        scenario_means = {}
        for metric_name, scores in metrics.items():
            if scores:
                scenario_means[metric_name] = {
                    'mean': mean(scores),
                    'count': len(scores),
                    'min': min(scores),
                    'max': max(scores),
                    'scores': sorted(scores)
                }
        if scenario_means:
            overall_mean = mean([m['mean'] for m in scenario_means.values()])
            scenario_means['overall_mean'] = overall_mean
        results['scenario_metrics'][scenario] = scenario_means
    
    # Calculate task-scenario combination means
    for task_scenario, metrics in task_scenario_metrics.items():
        ts_means = {}
        for metric_name, scores in metrics.items():
            if scores:
                ts_means[metric_name] = {
                    'mean': mean(scores),
                    'count': len(scores),
                    'min': min(scores),
                    'max': max(scores),
                    'scores': sorted(scores)
                }
        if ts_means:
            overall_mean = mean([m['mean'] for m in ts_means.values()])
            ts_means['overall_mean'] = overall_mean
        results['task_scenario_metrics'][task_scenario] = ts_means
    
    # Save results
    os.makedirs(output_folder, exist_ok=True)
    
    results_filename = f"task_scenario_metrics_analysis_{folder_name}.json" if folder_name else "task_scenario_metrics_analysis.json"
    results_file = os.path.join(output_folder, results_filename)
    with open(results_file, 'w', encoding='utf-8') as f:
        serializable_results = json.loads(json.dumps(results, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x)))
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    summary_file = generate_summary_report(results, output_folder, folder_name)
    save_intermediate_results(output_folder, detailed_results, total_processed, failed_count)
    
    # Clean up checkpoint file after successful completion
    if os.path.exists(checkpoint_file):
        try:
            os.remove(checkpoint_file)
            print("Checkpoint file cleaned up after successful completion")
        except Exception as e:
            print(f"Warning: Could not remove checkpoint file: {e}")
    
    print(f"\nResults saved to: {output_folder}")
    print(f"Detailed results: {results_file}")
    print(f"Summary report: {summary_file}")
    print(f"Individual LLM judge results stored in: llm_evals_scenario_task_thought/{folder_name}/")
    
    return results


# ============================================================================
# SUMMARY REPORT
# ============================================================================

def generate_summary_report(results, output_folder, folder_name=""):
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append(f"TASK AND SCENARIO-WISE METRICS ANALYSIS - {folder_name}")
    report_lines.append(f"Scenario mode: {results['summary'].get('scenario_mode', 'unknown')}")
    report_lines.append("=" * 80)
    
    summary = results['summary']
    report_lines.append(f"\nSUMMARY:")
    report_lines.append(f"  Total reports: {summary['total_reports']}")
    report_lines.append(f"  Processed successfully: {summary['processed_successfully']}")
    report_lines.append(f"  Failed: {summary['failed']}")
    report_lines.append(f"  Source folder: {folder_name}")
    
    # Task-wise metrics
    report_lines.append(f"\n{'=' * 80}")
    report_lines.append("TASK-WISE METRICS")
    report_lines.append("=" * 80)
    
    for task, metrics in sorted(results['task_metrics'].items()):
        report_lines.append(f"\n{task}:")
        if 'overall_mean' in metrics:
            report_lines.append(f"  Overall Mean: {metrics['overall_mean']:.2f}")
        for metric_name, stats in sorted(metrics.items()):
            if metric_name != 'overall_mean':
                report_lines.append(f"  {metric_name.replace('_', ' ').title():<25}: {stats['mean']:.2f} (n={stats['count']})")
    
    # Scenario-wise metrics
    report_lines.append(f"\n{'=' * 80}")
    report_lines.append("SCENARIO-WISE METRICS")
    report_lines.append("=" * 80)
    
    for scenario, metrics in sorted(results['scenario_metrics'].items()):
        report_lines.append(f"\n{scenario}:")
        if 'overall_mean' in metrics:
            report_lines.append(f"  Overall Mean: {metrics['overall_mean']:.2f}")
        for metric_name, stats in sorted(metrics.items()):
            if metric_name != 'overall_mean':
                report_lines.append(f"  {metric_name.replace('_', ' ').title():<25}: {stats['mean']:.2f} (n={stats['count']})")
    
    # Task-Scenario combination metrics
    report_lines.append(f"\n{'=' * 80}")
    report_lines.append("TASK-SCENARIO COMBINATION METRICS")
    report_lines.append("=" * 80)
    
    for task_scenario, metrics in sorted(results['task_scenario_metrics'].items()):
        report_lines.append(f"\n{task_scenario}:")
        if 'overall_mean' in metrics:
            report_lines.append(f"  Overall Mean: {metrics['overall_mean']:.2f}")
        for metric_name, stats in sorted(metrics.items()):
            if metric_name != 'overall_mean':
                report_lines.append(f"  {metric_name.replace('_', ' ').title():<25}: {stats['mean']:.2f} (n={stats['count']})")
    
    summary_filename = f"task_scenario_metrics_summary_{folder_name}.txt" if folder_name else "task_scenario_metrics_summary.txt"
    summary_file = os.path.join(output_folder, summary_filename)
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    for line in report_lines:
        print(line)
    
    return summary_file


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run text quality metrics on agent response folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run for litmus_reagent only:
  python run_text_metrics_configurable.py --folder litmus_reagent

  # Run for gpt4_baseline only:
  python run_text_metrics_configurable.py --folder gpt4_baseline

  # Run for magnetic_one only:
  python run_text_metrics_configurable.py --folder magnetic_one

  # Run for thought_agent only:
  python run_text_metrics_configurable.py --folder thought_agent

  # Run for ALL folders sequentially:
  python run_text_metrics_configurable.py --folder all

  # Run for specific folders:
  python run_text_metrics_configurable.py --folder litmus_reagent,thought_agent

  # Dry run (just show what would be processed, no LLM calls):
  python run_text_metrics_configurable.py --folder all --dry-run

  # Override output directory:
  python run_text_metrics_configurable.py --folder magnetic_one --output "C:\\custom\\output\\path"

  # Override questions directory:
  python run_text_metrics_configurable.py --folder all --questions "C:\\path\\to\\questions"
        """
    )
    
    parser.add_argument(
        '--folder', type=str, required=True,
        help='Folder config key(s) to process. Use comma-separated for multiple. '
             'Available: ' + ', '.join(FOLDER_CONFIGS.keys()) + ', all'
    )
    parser.add_argument(
        '--questions', type=str, default=QUESTIONS_FOLDER,
        help='Path to generated_questions folder'
    )
    parser.add_argument(
        '--output', type=str, default=OUTPUT_BASE,
        help='Base output directory'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Only show what would be processed, do not make LLM calls'
    )
    
    args = parser.parse_args()
    
    # Determine which folders to process
    if args.folder.lower() == 'all':
        folder_keys = list(FOLDER_CONFIGS.keys())
    else:
        folder_keys = [k.strip() for k in args.folder.split(',')]
    
    # Validate folder keys
    for key in folder_keys:
        if key not in FOLDER_CONFIGS:
            print(f"ERROR: Unknown folder key '{key}'. Available: {', '.join(FOLDER_CONFIGS.keys())}")
            sys.exit(1)
    
    questions_folder = args.questions
    output_base = args.output
    
    if not os.path.exists(questions_folder):
        print(f"ERROR: Questions folder does not exist: {questions_folder}")
        sys.exit(1)
    
    print("=" * 80)
    print("TEXT METRICS EVALUATION - CONFIGURABLE RUNNER")
    print("=" * 80)
    print(f"Folders to process: {folder_keys}")
    print(f"Questions folder:   {questions_folder}")
    print(f"Output base:        {output_base}")
    print(f"Dry run:            {args.dry_run}")
    print()
    
    # Process each folder
    for key in folder_keys:
        config = FOLDER_CONFIGS[key]
        reports_path = config["path"]
        scenario_mode = config["scenario_mode"]
        output_name = config["output_name"]
        
        print(f"\n{'#' * 80}")
        print(f"# PROCESSING: {key}")
        print(f"#   Path: {reports_path}")
        print(f"#   Scenario mode: {scenario_mode}")
        print(f"#   Output: {os.path.join(output_base, output_name)}")
        print(f"{'#' * 80}")
        
        if not os.path.exists(reports_path):
            print(f"WARNING: Reports folder does not exist: {reports_path}")
            continue
        
        folder_output = os.path.join(output_base, output_name)
        
        # Show current progress if resuming
        progress = get_progress_summary(folder_output)
        if progress['processed'] > 0:
            print(f"\nResuming from previous session:")
            print(f"  Already processed: {progress['processed']} reports")
            print(f"  Failed: {progress['failed']} reports")
            print(f"  Last checkpoint: {progress['last_checkpoint']}")
        
        if args.dry_run:
            # Dry run: just count files and show breakdown
            print("\n[DRY RUN] Scanning files...")
            uid_to_scenario = build_question_to_scenario_map(questions_folder) if scenario_mode == "all_in_one" else {}
            
            # Load question mapping to filter valid IDs
            q_mapping = load_question_mapping(questions_folder)
            valid_ids = set(q_mapping.keys())
            
            count = 0
            skipped = 0
            breakdown = defaultdict(lambda: defaultdict(int))
            for task_folder in sorted(os.listdir(reports_path)):
                task_path_full = os.path.join(reports_path, task_folder)
                if not os.path.isdir(task_path_full):
                    continue
                for sc_folder in sorted(os.listdir(task_path_full)):
                    sc_path = os.path.join(task_path_full, sc_folder)
                    if not os.path.isdir(sc_path):
                        continue
                    for qid in os.listdir(sc_path):
                        qid_path = os.path.join(sc_path, qid)
                        if os.path.isdir(qid_path) and os.path.exists(os.path.join(qid_path, "response.md")):
                            if qid not in valid_ids:
                                skipped += 1
                                continue
                            resolved = get_scenario_label(qid, sc_folder, scenario_mode, uid_to_scenario)
                            breakdown[task_folder][resolved] += 1
                            count += 1
            
            print(f"[DRY RUN] Valid response.md files: {count}")
            if skipped > 0:
                print(f"[DRY RUN] Skipped (not in generated_questions): {skipped}")
            for task in sorted(breakdown):
                for sc in sorted(breakdown[task]):
                    print(f"  {task}/{sc}: {breakdown[task][sc]}")
            
            already_done = progress['processed']
            print(f"[DRY RUN] Already processed: {already_done}")
            print(f"[DRY RUN] Remaining to process: {count - already_done}")
        else:
            process_task_scenario_reports(
                reports_folder=reports_path,
                questions_folder=questions_folder,
                output_folder=folder_output,
                folder_name=output_name,
                scenario_mode=scenario_mode,
            )
    
    print("\n" + "=" * 80)
    print("ALL DONE")
    print("=" * 80)
