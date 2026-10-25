"""
Special fallback for Code Generation ground truths using the additional_info/code_gen1.txt and code_gen2.txt files.
For questions without answers, uses these file contents to try to extract answers.
"""
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add root directory to path to import utils
root_dir = str(Path(__file__).resolve().parents[3])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utils.aoai_chat import get_chat_response

# Path to the additional info files
ADDITIONAL_INFO_FILE_1 = Path(__file__).parent / "additional_info" / "code_gen1.txt"
ADDITIONAL_INFO_FILE_2 = Path(__file__).parent / "additional_info" / "code_gen2.txt"


def load_code_gen_reference_data(file_num: int = 1) -> str:
    """Load the code_gen{file_num}.txt file content."""
    if file_num == 1:
        file_path = ADDITIONAL_INFO_FILE_1
    else:
        file_path = ADDITIONAL_INFO_FILE_2
    
    if not file_path.exists():
        print(f"Warning: {file_path} not found")
        return ""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def create_code_gen_fallback_prompt(user_query: str, reference_data: str, question_type: str) -> str:
    """
    Create LLM prompt for Code Generation ground truth using reference data.
    
    Args:
        user_query: The original user question
        reference_data: Content from code_gen1.txt
        question_type: Type of question (predictive/qna)
    
    Returns:
        Formatted prompt string
    """
    predictive_or_qna = "predictive" if question_type.lower() == "predictive" else "qna"
    
    prompt = f"""Extract ground truth answer from the reference data below.

USER QUERY: {user_query}
QUERY TYPE: {predictive_or_qna}

REFERENCE DATA (Code Generation Results - Languages are in ISO codes):
{reference_data}

INSTRUCTIONS:

1. DETERMINE is_answer_present:
   - Set to true ONLY if reference data contains a relevant, clear answer to the user query
   - The data contains code generation pass@1 results for various language-model combinations
   - Languages are in ISO codes (e.g., eng_Latn = English, deu_Latn = German, fra_Latn = French, etc.)
   - Models include: Claude3.5, GPT4o, GPT3.5, DeepSeek-Coder, WizardCoder, Aya
   - Set to false if no matching language/model found

2. FOR PREDICTIVE QUERIES (metrics questions):
   - Look for the EXACT language-model combination in the data
   - Extract the pass@1 score for that combination
   - For each metric, create an object with:
     * metric_name: "pass@1" (this is the metric in the data)
     * value: original value as string (e.g., "0.831")
     * value_in_100_range: value × 100 (e.g., 0.831 → 83.1)

3. FOR QNA QUERIES (comparison/best questions):
   - For "which model performs best" questions: find highest score for that language
   - For "which language performs best" questions: find highest score for that model
   - For comparisons: extract relevant values and determine answer
   - answer_text_for_qna should be CONCISE (model name, language, or value only)

4. LANGUAGE CODE MAPPING (common ones):
   - eng_Latn = English, deu_Latn = German, fra_Latn = French, spa_Latn = Spanish
   - zho_Hans = Chinese (Simplified), zho_Hant = Chinese (Traditional)
   - jpn_Jpan = Japanese, kor_Hang = Korean, hin_Deva = Hindi
   - arb_Arab = Arabic, rus_Cyrl = Russian, por_Latn = Portuguese
   - ita_Latn = Italian, nld_Latn = Dutch, pol_Latn = Polish
   - tur_Latn = Turkish, vie_Latn = Vietnamese, tha_Thai = Thai
   - ben_Beng = Bengali, tam_Taml = Tamil, urd_Arab = Urdu
   - heb_Hebr = Hebrew, ell_Grek = Greek, swe_Latn = Swedish
   - fin_Latn = Finnish, dan_Latn = Danish, nob_Latn/nno_Latn = Norwegian
   - ces_Latn = Czech, hun_Latn = Hungarian, ron_Latn = Romanian
   - ukr_Cyrl = Ukrainian, ind_Latn = Indonesian, zsm_Latn = Malay
   - tgl_Latn = Tagalog/Filipino, swh_Latn = Swahili
   - npi_Deva = Nepali, ory_Orya = Odia, kan_Knda = Kannada
   - mal_Mlym = Malayalam, tel_Telu = Telugu, mkd_Cyrl = Macedonian
   - mya_Mymr = Burmese, khm_Khmr = Khmer, sin_Sinh = Sinhala
   - kin_Latn = Kinyarwanda, sna_Latn = Shona, som_Latn = Somali
   - snd_Arab = Sindhi, pbt_Arab = Pashto, kir_Cyrl = Kyrgyz
   - tgk_Cyrl = Tajik, uig_Arab = Uyghur, ydd_Hebr = Yiddish
   - srd_Latn = Sardinian, tso_Latn = Tsonga, sag_Latn = Sango
   - sun_Latn = Sundanese, jav_Latn = Javanese, lug_Latn = Ganda
   - prs_Arab = Dari
   
5. CLASS INFORMATION:
   - Class 5: High-resource languages (eng, deu, fra, spa, zho, jpn, arb)
   - Class 4: Medium-high resource (hin, kor, rus, tur, etc.)
   - Class 3: Medium resource
   - Class 2: Low-medium resource
   - Class 1: Low resource languages
   - Class 0: Very low resource languages

OUTPUT FORMAT (strict JSON, no markdown, no explanation):

For PREDICTIVE:
{{
  "is_answer_present": true,
  "ground_truth_metrics_and_values_for_predictive": [
    {{
      "metric_name": "pass@1",
      "value": "0.831",
      "value_in_100_range": 83.1
    }}
  ],
  "answer_text_for_qna": ""
}}

For QNA:
{{
  "is_answer_present": true,
  "ground_truth_metrics_and_values_for_predictive": [],
  "answer_text_for_qna": "DeepSeek-Coder"
}}

For BOTH (when metrics exist AND there's a concise answer):
{{
  "is_answer_present": true,
  "ground_truth_metrics_and_values_for_predictive": [
    {{
      "metric_name": "pass@1",
      "value": "0.902",
      "value_in_100_range": 90.2
    }}
  ],
  "answer_text_for_qna": "DeepSeek-Coder"
}}

CRITICAL RULES:
- Use ONLY information from reference data above
- value_in_100_range must be NUMERIC ONLY (multiply decimal by 100)
- value keeps original format as string
- answer_text_for_qna must be CONCISE - NO full sentences
- Output valid JSON only
- If the EXACT language-model combination is NOT in the data, set is_answer_present to false
"""
    
    return prompt


