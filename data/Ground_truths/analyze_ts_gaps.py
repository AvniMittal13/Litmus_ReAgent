"""Analyze unanswered TS questions to identify missing data sources."""
import json, re, os
from collections import Counter, defaultdict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

all_unanswered = []
for i in range(1, 6):
    f = f"05_Text_Summarization_scenario_{i}_ground_truths.json"
    data = json.load(open(f, "r", encoding="utf-8"))
    for q in data:
        if not q.get("is_answer_present"):
            all_unanswered.append({"scenario": i, "question": q["complete_question"], "id": q["unique_id"]})

print(f"Total unanswered: {len(all_unanswered)}/300\n")

# Extract model names and languages from questions
model_lang_pairs = []
model_counter = Counter()
lang_counter = Counter()
scenario_breakdown = defaultdict(list)

for item in all_unanswered:
    q = item["question"]
    s = item["scenario"]
    
    # Try to extract model name
    model_patterns = [
        r"(?:performance of|score does|well does|value (?:of|achieved by|for)) (.+?) (?:on|achieve|perform|for)",
        r"(?:score for|performance value of) (.+?) (?:on|in|for)",
    ]
    model = None
    for pat in model_patterns:
        m = re.search(pat, q, re.IGNORECASE)
        if m:
            model = m.group(1).strip()
            break
    
    # Try to extract language
    lang_match = re.search(r"(?:for|in) ([A-Z][a-z]+(?:\s*\([^)]+\))?(?:\s*[A-Z][a-z]+)?)\s*[\?\.]", q)
    lang = lang_match.group(1).strip() if lang_match else "Unknown"
    
    # For "which model" / "top-performing" questions
    if not model:
        best_match = re.search(r"(?:best|top|highest).*?(?:for|in) (.+?)[\?\.]", q, re.IGNORECASE)
        if best_match:
            lang = best_match.group(1).strip()
            model = "BEST_MODEL_QUERY"
    
    if not model:
        model = "UNKNOWN"
    
    model_counter[model] += 1
    lang_counter[lang] += 1
    scenario_breakdown[s].append((model, lang, q))

print("=" * 70)
print("UNANSWERED BY MODEL (frequency)")
print("=" * 70)
for model, count in model_counter.most_common():
    print(f"  {model}: {count}")

print(f"\n{'=' * 70}")
print("UNANSWERED BY LANGUAGE (frequency)")
print("=" * 70)
for lang, count in lang_counter.most_common():
    print(f"  {lang}: {count}")

print(f"\n{'=' * 70}")
print("UNANSWERED BY SCENARIO")
print("=" * 70)
for s in sorted(scenario_breakdown.keys()):
    items = scenario_breakdown[s]
    print(f"\n--- Scenario {s}: {len(items)} unanswered ---")
    # Group by model within scenario
    s_models = Counter()
    s_langs = Counter()
    for model, lang, q in items:
        s_models[model] += 1
        s_langs[lang] += 1
    print(f"  Models: {dict(s_models.most_common())}")
    print(f"  Languages: {dict(s_langs.most_common())}")

# Identify which papers/benchmarks would fill the gaps
print(f"\n{'=' * 70}")
print("MISSING DATA ANALYSIS - What papers/sources are needed?")
print("=" * 70)

# Group by paper/benchmark needed
gaps = defaultdict(list)
for item in all_unanswered:
    q = item["question"]
    s = item["scenario"]
    
    if any(m in q for m in ["mBART", "mBART-multilingual-BART"]):
        gaps["XL-Sum Paper (mBART model scores)"].append((s, q))
    elif any(m in q for m in ["Community-models"]):
        gaps["XL-Sum Paper (Community model baselines)"].append((s, q))
    elif any(m in q for m in ["Lead-3"]):
        gaps["XL-Sum Paper (Lead-3 baseline scores)"].append((s, q))
    elif any(m in q for m in ["m2m-proposed", "m2o"]):
        gaps["CrossSum Paper (m2m/m2o translation-summarization models)"].append((s, q))
    elif any(m in q for m in ["GPT-3.5-turbo-16k", "GPT-3.5"]):
        gaps["GPT-3.5 Paper (languages not in ts_gen5: Armenian, Kazakh, etc.)"].append((s, q))
    elif any(m in q for m in ["ChatGLM3"]):
        gaps["ChatGLM3 Paper (multilingual summarization)"].append((s, q))
    elif any(m in q for m in ["Vicuna-7B", "Vicuna"]):
        gaps["Vicuna Paper (multilingual summarization)"].append((s, q))
    elif any(m in q for m in ["mT5-official-baseline", "mT5-multilingual-T5", "multilingual-transformer", "mT5"]):
        # Check if it's about a language not in ts_gen1
        gaps["XL-Sum/mT5 Paper (languages not in ts_gen1: Serbian, Czech, Dutch, etc.)"].append((s, q))
    elif "best" in q.lower() or "top" in q.lower() or "highest" in q.lower():
        gaps["Best-model queries (need comprehensive benchmarks for: Albanian, Armenian, Estonian, Bulgarian, Georgian, Hebrew, Hungarian, Finnish, Kazakh, Czech, Dutch)"].append((s, q))
    elif any(m in q for m in ["DeepSeek"]):
        gaps["DeepSeek (language not in ts_gen4)"].append((s, q))
    else:
        gaps["Other/Unknown"].append((s, q))

for source, questions in sorted(gaps.items(), key=lambda x: -len(x[1])):
    scenarios = Counter(s for s, q in questions)
    print(f"\n{source}")
    print(f"  Count: {len(questions)} questions")
    print(f"  Scenarios: {dict(scenarios)}")
    # Show sample questions
    for s, q in questions[:3]:
        print(f"  S{s}: {q[:100]}...")
