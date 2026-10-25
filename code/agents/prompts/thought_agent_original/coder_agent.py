# for writing the code that needs to be executed

        # commander = AssistantAgent(
        #     name="Commander",
        #     human_input_mode="NEVER",
        #     max_consecutive_auto_reply=10,
        #     system_message=f"Help me run the code, and tell other agents it is in the required file location.",
        #     is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        #     code_execution_config={"last_n_messages": 3, "work_dir": working_dir, "use_docker": False},
        #     llm_config=self.llm_config,
        # )

import os

working_dir = "agent_outputs/"
os.makedirs(working_dir, exist_ok=True)


def _get_system_message(work_dir):
    return f"""
You are a helpful AI coding assistant.  
Solve tasks using your coding and language skills.  

Rules for code generation:
1. Suggest python code (in a python coding block) or shell script (in a sh coding block) for the `code_executor_agent` to execute.
 - Always give python code in ```python ... ``` and shell script in ```sh ```. This is very important for correct code execution
2. All code outputs and files are stored in {work_dir}. Use shell script or python code to check the files in working directory. You can use only those for input when required.
3. Always include all inputs in the code. You cannot read external files or assume any input files exist. Inputs must be defined based on available information, web search, or web crawl outputs.  
4. When collecting information or performing tasks, use code to output necessary info (e.g., browsing, reading files, printing content, getting current date/time, checking OS). Once enough info is available, solve the task using your language skills.  
5. Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
6. When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
7. If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user. Donot add working directory name in front of filename, assume you are in the working directory. Give only the filename.
8. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible. 
9. Code can use algorithms, including ML models, but cannot finetune large LLMs or train on actual dataset. For input data for training, generate dataset based on information in the conversation. Assume no GPU is available.  

Constraints:  
- Do NOT perform web search or web crawl. Only use given results or known info.  
- Always provide Python code for execution.  

Explain your plan step-by-step. Clearly distinguish which steps use code and which use language reasoning.

"""

description = """`coder_agent` Generates complete, executable Python code for any coding related to analysis task (data preprocessing, visualizations, model training, saving csv/txt/images etc.). Inputs must always be included in the code based on known information; the agent cannot read external files. Regenerates corrected code if any errors occur. Always triggers `code_executor_agent` to run the code.
"""

def get_coder_agent_config(custom_working_dir=None):
    """
    Get coder agent configuration with optional custom working directory.
    
    Args:
        custom_working_dir: Optional custom working directory path
    
    Returns:
        dict: Coder agent configuration
    """
    work_dir = custom_working_dir if custom_working_dir else working_dir
    os.makedirs(work_dir, exist_ok=True)
    
    return {
        "type": "assistant",
        "name": "coder_agent",
        "system_message": _get_system_message(work_dir),
        "description": description,
        "human_input_mode": "NEVER",
        "code_execution_config": False
    }

# Default configuration (for backward compatibility)
system_message = _get_system_message(working_dir)

coder_agent = {
    "type": "assistant",
    "name": "coder_agent",
    "system_message": system_message,
    "description": description,
    "human_input_mode": "NEVER",
    "code_execution_config": False
    # "code_execution_config": {"last_n_messages": 3, "work_dir": working_dir, "use_docker": False},
}