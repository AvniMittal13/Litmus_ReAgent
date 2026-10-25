#!/usr/bin/env python3
"""
Configuration file for question generation scenarios.

This script centralizes all configuration parameters and provides
a unified interface to run all question generation scenarios.

Usage:
    python config.py                    # Run all scenarios
    python config.py --scenario 1      # Run specific scenario
    python config.py --scenario 1,3,5  # Run multiple scenarios
    python config.py --help            # Show help
"""

import os
import sys
import argparse
import subprocess
import time
import importlib.util
from typing import List, Dict, Optional
from pathlib import Path

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# =====================================
# CONFIGURATION PARAMETERS
# =====================================

class QuestionGenerationConfig:
    """Centralized configuration for all question generation scenarios."""
    
    # === QUESTION COUNTS PER SCENARIO ===
    QUESTION_COUNTS = {
        1: 60,  # Scenario 1: Same language, same model
        2: 60,  # Scenario 2: Same language, different model  
        3: 60,  # Scenario 3: Different language, same model
        4: 60,  # Scenario 4: Different language, different model (with gap data)
        5: 60,  # Scenario 5: Different language, different model (no gap data)
    }
    
    # === OUTPUT DIRECTORY ===
    OUTPUT_DIR = "generated_questions"
    
    # === BASE DATA PATH ===
    BASE_DATA_PATH = r"./all_final_csvs_finall"
    
    # === SCENARIO SCRIPTS ===
    SCENARIO_SCRIPTS = {
        1: "generate_que_scenario1.py",
        2: "generate_que_scenario2.py", 
        3: "generate_que_scenario3.py",
        4: "generate_que_scenario4.py",
        5: "generate_que_scenario5_retry.py",
    }
    
    # === SCENARIO FUNCTION NAMES ===
    SCENARIO_FUNCTIONS = {
        1: "process_all_tasks",
        2: "process_all_tasks_scenario2",
        3: "process_all_tasks_scenario3", 
        4: "process_all_tasks_scenario4",
        5: "process_all_tasks_scenario5",
    }
    
    # === EXECUTION MODES ===
    # Set to True to import and call functions directly (faster)
    # Set to False to use subprocess calls (safer, but slower)
    USE_DIRECT_IMPORT = True
    # === SCENARIO DESCRIPTIONS ===
    SCENARIO_DESCRIPTIONS = {
        1: "Same Language, Same Model",
        2: "Same Language, Different Model",
        3: "Different Language, Same Model", 
        4: "Different Language, Different Model (with gap language data)",
        5: "Different Language, Different Model (no gap language data)",
    }
    
    @classmethod
    def get_question_count(cls, scenario: int) -> int:
        """Get the number of questions for a specific scenario."""
        return cls.QUESTION_COUNTS.get(scenario, 50)
    
    @classmethod
    def get_script_path(cls, scenario: int) -> str:
        """Get the script path for a specific scenario."""
        script_dir = Path(__file__).parent
        return str(script_dir / cls.SCENARIO_SCRIPTS.get(scenario, f"generate_que_scenario{scenario}.py"))
    
    @classmethod
    def get_function_name(cls, scenario: int) -> str:
        """Get the function name for a specific scenario."""
        return cls.SCENARIO_FUNCTIONS.get(scenario, f"process_all_tasks_scenario{scenario}")
    
    @classmethod
    def get_scenario_description(cls, scenario: int) -> str:
        """Get the description for a specific scenario."""
        return cls.SCENARIO_DESCRIPTIONS.get(scenario, f"Scenario {scenario}")


# =====================================
# UTILITY FUNCTIONS
# =====================================

