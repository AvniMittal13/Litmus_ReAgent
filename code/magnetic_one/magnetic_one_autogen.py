import asyncio
import asyncio
import os
from site import venv
from dotenv import load_dotenv

from autogen_ext.auth.azure import AzureTokenProvider
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from autogen_core.models import UserMessage
from azure.core.credentials import AzureKeyCredential
# from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

load_dotenv()


# Create the token provider
token_provider = AzureTokenProvider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default",
)

model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
    model=os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
    api_version=os.getenv("OPENAI_API_VERSION", "2025-01-01-preview"),
    azure_endpoint=os.getenv("OPENAI_BASE_URL", "https://YOUR_AZURE_OPENAI_ENDPOINT.openai.azure.com"),
    # azure_ad_token_provider=token_provider,  # Optional if you choose key-based authentication.
    api_key=os.getenv("OPENAI_API_KEY"), # For key-based authentication.
)

llm_config = {

    "config_list": [
        {
            "model": os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL"),
            "api_type": os.getenv("OPENAI_API_TYPE"),
            "api_version": os.getenv("OPENAI_API_VERSION")
        }
    ]
}


import asyncio
# from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console

from openai import AzureOpenAI
from autogen_ext.teams.magentic_one import MagenticOne
# from autogen_ext.code_executors import LocalCommandLineCodeExecutor
# from autogen.coding import LocalCommandLineCodeExecutor
from pathlib import Path
import venv

work_dir = Path("magnetic_one_coding")
work_dir.mkdir(exist_ok=True)

venv_dir = "./venv"
venv_builder = venv.EnvBuilder(with_pip=True)
# venv_builder.create(venv_dir)
venv_context = venv_builder.ensure_directories(venv_dir)

local_executor = LocalCommandLineCodeExecutor(work_dir=work_dir, virtual_env_context=venv_context)



async def example_usage():
    m1 = MagenticOne(
        client=model_client,
        code_executor=local_executor
    )
    task = "Use code generation and execution to train mini regressor model after collecting information from the web for the following question: What is the accuracy of llama in Santali for summarization task?"
    result = await Console(m1.run_stream(task=task))

    print("Final Result:")
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(example_usage())

