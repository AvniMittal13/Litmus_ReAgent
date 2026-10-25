"""
Azure OpenAI embedding helpers (text-embedding-ada-002).

NOTE: reconstructed for this release. The original module was not part of the
uploaded sources; this version provides the same interface the code relies on
(`embedding_client`, `openai_embedding_function`, `_embedding_token_provider`).

The precomputed paper embeddings in data/all_final_csvs_finall were created with
text-embedding-ada-002, so query embeddings must use the same model.
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

AZURE_OPENAI_ENDPOINT_EMBEDDING = os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDING") or os.getenv("OPENAI_BASE_URL")
AZURE_OPENAI_API_KEY_EMBEDDING = os.getenv("AZURE_OPENAI_API_KEY_EMBEDDING")
EMBEDDING_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-12-01-preview")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

_embedding_token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

if AZURE_OPENAI_API_KEY_EMBEDDING:
    _auth = {"api_key": AZURE_OPENAI_API_KEY_EMBEDDING}
else:
    _auth = {"azure_ad_token_provider": _embedding_token_provider}

embedding_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT_EMBEDDING,
    api_version=EMBEDDING_API_VERSION,
    **_auth,
)


class AzureEmbeddingFunction:
    """Chroma-compatible embedding function backed by `embedding_client`."""

    def __call__(self, input):
        resp = embedding_client.embeddings.create(input=list(input), model=OPENAI_EMBEDDING_MODEL)
        return [d.embedding for d in resp.data]

    def name(self):
        return "azure_openai_embedding"


openai_embedding_function = AzureEmbeddingFunction()