def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_config_summary():
    """Print the current configuration summary."""
    print_header("QUESTION GENERATION CONFIGURATION")
    
    print(f"📁 Output Directory: {QuestionGenerationConfig.OUTPUT_DIR}")
    print(f"📂 Base Data Path: {QuestionGenerationConfig.BASE_DATA_PATH}")
    print(f"🎯 Total Scenarios: {len(QuestionGenerationConfig.SCENARIO_SCRIPTS)}")
    
    print("\n📊 Question Counts per Scenario:")
    for scenario, count in QuestionGenerationConfig.QUESTION_COUNTS.items():
        desc = QuestionGenerationConfig.get_scenario_description(scenario)
        print(f"  Scenario {scenario}: {count:2d} questions - {desc}")
    
    print(f"\n📄 Available Scripts:")
    for scenario, script in QuestionGenerationConfig.SCENARIO_SCRIPTS.items():
        print(f"  Scenario {scenario}: {script}")


def validate_environment():
    """Validate that all required files and paths exist."""
    print_header("ENVIRONMENT VALIDATION")
    
    errors = []
    
    # Check base data path
    if not os.path.exists(QuestionGenerationConfig.BASE_DATA_PATH):
        errors.append(f"❌ Base data path not found: {QuestionGenerationConfig.BASE_DATA_PATH}")
    else:
        print(f"✅ Base data path exists: {QuestionGenerationConfig.BASE_DATA_PATH}")
    
    # Check scenario scripts
    for scenario, script in QuestionGenerationConfig.SCENARIO_SCRIPTS.items():
        script_path = QuestionGenerationConfig.get_script_path(scenario)
        if not os.path.exists(script_path):
            errors.append(f"❌ Scenario {scenario} script not found: {script_path}")
        else:
            print(f"✅ Scenario {scenario} script found: {script}")
    
    # Check output directory (create if doesn't exist)
    output_dir = Path(QuestionGenerationConfig.OUTPUT_DIR)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created output directory: {QuestionGenerationConfig.OUTPUT_DIR}")
    else:
        print(f"✅ Output directory exists: {QuestionGenerationConfig.OUTPUT_DIR}")
    
    if errors:
        print("\n❌ VALIDATION ERRORS:")
        for error in errors:
            print(f"  {error}")
        return False
    
    print("\n✅ All validations passed!")
    return True


def import_scenario_module(scenario: int):
    """Import a scenario module dynamically."""
    script_path = QuestionGenerationConfig.get_script_path(scenario)
    
    if not os.path.exists(script_path):
        raise ImportError(f"Scenario {scenario} script not found: {script_path}")
    
    # Create module spec
    module_name = f"scenario_{scenario}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create module spec for {script_path}")
    
    # Import the module
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    return module