def generate_ground_truth_from_reference(
    user_query: str, 
    reference_data: str, 
    question_type: str
) -> Dict:
    """
    Generate ground truth using LLM based on reference data file.
    
    Args:
        user_query: The original user question
        reference_data: Content from code_gen1.txt
        question_type: Type of question (predictive/qna)
    
    Returns:
        Dict with is_answer_present, ground_truth_metrics_and_values_for_predictive, answer_text_for_qna
    """
    try:
        prompt = create_code_gen_fallback_prompt(user_query, reference_data, question_type)
        
        response = get_chat_response(
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
        else:
            result = json.loads(response)
        
        # Validate structure
        if "is_answer_present" not in result:
            result["is_answer_present"] = False
        
        if result.get("ground_truth_metrics_and_values_for_predictive") is None:
            result["ground_truth_metrics_and_values_for_predictive"] = []
        elif not isinstance(result.get("ground_truth_metrics_and_values_for_predictive"), list):
            result["ground_truth_metrics_and_values_for_predictive"] = []
        
        if result.get("answer_text_for_qna") is None:
            result["answer_text_for_qna"] = ""
        elif not isinstance(result.get("answer_text_for_qna"), str):
            result["answer_text_for_qna"] = str(result.get("answer_text_for_qna", ""))
        
        return result
    
    except Exception as e:
        print(f"Error in fallback ground truth generation: {e}")
        return {
            "is_answer_present": False,
            "ground_truth_metrics_and_values_for_predictive": [],
            "answer_text_for_qna": ""
        }


def process_unanswered_code_gen_questions(ground_truths_file: Path, file_num: int = 1) -> int:
    """
    Process Code Generation ground truths file and try to answer unanswered questions
    using the reference data file.
    
    Args:
        ground_truths_file: Path to the ground truths JSON file
        file_num: Which reference file to use (1 or 2)
    
    Returns:
        Number of questions that got answers
    """
    if not ground_truths_file.exists():
        print(f"Error: {ground_truths_file} not found")
        return 0
    
    # Load reference data
    reference_data = load_code_gen_reference_data(file_num)
    if not reference_data:
        print("Error: Could not load reference data")
        return 0
    
    print(f"Using reference file: code_gen{file_num}.txt")
    
    # Load ground truths
    with open(ground_truths_file, 'r', encoding='utf-8') as f:
        ground_truths = json.load(f)
    
    if not isinstance(ground_truths, list):
        print("Error: Expected list format for ground truths")
        return 0
    
    # Find unanswered questions
    unanswered = [gt for gt in ground_truths if not gt.get('is_answer_present', False)]
    print(f"Found {len(unanswered)} unanswered questions out of {len(ground_truths)} total")
    
    if not unanswered:
        print("All questions already have answers!")
        return 0
    
    # Process each unanswered question
    updated_count = 0
    for gt in ground_truths:
        if gt.get('is_answer_present', False):
            continue  # Skip already answered
        
        unique_id = gt.get('unique_id', 'Unknown')
        complete_question = gt.get('complete_question', '')
        question_type = gt.get('predictive_or_qna', 'qna')
        
        print(f"\n{'='*50}")
        print(f"Processing: {unique_id}")
        print(f"Question: {complete_question[:100]}...")
        
        # Try to get answer from reference data
        result = generate_ground_truth_from_reference(
            complete_question, 
            reference_data, 
            question_type
        )
        
        if result.get('is_answer_present', False):
            # Update the ground truth
            gt['is_answer_present'] = True
            gt['ground_truth_metrics_and_values_for_predictive'] = result.get('ground_truth_metrics_and_values_for_predictive', [])
            gt['answer_text_for_qna'] = result.get('answer_text_for_qna', '')
            updated_count += 1
            print(f"✅ Got answer!")
            if result.get('ground_truth_metrics_and_values_for_predictive'):
                print(f"   Metrics: {result['ground_truth_metrics_and_values_for_predictive']}")
            if result.get('answer_text_for_qna'):
                print(f"   Answer: {result['answer_text_for_qna']}")
        else:
            print(f"❌ Could not find answer in reference data")
    
    # Save updated ground truths
    with open(ground_truths_file, 'w', encoding='utf-8') as f:
        json.dump(ground_truths, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"SUMMARY: Updated {updated_count}/{len(unanswered)} unanswered questions")
    print(f"Saved to: {ground_truths_file}")
    
    return updated_count


def main():
    """Run the Code Generation fallback for all scenarios."""
    from .config import OUTPUT_DIR
    
    parser = argparse.ArgumentParser(description="Code Generation Ground Truth Fallback")
    parser.add_argument('--scenario', type=int, help='Specific scenario to process (1-5)')
    parser.add_argument('--file', type=int, default=1, choices=[1, 2], 
                       help='Which reference file to use: 1 for code_gen1.txt, 2 for code_gen2.txt')
    args = parser.parse_args()
    
    output_dir = Path(OUTPUT_DIR)
    total_updated = 0
    
    if args.scenario:
        scenarios = [args.scenario]
    else:
        scenarios = range(1, 6)
    
    print(f"Using reference file: code_gen{args.file}.txt")
    
    for scenario in scenarios:
        gt_file = output_dir / f"01_Code_Generation_scenario_{scenario}_ground_truths.json"
        if gt_file.exists():
            print(f"\n{'#'*60}")
            print(f"Processing Scenario {scenario}")
            print(f"{'#'*60}")
            updated = process_unanswered_code_gen_questions(gt_file, args.file)
            total_updated += updated
        else:
            print(f"Skipping scenario {scenario}: file not found")
    
    print(f"\n{'#'*60}")
    print(f"TOTAL: Updated {total_updated} questions across all scenarios")
    print(f"{'#'*60}")


if __name__ == "__main__":
    main()
