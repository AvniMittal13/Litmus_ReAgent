"""
Single LLM Agent baseline – one agent with iterative tool-calling.

Tools available:
  1. db_search_and_scrape  – search paper embeddings DB + scrape + GPT summarise
  2. expert_knowledge_query – RAG over expert knowledge corpus
  3. execute_python_code   – run arbitrary Python in a sandboxed working dir

The agent uses Azure OpenAI's native tool-calling API (no AutoGen orchestration).
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import time
import traceback
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Lazy imports for heavy dependencies (loaded once, at first use)
# ---------------------------------------------------------------------------
_tools_loaded = False
_db_search_fn = None
_expert_knowledge_fn = None


def _ensure_tools():
    """Import tool implementations once."""
    global _tools_loaded, _db_search_fn, _expert_knowledge_fn
    if _tools_loaded:
        return
    from agents.tools.db_search_and_scrape import db_search_and_scrape
    from agents.single_agent._expert_rag import expert_knowledge_query
    _db_search_fn = db_search_and_scrape
    _expert_knowledge_fn = expert_knowledge_query
    _tools_loaded = True


# ---------------------------------------------------------------------------
# Tool definitions (OpenAI function-calling schema)
# ---------------------------------------------------------------------------
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "db_search_and_scrape",
            "description": (
                "Search the research-paper embedding database for papers relevant "
                "to a natural-language query.  Returns a GPT-generated analysis of "
                "the most relevant papers found, including extracted data, tables, "
                "metrics, and citations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural-language search query about NLP benchmarks, models, languages, or tasks.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "expert_knowledge_query",
            "description": (
                "Query the expert-knowledge RAG system for PhD-level methodology "
                "guidance on multilingual NLP research, feature engineering, "
                "predictive modelling strategies, and best practices."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Research methodology question to ask the expert knowledge base.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": (
                "Execute a Python code snippet and return its stdout/stderr. "
                "Use this for data processing, feature engineering, ML model "
                "training, predictions, and any computational analysis. "
                "Available libraries: lang2vec, scikit-learn, xgboost, lightgbm, "
                "pandas, numpy, shap, transformers, wikipedia-api."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Complete Python code to execute. Must be self-contained.",
                    }
                },
                "required": ["code"],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# System prompt – merged from research_planner + coder guidance
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = textwrap.dedent("""\
You are a single expert research agent specializing in multilingual NLP performance prediction.
You have access to three tools that you must use iteratively to answer the user's question:

1. **db_search_and_scrape(query: str)** – Search a database of NLP research papers for benchmark results, model performance data, and related findings. Input is a natural-language search query about NLP benchmarks, models, languages, or tasks (e.g. "GPT-3.5 performance on Code Generation for low-resource languages"). Returns a GPT-generated analysis of the most relevant papers found, including extracted data, tables, metrics, and citations. Always run multiple diverse queries to gather comprehensive data.

2. **expert_knowledge_query(query: str)** – Get PhD-level methodology guidance from an expert knowledge base. Input is a research methodology question (e.g. "How should I predict NLP benchmark performance for an unseen language using linguistic features?"). Returns structured guidance on data collection, feature engineering, modelling strategies, and best practices.

3. **execute_python_code(code: str)** – Execute a Python code snippet and return its stdout/stderr. Input is a complete, self-contained Python script as a string. All code runs in a sandboxed working directory. Use this for data processing, computing linguistic features, training ML models, generating predictions, and any computational analysis.

### Your Workflow:
1. **Understand the question** – Parse what prediction or analysis is needed (task, model, language, metric).
2. **Consult expert knowledge** – Ask the expert system for guidance on approach and features.
3. **Search for data** – Use db_search_and_scrape with multiple diverse queries to find relevant benchmark data, proxy data, and linguistic information.
4. **Perform predictive analysis with code** – This is CRITICAL. You MUST execute code to:
   - Collect linguistic features using lang2vec (URIEL vectors, syntax, phonology, geography, family)
   - Build feature matrices for known data points
   - Train regression/ensemble models (XGBoost, LightGBM, RandomForest, etc.)
   - Generate predictions with error estimates
   - lang2vec returns '--' for missing values – always convert to np.nan
   - Use ISO 639-3 codes (3-letter): 'eng', 'deu', 'hin'
5. **Iterate** – If results are unsatisfactory, refine queries, collect more data, and re-run code.
6. **Provide final answer** – Structured response with predictions, confidence, methodology, and citations.

