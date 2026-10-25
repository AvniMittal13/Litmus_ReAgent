"""
Azure OpenAI chat helpers shared by the agents and evaluation scripts.

NOTE: reconstructed for this release. The original module was not part of the
uploaded sources; this version provides the same interface the code relies on
(`model_config`, `client`, `get_gpt_output`, `get_chat_response`,
`get_structured_response`) and is configured entirely via environment variables
(see `.env.example`).

Authentication: if OPENAI_API_KEY is set it is used, otherwise Azure AD
(DefaultAzureCredential, e.g. `az login`) is used.
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-12-01-preview")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4.1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    _auth = {"api_key": OPENAI_API_KEY}
else:
    _auth = {
        "azure_ad_token_provider": get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
    }

# autogen llm_config
model_config = {
    "config_list": [
        {
            "model": OPENAI_DEPLOYMENT_NAME,
            "base_url": OPENAI_BASE_URL,
            "api_version": OPENAI_API_VERSION,
            "api_type": "azure",
            **_auth,
        }
    ],
    "cache_seed": None,
}

client = AzureOpenAI(
    azure_endpoint=OPENAI_BASE_URL,
    api_version=OPENAI_API_VERSION,
    **_auth,
)


def get_chat_response(messages, output_dir=None, model_name=None, **kwargs):
    """Return the assistant text for a list of chat messages."""
    response = client.chat.completions.create(
        model=model_name or OPENAI_DEPLOYMENT_NAME,
        messages=messages,
        **kwargs,
    )
    return response.choices[0].message.content


def get_gpt_output(system_message, user_message, model_name=None):
    """Single-turn completion with a system and a user message."""
    return get_chat_response(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        model_name=model_name,
    )


def get_structured_response(prompt, structuredClass, model_name=None):
    """Return a JSON string conforming to the given pydantic model."""
    response = client.beta.chat.completions.parse(
        model=model_name or OPENAI_DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format=structuredClass,
    )
    return response.choices[0].message.content
