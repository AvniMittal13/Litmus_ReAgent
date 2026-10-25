#!/usr/bin/env python3
"""
Evaluate Thought Creator Agent Performance across all runs.

Metrics:
1. Faithfulness Reflection (out of 3 thoughts)
   - Does each thought correctly reflect the reasoning steps suggested in the 
     expert knowledge/user_proxy message for thought_creator_agent?
   - Counts how many of the 3 generated thoughts faithfully follow guidance

2. System Capability Adherence (out of 3 thoughts)
   - Does each thought stay within system capabilities?
   - Penalizes suggestions of: fine-tuning, dataset creation, model downloads, 
     or other unavailable operations
   - Counts how many thoughts avoid suggesting unavailable capabilities

For each metric, returns a score out of 3 (number of thoughts satisfying criteria).

Output: JSON file with detailed results per conversation and overall metrics
"""
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_chat_response

def find_all_conversation_hierarchies(base_dir: str) -> List[Path]:
    """Find all conversation_hierarchy.json files in the response directory."""
    base_path = Path(base_dir)
    hierarchy_files = []
    
    for hierarchy_file in base_path.rglob("conversation_hierarchy.json"):
        hierarchy_files.append(hierarchy_file)
    
    return hierarchy_files

def extract_thought_creator_conversation(hierarchy_data: Dict) -> Tuple[str, str, List[Dict]]:
    """
    Extract the thought_creator_agent conversation from hierarchy.
    
    Returns:
        Tuple[str, str, List[Dict]]: (user_proxy_message, thought_creator_response, thought_paths)
    """
    try:
        main_convs = hierarchy_data.get("main_agent_conversations", [])
        
        # Find thought_creator_agent conversation
        thought_creator_conv = None
        for conv in main_convs:
            if conv.get("agent") == "thought_creator_agent":
                thought_creator_conv = conv
                break
        
        if not thought_creator_conv:
            return None, None, []
        
        messages = thought_creator_conv.get("messages", [])
        if len(messages) < 2:
            return None, None, []
        
        # First message is from user_proxy_agent (contains expert knowledge)
        user_proxy_message = messages[0].get("content", "")
        
        # Second message is from thought_creator_agent (contains JSON with thoughts)
        thought_creator_response = messages[1].get("content", "")
        
        # Parse JSON to extract thought_paths
        thought_paths = []
        try:
            # Extract JSON from the response
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', thought_creator_response, re.DOTALL)
            if json_match:
                thoughts_json = json.loads(json_match.group(1))
                thought_paths = thoughts_json.get("thought_paths", [])
        except json.JSONDecodeError:
            pass
        
        return user_proxy_message, thought_creator_response, thought_paths
    
    except Exception as e:
        print(f"Error extracting thought_creator conversation: {e}")
        return None, None, []

def evaluate_faithfulness_reflection(user_proxy_message: str, thought_paths: List[Dict]) -> Dict:
    """
    Evaluate how well each thought reflects the reasoning steps in expert knowledge.
    
    Uses LLM to analyze if each thought follows the guidance provided.
    
    Returns:
        Dict: {
            "faithful_thoughts_count": int (out of 3),
            "total_thoughts": int,
            "details": [{"thought_name": str, "is_faithful": bool, "explanation": str}]
        }
    """
    if not thought_paths:
        return {
            "faithful_thoughts_count": 0,
            "total_thoughts": 0,
            "details": []
        }
    
    prompt = f"""You are evaluating whether thought hypotheses correctly reflect reasoning guidance.

Expert Knowledge/Guidance (from user_proxy message):
{user_proxy_message}

Generated Thoughts:
{json.dumps(thought_paths, indent=2)}

For EACH of the {len(thought_paths)} thoughts, determine:
- Does the thought's method/approach align with the reasoning steps suggested in the expert knowledge?
- Does it follow the strategic guidance provided?

Respond with JSON:
{{"evaluations": [{{"thought_name": "<name>", "is_faithful": true/false, "explanation": "<brief reason>"}}]}}

Be strict: mark false if the thought significantly deviates from suggested approaches or ignores key guidance."""

    try:
        response = get_chat_response(
            messages=[{"role": "user", "content": prompt}],
            # temperature=0.0,
            # max_tokens=1000
        )        
        # Parse LLM response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
            evaluations = result.get("evaluations", [])
            
            faithful_count = sum(1 for e in evaluations if e.get("is_faithful", False))
            
            return {
                "faithful_thoughts_count": faithful_count,
                "total_thoughts": len(thought_paths),
                "details": evaluations
            }
    except Exception as e:
        print(f"Error in faithfulness evaluation: {e}")
    
    return {
        "faithful_thoughts_count": 0,
        "total_thoughts": len(thought_paths),
        "details": []
    }