def run_scenario_direct(scenario: int) -> bool:
    """Run a scenario by directly importing and calling the function."""
    try:
        # Import the scenario module
        module = import_scenario_module(scenario)
        
        # Get the function name and parameters
        function_name = QuestionGenerationConfig.get_function_name(scenario)
        question_count = QuestionGenerationConfig.get_question_count(scenario)
        base_path = QuestionGenerationConfig.BASE_DATA_PATH
        
        # Get the function
        if not hasattr(module, function_name):
            print(f"❌ Function '{function_name}' not found in scenario {scenario} module")
            return False
        
        process_function = getattr(module, function_name)
        
        # Call the function with appropriate parameters
        print(f"🔧 Calling {function_name}(base_path='{base_path}', num_questions_per_task={question_count})")
        
        # Capture any output by redirecting stdout temporarily
        import io
        from contextlib import redirect_stdout
        
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            process_function(base_path=base_path, num_questions_per_task=question_count)
        
        # Get the captured output
        captured_output = output_buffer.getvalue()
        
        # Print the output
        if captured_output.strip():
            print("📄 Function output:")
            print(captured_output)
        
        return True
        
    except Exception as e:
        print(f"❌ Error running scenario {scenario} directly: {e}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False


def run_scenario_subprocess(scenario: int) -> bool:
    """Run a scenario using subprocess (original method)."""
    script_path = QuestionGenerationConfig.get_script_path(scenario)
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        print(f"🚀 Starting scenario {scenario} generation via subprocess...")
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            # Show output summary if available
            if result.stdout:
                print("📄 Script output:")
                print(result.stdout.strip())
            return True
        else:
            print(f"❌ Scenario {scenario} failed!")
            print(f"Exit code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error running scenario {scenario}: {e}")
        return False


def run_scenario(scenario: int) -> bool:
    """Run a specific scenario generation script."""
    script_path = QuestionGenerationConfig.get_script_path(scenario)
    desc = QuestionGenerationConfig.get_scenario_description(scenario)
    count = QuestionGenerationConfig.get_question_count(scenario)
    
    print_header(f"RUNNING SCENARIO {scenario}: {desc}")
    print(f"📝 Questions to generate: {count}")
    print(f"📄 Script: {os.path.basename(script_path)}")
    print(f"📁 Output: {QuestionGenerationConfig.OUTPUT_DIR}")
    print(f"🔧 Execution mode: {'Direct Import' if QuestionGenerationConfig.USE_DIRECT_IMPORT else 'Subprocess'}")
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    # Record start time
    start_time = time.time()
    
    # Choose execution method
    if QuestionGenerationConfig.USE_DIRECT_IMPORT:
        success = run_scenario_direct(scenario)
    else:
        success = run_scenario_subprocess(scenario)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    if success:
        print(f"✅ Scenario {scenario} completed successfully!")
        print(f"⏱️ Execution time: {execution_time:.2f} seconds")
    else:
        print(f"❌ Scenario {scenario} failed!")
        print(f"⏱️ Execution time: {execution_time:.2f} seconds")
    
    return success


def run_multiple_scenarios(scenarios: List[int]) -> Dict[int, bool]:
    """Run multiple scenarios and return results."""
    results = {}
    
    print_header(f"RUNNING {len(scenarios)} SCENARIOS")
    print(f"Scenarios to run: {', '.join(map(str, scenarios))}")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔄 Progress: {i}/{len(scenarios)}")
        results[scenario] = run_scenario(scenario)
        
        # Brief pause between scenarios
        if i < len(scenarios):
            time.sleep(1)
    
    return results


def print_final_summary(results: Dict[int, bool]):
    """Print the final execution summary."""
    print_header("EXECUTION SUMMARY")
    
    successful = [s for s, success in results.items() if success]
    failed = [s for s, success in results.items() if not success]
    
    print(f"📊 Total scenarios processed: {len(results)}")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n✅ Successfully completed scenarios:")
        for scenario in successful:
            desc = QuestionGenerationConfig.get_scenario_description(scenario)
            count = QuestionGenerationConfig.get_question_count(scenario)
            print(f"  Scenario {scenario}: {desc} ({count} questions)")
    
    if failed:
        print(f"\n❌ Failed scenarios:")
        for scenario in failed:
            desc = QuestionGenerationConfig.get_scenario_description(scenario)
            print(f"  Scenario {scenario}: {desc}")
    
    # Overall status
    if len(successful) == len(results):
        print(f"\n🎉 ALL SCENARIOS COMPLETED SUCCESSFULLY!")
    elif successful:
        print(f"\n⚠️ PARTIAL SUCCESS: {len(successful)}/{len(results)} scenarios completed")
    else:
        print(f"\n💥 ALL SCENARIOS FAILED!")
    
    print(f"\n📁 Generated questions saved to: {QuestionGenerationConfig.OUTPUT_DIR}")


def parse_scenario_list(scenario_str: str) -> List[int]:
    """Parse comma-separated scenario numbers."""
    try:
        scenarios = []
        for s in scenario_str.split(','):
            scenario = int(s.strip())
            if scenario not in QuestionGenerationConfig.SCENARIO_SCRIPTS:
                raise ValueError(f"Invalid scenario number: {scenario}")
            scenarios.append(scenario)
        return sorted(list(set(scenarios)))  # Remove duplicates and sort
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid scenario specification: {e}")


# =====================================
# COMMAND LINE INTERFACE
# =====================================

def main():
    """Main entry point with command line interface."""
    parser = argparse.ArgumentParser(
        description="Question Generation Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python config.py                    # Run all scenarios
  python config.py --scenario 1      # Run scenario 1 only
  python config.py --scenario 1,3,5  # Run scenarios 1, 3, and 5
  python config.py --config          # Show configuration only
  python config.py --validate        # Validate environment only
        """
    )
    
    parser.add_argument(
        '--scenario', '-s',
        type=parse_scenario_list,
        help='Scenario number(s) to run (1-5). Comma-separated for multiple. Default: all scenarios'
    )
    
    parser.add_argument(
        '--config', '-c',
        action='store_true',
        help='Show configuration summary and exit'
    )
    
    parser.add_argument(
        '--validate', '-v',
        action='store_true',
        help='Validate environment and exit'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default=QuestionGenerationConfig.OUTPUT_DIR,
        help=f'Output directory for generated questions. Default: {QuestionGenerationConfig.OUTPUT_DIR}'
    )
    
    parser.add_argument(
        '--base-path', '-b',
        default=QuestionGenerationConfig.BASE_DATA_PATH,
        help='Base path to the task data folder'
    )
    
    parser.add_argument(
        '--questions', '-q',
        type=int,
        help='Override number of questions for all scenarios'
    )
    
    parser.add_argument(
        '--direct', '-d',
        action='store_true',
        help='Use direct function import (faster)'
    )
    
    parser.add_argument(
        '--subprocess', '-p',
        action='store_true',
        help='Use subprocess execution (safer)'
    )
    
    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='Skip environment validation before running'
    )
    
    args = parser.parse_args()
    
    # Update configuration based on command line arguments
    if args.output_dir:
        QuestionGenerationConfig.OUTPUT_DIR = args.output_dir
    
    if args.base_path:
        QuestionGenerationConfig.BASE_DATA_PATH = args.base_path
    
    if args.questions:
        # Override all question counts
        for scenario in QuestionGenerationConfig.QUESTION_COUNTS:
            QuestionGenerationConfig.QUESTION_COUNTS[scenario] = args.questions
    
    if args.direct:
        QuestionGenerationConfig.USE_DIRECT_IMPORT = True
    elif args.subprocess:
        QuestionGenerationConfig.USE_DIRECT_IMPORT = False
    
    # Show configuration if requested
    if args.config:
        print_config_summary()
        return
    
    # Validate environment if requested
    if args.validate:
        validate_environment()
        return
    
    # Default to all scenarios if none specified
    scenarios_to_run = args.scenario if args.scenario else list(QuestionGenerationConfig.SCENARIO_SCRIPTS.keys())
    
    print_header("QUESTION GENERATION MANAGER")
    print("🤖 Automated Question Generation for Multiple Scenarios")
    
    # Validate environment unless explicitly skipped
    if not args.no_validate:
        if not validate_environment():
            print("\n❌ Environment validation failed. Use --no-validate to skip.")
            sys.exit(1)
    
    # Show configuration
    print_config_summary()
    
    # Confirm before running (unless single scenario)
    if len(scenarios_to_run) > 1:
        print(f"\n🎯 About to run {len(scenarios_to_run)} scenarios: {', '.join(map(str, scenarios_to_run))}")
        response = input("Continue? [Y/n]: ").strip().lower()
        if response and response not in ['y', 'yes']:
            print("❌ Cancelled by user.")
            return
    
    # Run scenarios
    start_time = time.time()
    results = run_multiple_scenarios(scenarios_to_run)
    total_time = time.time() - start_time
    
    # Print final summary
    print_final_summary(results)
    print(f"⏱️ Total execution time: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
