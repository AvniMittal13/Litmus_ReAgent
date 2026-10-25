#!/usr/bin/env python3
"""
Evaluate Generated Python Code Quality and Methodology.

This script analyzes all Python files in the generated_files folders to assess:
1. Algorithm/Methodology appropriateness for the task
2. Feature engineering and selection
3. Code structure and implementation quality
4. Statistical/ML approach correctness
5. Overall code sophistication

Each Python file is analyzed via LLM with a detailed prompt to extract:
- Algorithms/models used
- Features/variables utilized
- Methodology (statistical tests, ML approach, visualization techniques)
- Code quality indicators
- Appropriateness for research question

Output: JSON file with detailed analysis per file and aggregate metrics
"""
import sys
import json
import os
from pathlib import Path
from typing import Dict, List
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.aoai_chat import get_chat_response

def load_existing_results(output_file: Path) -> Dict:
    """
    Load existing results file if it exists.
    Returns dict with 'detailed_analyses' list and set of already-processed files.
    """
    if output_file.exists():
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            analyses = data.get('detailed_analyses', [])
            processed_files = {a.get('file_path') for a in analyses if a.get('file_path')}
            print(f"Loaded {len(analyses)} existing analyses from checkpoint file")
            return {'analyses': analyses, 'processed_files': processed_files}
        except Exception as e:
            print(f"Warning: Could not load existing results: {e}")
            print("Starting fresh...")
    return {'analyses': [], 'processed_files': set()}