def evaluate_system_capability_adherence(thought_paths: List[Dict]) -> Dict:
    """
    Evaluate if thoughts stay within system capabilities.
    
    Checks for prohibited suggestions: fine-tuning, dataset creation, model downloads, etc.
    
    Returns:
        Dict: {
            "compliant_thoughts_count": int (out of 3),
            "total_thoughts": int,
            "details": [{"thought_name": str, "is_compliant": bool, "violations": [str]}]
        }
    """
    if not thought_paths:
        return {
            "compliant_thoughts_count": 0,
            "total_thoughts": 0,
            "details": []
        }
    
    prompt = f"""You are evaluating whether thought hypotheses stay within system capabilities.

PROHIBITED suggestions (mark as non-compliant if suggested):
- Fine-tuning models
- Creating new datasets
- Downloading models locally
- Training new models from scratch
- Accessing external APIs not already available
- Creating infrastructure (servers, databases not already present)

Generated Thoughts:
{json.dumps(thought_paths, indent=2)}

For EACH of the {len(thought_paths)} thoughts, check the "method" field:
- Does it suggest any PROHIBITED operations?
- List any violations found

Respond with JSON:
{{"evaluations": [{{"thought_name": "<name>", "is_compliant": true/false, "violations": ["violation1", ...]}}]}}

Be strict: even mentioning these as options should be marked as non-compliant."""

    try:
        response = get_chat_response(
            messages=[{"role": "user", "content": prompt}],
            # temperature=0.0,
            # max_tokens=1000
        )
        
        # Parse LLM response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
            evaluations = result.get("evaluations", [])
            
            compliant_count = sum(1 for e in evaluations if e.get("is_compliant", False))
            
            return {
                "compliant_thoughts_count": compliant_count,
                "total_thoughts": len(thought_paths),
                "details": evaluations
            }
    except Exception as e:
        print(f"Error in capability adherence evaluation: {e}")
    
    return {
        "compliant_thoughts_count": 0,
        "total_thoughts": len(thought_paths),
        "details": []
    }

def analyze_conversation_hierarchy(hierarchy_path: Path) -> Dict:
    """
    Analyze a single conversation_hierarchy.json file.
    
    Returns:
        Dict with evaluation metrics
    """
    try:
        with open(hierarchy_path, 'r', encoding='utf-8') as f:
            hierarchy_data = json.load(f)
        
        user_proxy_msg, thought_response, thought_paths = extract_thought_creator_conversation(hierarchy_data)
        
        if not thought_paths:
            return {
                "file": str(hierarchy_path),
                "status": "no_thoughts_found",
                "faithfulness_reflection": None,
                "capability_adherence": None
            }
        
        # Evaluate both metrics
        faithfulness = evaluate_faithfulness_reflection(user_proxy_msg, thought_paths)
        capability = evaluate_system_capability_adherence(thought_paths)
        
        return {
            "file": str(hierarchy_path),
            "status": "success",
            "total_thoughts": len(thought_paths),
            "faithfulness_reflection": faithfulness,
            "capability_adherence": capability
        }
    
    except Exception as e:
        return {
            "file": str(hierarchy_path),
            "status": "error",
            "error": str(e)
        }

def calculate_overall_metrics(detailed_results: List[Dict]) -> Dict:
    """
    Calculate aggregate metrics across all conversation hierarchies.
    
    Returns:
        Dict with overall percentages
    """
    total_faithfulness_score = 0
    total_capability_score = 0
    total_thoughts = 0
    successful_analyses = 0
    
    for result in detailed_results:
        if result.get("status") == "success":
            successful_analyses += 1
            
            faithfulness = result.get("faithfulness_reflection", {})
            capability = result.get("capability_adherence", {})
            
            total_faithfulness_score += faithfulness.get("faithful_thoughts_count", 0)
            total_capability_score += capability.get("compliant_thoughts_count", 0)
            total_thoughts += result.get("total_thoughts", 0)
    
    # Calculate percentages
    faithfulness_percent = (total_faithfulness_score / total_thoughts * 100) if total_thoughts > 0 else 0
    capability_percent = (total_capability_score / total_thoughts * 100) if total_thoughts > 0 else 0
    
    return {
        "total_conversations_analyzed": len(detailed_results),
        "successful_analyses": successful_analyses,
        "total_thoughts_evaluated": total_thoughts,
        "faithfulness_reflection": {
            "thoughts_faithful": total_faithfulness_score,
            "total_thoughts": total_thoughts,
            "faithfulness_rate_percent": f"{faithfulness_percent:.2f}%"
        },
        "capability_adherence": {
            "thoughts_compliant": total_capability_score,
            "total_thoughts": total_thoughts,
            "compliance_rate_percent": f"{capability_percent:.2f}%"
        }
    }