### Critical Rules:
- NEVER make predictions without executing code first.
- ALWAYS provide concrete numerical predictions based on code output.
- Use proxy data and predictive modelling when direct benchmarks are unavailable.
- Always suppress warnings in Python code.
- Always add `import sys; sys.stdout.reconfigure(encoding='utf-8', errors='replace')` at top of code.
- Include error handling (try-except) in all code.
- Available Python libraries: lang2vec, scikit-learn, xgboost, lightgbm, pandas, numpy, shap, transformers, wikipedia-api, matplotlib, seaborn.
- No GPU available – use CPU-only models.
- Do NOT finetune LLMs. You CAN train regression/classification/ensemble models.
""")


# ---------------------------------------------------------------------------
# Code executor helper
# ---------------------------------------------------------------------------
def _execute_python_code(code: str, working_dir: str, timeout: int = 120) -> str:
    """Run Python code in a subprocess, return combined stdout+stderr."""
    os.makedirs(working_dir, exist_ok=True)

    # Write code to a temp file inside working_dir
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    script_path = os.path.join(working_dir, f"script_{ts}.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=working_dir,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n[STDERR]\n" + result.stderr
        if not output.strip():
            output = "(no output)"
        # Truncate very long outputs
        if len(output) > 30000:
            output = output[:15000] + "\n\n... [TRUNCATED] ...\n\n" + output[-15000:]
        return output
    except subprocess.TimeoutExpired:
        return f"[ERROR] Code execution timed out after {timeout} seconds."
    except Exception as e:
        return f"[ERROR] Code execution failed: {e}"


# ---------------------------------------------------------------------------
# Tool dispatcher
# ---------------------------------------------------------------------------
def _dispatch_tool(name: str, arguments: dict, working_dir: str) -> str:
    """Execute a tool call and return the string result."""
    _ensure_tools()
    if name == "db_search_and_scrape":
        return _db_search_fn(arguments["query"])
    elif name == "expert_knowledge_query":
        return _expert_knowledge_fn(arguments["query"])
    elif name == "execute_python_code":
        return _execute_python_code(arguments["code"], working_dir)
    else:
        return f"Unknown tool: {name}"


# ---------------------------------------------------------------------------
# Main agent class
# ---------------------------------------------------------------------------
class SingleAgent:
    """
    Single LLM agent with iterative tool-calling loop.
    Uses Azure OpenAI chat completions API with native tool-calling.
    """

    def __init__(self, working_dir: str = "agent_outputs/single_agent"):
        self.working_dir = working_dir
        os.makedirs(working_dir, exist_ok=True)

        # Build the Azure OpenAI client (reuse the shared one from aoai_chat)
        from utils.aoai_chat import client as aoai_client
        self.client = aoai_client
        self.model = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4.1")

        # Conversation history
        self.messages = []
        # Tool call log for intermediates
        self.tool_log = []

    def run(self, user_query: str, max_iterations: int = 30) -> str:
        """
        Run the agent on a user query with iterative tool-calling.
        Returns the final text response.
        """
        # Build role-appropriate message format
        model_lower = self.model.lower()
        if model_lower in ("o4-mini", "gpt-4.1"):
            self.messages = [
                {"role": "developer", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
                {"role": "user", "content": [{"type": "text", "text": user_query}]},
            ]
        else:
            self.messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
            ]

        for iteration in range(max_iterations):
            print(f"\n[SingleAgent] Iteration {iteration + 1}/{max_iterations}")

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=TOOL_SCHEMAS,
                    tool_choice="auto",
                )
            except Exception as e:
                print(f"[SingleAgent] API error: {e}")
                # Retry once after a short delay
                time.sleep(5)
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        tools=TOOL_SCHEMAS,
                        tool_choice="auto",
                    )
                except Exception as e2:
                    return f"[ERROR] API call failed after retry: {e2}"

            choice = response.choices[0]
            message = choice.message

            # If no tool calls, we have the final answer
            if not message.tool_calls:
                final_text = message.content or ""
                print(f"[SingleAgent] Final response received ({len(final_text)} chars)")
                self.messages.append({"role": "assistant", "content": final_text})
                return final_text

            # Process tool calls
            # Append the assistant message (with tool_calls) to history
            self.messages.append(message.model_dump())

            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                try:
                    fn_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    fn_args = {"error": "Could not parse arguments"}

                print(f"[SingleAgent] Tool call: {fn_name}({list(fn_args.keys())})")

                start_time = time.time()
                tool_result = _dispatch_tool(fn_name, fn_args, self.working_dir)
                elapsed = time.time() - start_time

                # Log the tool invocation
                self.tool_log.append({
                    "iteration": iteration + 1,
                    "tool": fn_name,
                    "arguments": {k: v[:200] if isinstance(v, str) and len(v) > 200 else v for k, v in fn_args.items()},
                    "result_length": len(tool_result),
                    "elapsed_seconds": round(elapsed, 2),
                    "timestamp": datetime.now().isoformat(),
                })

                print(f"[SingleAgent] Tool result: {len(tool_result)} chars ({elapsed:.1f}s)")

                # Append tool result to conversation
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

        # Max iterations reached
        print(f"[SingleAgent] Max iterations ({max_iterations}) reached")
        return "[MAX_ITERATIONS] The agent reached the maximum number of tool-calling iterations without producing a final answer."

    def get_intermediates(self) -> dict:
        """Return tool invocation log and conversation for saving."""
        return {
            "tool_log": self.tool_log,
            "total_tool_calls": len(self.tool_log),
            "conversation_length": len(self.messages),
        }