def save_checkpoint(output_file: Path, analyses: List[Dict]):
    """
    Save current analyses and recalculated aggregate metrics to output file.
    """
    output_file.parent.mkdir(exist_ok=True, parents=True)
    
    aggregate = calculate_aggregate_metrics(analyses)
    output_data = {
        "aggregate_metrics": aggregate,
        "detailed_analyses": analyses
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

def find_all_python_files(base_dir: str) -> List[Path]:
    """Find all Python files in generated_files folders."""
    base_path = Path(base_dir)
    python_files = []
    
    # Search for all .py files within generated_files folders
    for py_file in base_path.rglob("generated_files/**/*.py"):
        python_files.append(py_file)
    
    return python_files

def analyze_python_code(py_file_path: Path) -> Dict:
    """
    Use LLM to comprehensively analyze a Python code file.
    
    Returns detailed analysis including algorithms, features, methodology, and quality assessment.
    """
    try:
        # Read the Python file
        with open(py_file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Extract context from file path
        relative_path = str(py_file_path)
        task_context = "Unknown Task"
        if "Code_Generation" in relative_path:
            task_context = "Code Generation"
        elif "Math_Reasoning" in relative_path:
            task_context = "Math Reasoning"
        elif "QA_VQA" in relative_path:
            task_context = "QA/VQA"
        elif "Classification" in relative_path:
            task_context = "Classification/NLI"
        elif "Text_Summarization" in relative_path:
            task_context = "Text Summarization"
        elif "Machine_Translation" in relative_path:
            task_context = "Machine Translation"
        
        # Try to extract user question from question_metadata.json
        user_question = "Not available"
        try:
            # Navigate up to the unique_id directory and look for question_metadata.json
            question_metadata_path = py_file_path.parents[2] / "question_metadata.json"
            if question_metadata_path.exists():
                with open(question_metadata_path, 'r', encoding='utf-8') as qf:
                    metadata = json.load(qf)
                    user_question = metadata.get('complete_question', 'Not available')
        except Exception:
            pass  # If we can't find the question, proceed without it
        
        prompt = f"""You are an expert code reviewer specializing in data science, machine learning, and research methodology. You are analyzing generated Python code to assess its quality, appropriateness, and sophistication.

**Context:**
- Task Domain: {task_context}
- User Question/Task: {user_question}
- File Path: {py_file_path.name}

**Python Code to Analyze:**
```python
{code_content}
```

**Your Task:**
Perform a comprehensive analysis of this code and provide a structured assessment. Consider the following dimensions:

0. **TASK-QUERY ALIGNMENT**
   - Does the code actually address the user's research question/task?
   - Is the approach appropriate for solving the stated problem?
   - Assess relevance and directness of the solution

1. **ALGORITHMS & MODELS**
   - Identify all algorithms, statistical methods, or ML models used
   - Assess appropriateness for the apparent research question
   - Note any advanced vs. basic techniques
   - Check for correct implementation

2. **FEATURES & VARIABLES**
   - List all key features/variables/columns used
   - Assess feature engineering sophistication (derived features, transformations, encodings)
   - Evaluate feature selection approach
   - Check for feature validity (do they make sense for the task?)

3. **METHODOLOGY & APPROACH**
   - Identify the overall analytical approach (regression, classification, clustering, visualization, etc.)
   - Assess statistical rigor (hypothesis testing, confidence intervals, validation)
   - Check for proper data preprocessing and handling
   - Evaluate model evaluation strategy (metrics, cross-validation, etc.)

4. **CODE STRUCTURE & QUALITY**
   - Assess code organization and readability
   - Check for proper error handling
   - Evaluate use of libraries and best practices
   - Note any code smells or issues

5. **RESEARCH APPROPRIATENESS**
   - Does the approach match what appears to be the research question?
   - Is the methodology scientifically sound?
   - Are appropriate assumptions made or tested?
   - Could this code produce meaningful insights?

6. **SOPHISTICATION LEVEL**
   - Rate complexity: Basic, Intermediate, Advanced
   - Identify any novel or creative approaches
   - Assess depth of analysis

**Output Requirements:**
Return ONLY a valid JSON object with this EXACT structure (no markdown, no explanation outside JSON):

{{
  "algorithms_used": ["list of algorithms/models/methods"],
  "algorithm_appropriateness": "appropriate|questionable|inappropriate",
  "algorithm_explanation": "brief explanation of why",
  
  "features_used": ["list of key features/variables"],
  "feature_count": 0,
  "feature_engineering_level": "none|basic|moderate|advanced",
  "feature_validity": "valid|partially_valid|invalid",
  "feature_explanation": "brief explanation",
  
  "methodology_type": "regression|classification|clustering|statistical_test|visualization|data_analysis|other",
  "methodology_rigor": "high|moderate|low",
  "methodology_explanation": "brief explanation",
  
  "data_preprocessing": ["list of preprocessing steps"],
  "evaluation_metrics": ["list of metrics used"],
  "validation_approach": "description of validation if any",
  
  "code_quality": "excellent|good|fair|poor",
  "code_issues": ["list of issues if any"],
  
  "task_query_alignment": "well_aligned|moderately_aligned|poorly_aligned|not_applicable",
  "task_query_explanation": "brief explanation of how code addresses the user's question",
  
  "research_alignment": "well_aligned|moderately_aligned|poorly_aligned",
  "research_soundness": "sound|questionable|unsound",
  "research_explanation": "brief explanation",
  
  "sophistication_level": "basic|intermediate|advanced",
  "novel_approaches": ["any creative/novel techniques"],
  
  "overall_assessment": "excellent|good|fair|poor",
  "strengths": ["list key strengths"],
  "weaknesses": ["list key weaknesses"],
  "summary": "1-2 sentence overall summary"
}}

**Important:**
- Be objective and evidence-based
- Consider the apparent context and goals
- Focus on what the code DOES, not what it COULD do
- Rate appropriateness relative to typical research standards
- Be concise but specific in explanations
"""

        response = get_chat_response(
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Extract JSON from response
        content = response.strip()
        
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        
        # Remove any leading/trailing text outside JSON
        start_brace = content.find('{')
        end_brace = content.rfind('}')
        if start_brace != -1 and end_brace != -1:
            content = content[start_brace:end_brace+1]
        
        # Parse JSON
        analysis = json.loads(content)
        
        # Add metadata
        analysis["file_path"] = str(py_file_path)
        analysis["file_name"] = py_file_path.name
        analysis["task_context"] = task_context
        analysis["code_length_lines"] = len(code_content.split('\n'))
        
        return analysis
        
    except Exception as e:
        print(f"  ❌ Error analyzing {py_file_path.name}: {e}")
        return {
            "file_path": str(py_file_path),
            "file_name": py_file_path.name,
            "error": str(e),
            "analysis_failed": True
        }

def calculate_aggregate_metrics(analyses: List[Dict]) -> Dict:
    """Calculate aggregate metrics from all code analyses."""
    # Filter out failed analyses
    valid_analyses = [a for a in analyses if not a.get("analysis_failed")]
    
    if not valid_analyses:
        return {
            "total_files": len(analyses),
            "successfully_analyzed": 0,
            "failed_analyses": len(analyses)
        }
    
    # Algorithm appropriateness
    algo_appropriate = sum(1 for a in valid_analyses if a.get("algorithm_appropriateness") == "appropriate")
    algo_questionable = sum(1 for a in valid_analyses if a.get("algorithm_appropriateness") == "questionable")
    algo_inappropriate = sum(1 for a in valid_analyses if a.get("algorithm_appropriateness") == "inappropriate")
    
    # Feature engineering levels
    feature_levels = {}
    for level in ["none", "basic", "moderate", "advanced"]:
        feature_levels[level] = sum(1 for a in valid_analyses if a.get("feature_engineering_level") == level)
    
    # Methodology rigor
    rigor_high = sum(1 for a in valid_analyses if a.get("methodology_rigor") == "high")
    rigor_moderate = sum(1 for a in valid_analyses if a.get("methodology_rigor") == "moderate")
    rigor_low = sum(1 for a in valid_analyses if a.get("methodology_rigor") == "low")
    
    # Code quality
    quality_excellent = sum(1 for a in valid_analyses if a.get("code_quality") == "excellent")
    quality_good = sum(1 for a in valid_analyses if a.get("code_quality") == "good")
    quality_fair = sum(1 for a in valid_analyses if a.get("code_quality") == "fair")
    quality_poor = sum(1 for a in valid_analyses if a.get("code_quality") == "poor")
    
    # Research alignment
    align_well = sum(1 for a in valid_analyses if a.get("research_alignment") == "well_aligned")
    align_moderate = sum(1 for a in valid_analyses if a.get("research_alignment") == "moderately_aligned")
    align_poor = sum(1 for a in valid_analyses if a.get("research_alignment") == "poorly_aligned")
    
    # Sophistication levels
    sophistication = {}
    for level in ["basic", "intermediate", "advanced"]:
        sophistication[level] = sum(1 for a in valid_analyses if a.get("sophistication_level") == level)
    
    # Overall assessment
    overall_excellent = sum(1 for a in valid_analyses if a.get("overall_assessment") == "excellent")
    overall_good = sum(1 for a in valid_analyses if a.get("overall_assessment") == "good")
    overall_fair = sum(1 for a in valid_analyses if a.get("overall_assessment") == "fair")
    overall_poor = sum(1 for a in valid_analyses if a.get("overall_assessment") == "poor")
    
    # Average metrics
    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0
    total = len(valid_analyses)
    avg_feature_count = sum(safe_int(a.get("feature_count", 0)) for a in valid_analyses) / total if total > 0 else 0
    avg_code_lines = sum(safe_int(a.get("code_length_lines", 0)) for a in valid_analyses) / total if total > 0 else 0
    
    return {
        "total_files": len(analyses),
        "successfully_analyzed": len(valid_analyses),
        "failed_analyses": len(analyses) - len(valid_analyses),
        
        "algorithm_appropriateness": {
            "appropriate": algo_appropriate,
            "questionable": algo_questionable,
            "inappropriate": algo_inappropriate,
            "appropriate_percentage": f"{(algo_appropriate/total*100):.1f}%" if total > 0 else "0%"
        },
        
        "feature_engineering": {
            **feature_levels,
            "average_features_per_file": f"{avg_feature_count:.1f}"
        },
        
        "methodology_rigor": {
            "high": rigor_high,
            "moderate": rigor_moderate,
            "low": rigor_low,
            "high_percentage": f"{(rigor_high/total*100):.1f}%" if total > 0 else "0%"
        },
        
        "code_quality": {
            "excellent": quality_excellent,
            "good": quality_good,
            "fair": quality_fair,
            "poor": quality_poor,
            "excellent_or_good": quality_excellent + quality_good,
            "excellent_or_good_percentage": f"{((quality_excellent+quality_good)/total*100):.1f}%" if total > 0 else "0%"
        },
        
        "research_alignment": {
            "well_aligned": align_well,
            "moderately_aligned": align_moderate,
            "poorly_aligned": align_poor,
            "well_aligned_percentage": f"{(align_well/total*100):.1f}%" if total > 0 else "0%"
        },
        
        "sophistication": {
            **sophistication,
            "intermediate_or_advanced": sophistication.get("intermediate", 0) + sophistication.get("advanced", 0),
            "intermediate_or_advanced_percentage": f"{((sophistication.get('intermediate', 0)+sophistication.get('advanced', 0))/total*100):.1f}%" if total > 0 else "0%"
        },
        
        "overall_assessment": {
            "excellent": overall_excellent,
            "good": overall_good,
            "fair": overall_fair,
            "poor": overall_poor,
            "excellent_or_good_percentage": f"{((overall_excellent+overall_good)/total*100):.1f}%" if total > 0 else "0%"
        },
        
        "code_statistics": {
            "average_code_lines": f"{avg_code_lines:.0f}",
            "total_code_lines": sum(a.get("code_length_lines", 0) for a in valid_analyses)
        }
    }

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate Generated Python Code Quality")
    parser.add_argument(
        "--input-dir",
        type=str,
        default=r"./final_testing_codes\task_scenario_new_final_2_responses",
        help="Base directory containing generated_files folders"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="final_evals/FINAL_OUTCOMES/CODE_ANALYSIS2/generated_code_evaluation_results.json",
        help="Output JSON file path"
    )
    
    args = parser.parse_args()
    
    base_dir = args.input_dir
    output_file = Path(args.output_file)
    
    print(f"Input Directory: {base_dir}")
    print(f"Output File: {output_file}")
    print("="*80)
    
    print("\nLoading existing results (if any)...")
    checkpoint_data = load_existing_results(output_file)
    analyses = checkpoint_data['analyses']
    processed_files = checkpoint_data['processed_files']
    
    print("\nFinding all Python files in generated_files folders...")
    py_files = find_all_python_files(base_dir)
    print(f"Found {len(py_files)} Python files total")
    
    # Filter out already-processed files
    pending_files = [f for f in py_files if str(f) not in processed_files]
    print(f"Already processed: {len(py_files) - len(pending_files)}")
    print(f"Pending analysis: {len(pending_files)}\n")
    
    if not pending_files:
        print("All files already analyzed!")
        print("\nRecalculating aggregate metrics from existing data...")
        save_checkpoint(output_file, analyses)
        print(f"\n✓ Results saved to: {output_file.absolute()}")
        return
    
    print("Analyzing Python files...")
    print("(This may take several minutes depending on file count)\n")
    
    for i, py_file in enumerate(pending_files, 1):
        rel_path = py_file.relative_to(Path(base_dir))
        total_analyzed = len(analyses) + i
        print(f"[{total_analyzed}/{len(py_files)}] Analyzing: {rel_path}")
        
        analysis = analyze_python_code(py_file)
        analyses.append(analysis)
        
        if not analysis.get("analysis_failed"):
            print(f"  ✓ Quality: {analysis.get('code_quality', 'N/A')}, "
                  f"Sophistication: {analysis.get('sophistication_level', 'N/A')}, "
                  f"Overall: {analysis.get('overall_assessment', 'N/A')}")
        else:
            print(f"  ✗ Analysis failed")
        
        # Save checkpoint after each file
        save_checkpoint(output_file, analyses)
        
        # Add a small delay to avoid rate limiting
        if i % 10 == 0 and i < len(pending_files):
            print("  (Pausing briefly to avoid rate limits...)")
            import time
            time.sleep(2)
    
    print("\n" + "="*80)
    print("AGGREGATE METRICS")
    print("="*80)
    
    aggregate = calculate_aggregate_metrics(analyses)
    
    print(f"\nTotal Files Analyzed: {aggregate['total_files']}")
    print(f"Successfully Analyzed: {aggregate['successfully_analyzed']}")
    print(f"Failed Analyses: {aggregate['failed_analyses']}")
    
    print("\n1. ALGORITHM APPROPRIATENESS:")
    print(f"   Appropriate: {aggregate['algorithm_appropriateness']['appropriate']} ({aggregate['algorithm_appropriateness']['appropriate_percentage']})")
    print(f"   Questionable: {aggregate['algorithm_appropriateness']['questionable']}")
    print(f"   Inappropriate: {aggregate['algorithm_appropriateness']['inappropriate']}")
    
    print("\n2. FEATURE ENGINEERING:")
    print(f"   Advanced: {aggregate['feature_engineering']['advanced']}")
    print(f"   Moderate: {aggregate['feature_engineering']['moderate']}")
    print(f"   Basic: {aggregate['feature_engineering']['basic']}")
    print(f"   None: {aggregate['feature_engineering']['none']}")
    print(f"   Avg Features/File: {aggregate['feature_engineering']['average_features_per_file']}")
    
    print("\n3. METHODOLOGY RIGOR:")
    print(f"   High: {aggregate['methodology_rigor']['high']} ({aggregate['methodology_rigor']['high_percentage']})")
    print(f"   Moderate: {aggregate['methodology_rigor']['moderate']}")
    print(f"   Low: {aggregate['methodology_rigor']['low']}")
    
    print("\n4. CODE QUALITY:")
    print(f"   Excellent: {aggregate['code_quality']['excellent']}")
    print(f"   Good: {aggregate['code_quality']['good']}")
    print(f"   Fair: {aggregate['code_quality']['fair']}")
    print(f"   Poor: {aggregate['code_quality']['poor']}")
    print(f"   Excellent/Good: {aggregate['code_quality']['excellent_or_good_percentage']}")
    
    print("\n5. RESEARCH ALIGNMENT:")
    print(f"   Well Aligned: {aggregate['research_alignment']['well_aligned']} ({aggregate['research_alignment']['well_aligned_percentage']})")
    print(f"   Moderately Aligned: {aggregate['research_alignment']['moderately_aligned']}")
    print(f"   Poorly Aligned: {aggregate['research_alignment']['poorly_aligned']}")
    
    print("\n6. SOPHISTICATION:")
    print(f"   Advanced: {aggregate['sophistication']['advanced']}")
    print(f"   Intermediate: {aggregate['sophistication']['intermediate']}")
    print(f"   Basic: {aggregate['sophistication']['basic']}")
    print(f"   Intermediate+: {aggregate['sophistication']['intermediate_or_advanced_percentage']}")
    
    print("\n7. OVERALL ASSESSMENT:")
    print(f"   Excellent: {aggregate['overall_assessment']['excellent']}")
    print(f"   Good: {aggregate['overall_assessment']['good']}")
    print(f"   Fair: {aggregate['overall_assessment']['fair']}")
    print(f"   Poor: {aggregate['overall_assessment']['poor']}")
    print(f"   Excellent/Good: {aggregate['overall_assessment']['excellent_or_good_percentage']}")
    
    # Save final results with updated aggregate metrics
    print(f"\n✓ Final results saved to: {output_file.absolute()}")
    print("="*80)

if __name__ == "__main__":
    main()