def load_existing_results(output_file: str) -> Dict:
    """Load existing evaluation results if available."""
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load existing results: {e}")
    return {"overall_metrics": {}, "detailed_results": []}

def save_intermediate_results(output_file: str, detailed_results: List[Dict]):
    """Save intermediate results with recalculated overall metrics."""
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    
    overall_metrics = calculate_overall_metrics(detailed_results)
    
    output_data = {
        "overall_metrics": overall_metrics,
        "detailed_results": detailed_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate Thought Creator Agent Performance")
    parser.add_argument(
        "--input-dir",
        type=str,
        default=r"./final_testing_codes\task_scenario_new_final_2_responses",
        help="Base directory containing conversation_hierarchy.json files"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=r"./final_evals\FINAL_OUTCOMES\THOUGHT_CREATOR\thought_creator_evaluation_results2.json",
        help="Output JSON file path (e.g., 'final_evals/thought_creator_results.json')"
    )
    
    args = parser.parse_args()
    
    BASE_DIR = args.input_dir
    OUTPUT_FILE = args.output_file
    
    print("=" * 60)
    print("Thought Creator Agent Evaluation")
    print("=" * 60)
    print(f"\nInput Directory: {BASE_DIR}")
    print(f"Output File: {OUTPUT_FILE}")
    print(f"\nSearching for conversation_hierarchy.json files...\n")
    
    # Load existing results
    existing_data = load_existing_results(OUTPUT_FILE)
    existing_results = existing_data.get("detailed_results", [])
    processed_files = {result["file"] for result in existing_results}
    
    print(f"Loaded {len(existing_results)} previously processed files\n")
    
    # Find all conversation hierarchy files
    hierarchy_files = find_all_conversation_hierarchies(BASE_DIR)
    print(f"Found {len(hierarchy_files)} conversation hierarchy files\n")
    
    if not hierarchy_files:
        print("No conversation hierarchy files found. Exiting.")
        return
    
    # Filter out already processed files
    new_files = [f for f in hierarchy_files if str(f) not in processed_files]
    print(f"New files to process: {len(new_files)}\n")
    
    if not new_files:
        print("All files already processed. Recalculating overall metrics...")
        save_intermediate_results(OUTPUT_FILE, existing_results)
        print(f"✅ Updated results saved to: {OUTPUT_FILE}")
        return
    
    # Start with existing results
    detailed_results = existing_results.copy()
    
    # Analyze each new file
    for i, hierarchy_path in enumerate(new_files, 1):
        print(f"[{i}/{len(new_files)}] Analyzing: {hierarchy_path.name}")
        result = analyze_conversation_hierarchy(hierarchy_path)
        detailed_results.append(result)
        
        if result.get("status") == "success":
            faith = result.get("faithfulness_reflection", {})
            cap = result.get("capability_adherence", {})
            print(f"  Faithfulness: {faith.get('faithful_thoughts_count', 0)}/{result.get('total_thoughts', 0)}")
            print(f"  Capability: {cap.get('compliant_thoughts_count', 0)}/{result.get('total_thoughts', 0)}")
        
        # Save intermediate results after each file
        save_intermediate_results(OUTPUT_FILE, detailed_results)
        print(f"  ✅ Intermediate results saved")
    
    # Final save with updated metrics
    print("\n" + "=" * 60)
    print("Finalizing Results...")
    print("=" * 60)
    
    # Ensure output directory exists
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    
    save_intermediate_results(OUTPUT_FILE, detailed_results)
    overall_metrics = calculate_overall_metrics(detailed_results)
    
    print(f"\n✅ Final results saved to: {output_path.absolute()}\n")
    
    # Print summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Conversations: {overall_metrics['total_conversations_analyzed']}")
    print(f"Successful Analyses: {overall_metrics['successful_analyses']}")
    print(f"Total Thoughts Evaluated: {overall_metrics['total_thoughts_evaluated']}")
    print("\nFaithfulness Reflection:")
    print(f"  Faithful Thoughts: {overall_metrics['faithfulness_reflection']['thoughts_faithful']}/{overall_metrics['faithfulness_reflection']['total_thoughts']}")
    print(f"  Faithfulness Rate: {overall_metrics['faithfulness_reflection']['faithfulness_rate_percent']}")
    print("\nCapability Adherence:")
    print(f"  Compliant Thoughts: {overall_metrics['capability_adherence']['thoughts_compliant']}/{overall_metrics['capability_adherence']['total_thoughts']}")
    print(f"  Compliance Rate: {overall_metrics['capability_adherence']['compliance_rate_percent']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
