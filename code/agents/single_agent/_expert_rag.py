"""
Expert knowledge RAG tool – standalone function wrapping the same RAG pipeline
used by Expert_Knowledge_Agent, but callable as a plain function for the
single-agent baseline.
"""

import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

from utils.aoai_chat import model_config
from utils.azure_embedding import openai_embedding_function, embedding_client as _embedding_client
from agents.custom_agents.expert_knowledge import (
    _get_query_embedding,
    _search_expert_knowledge_cache,
    _save_expert_knowledge_cache,
)

# We build the RAG components lazily so the module can be imported without
# side-effects (Chroma collection creation, etc.).
_rag_initialized = False
_rag_assistant = None
_rag_proxy = None


def _init_rag():
    """Initialise AutoGen RAG agents once."""
    global _rag_initialized, _rag_assistant, _rag_proxy
    if _rag_initialized:
        return

    from autogen import AssistantAgent
    from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

    _rag_assistant = AssistantAgent(
        name="assistant",
        system_message=(
            "You are the Expert Knowledge Agent, acting as a senior multilingual NLP "
            "researcher guiding another researcher through complex performance prediction "
            "or multilingual modeling challenges.\n\n"
            "You have access to a corpus of expert research practices, experimental "
            "strategies, and multilingual NLP analysis guides via a RAG system. Based on "
            "retrieved passages from that knowledge base, your job is to translate the "
            "content into clear, actionable next steps.\n\n"
            "### Your task:\n"
            "- Extract expert insights from the retrieved content and explain exactly how "
            "to proceed in the current research scenario.\n"
            "- Provide step-by-step, structured guidance covering: what data to gather, "
            "what features to compute, how to structure the data, what modeling strategies "
            "are appropriate, how to analyze and interpret the results.\n"
            "- Where relevant, highlight trade-offs, risks, and fallback options.\n"
            "- DO NOT give code in your response.\n"
            "- Give instructions for reiterations.\n"
        ),
        llm_config=model_config,
    )

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    _rag_proxy = RetrieveUserProxyAgent(
        name="ragproxyagent",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        retrieve_config={
            "task": "default",
            "docs_path": [
                os.path.join(base_dir, "knowledge", "knowledge_2.md"),
            ],
            "custom_text_types": ["mdx"],
            "chunk_token_size": 1000,
            "vector_db": "chroma",
            "collection_name": "expert_knowledge_new2",
            "model": model_config["config_list"][0]["model"],
            "client": chromadb.PersistentClient(
                path=os.path.join(base_dir, "tmp", "db")
            ),
            "embedding_function": openai_embedding_function,
            "embedding_model": "text-embedding-ada-002",
            "override": True,
            "get_or_create": True,
        },
        code_execution_config=False,
    )

    _rag_initialized = True


def expert_knowledge_query(query: str) -> str:
    """
    Query the expert-knowledge RAG system.
    Returns methodology guidance as a plain string.
    """
    # 1. Check cache
    query_embedding = _get_query_embedding(query)
    cached = _search_expert_knowledge_cache(query_embedding, threshold=0.90)
    if cached:
        print("[ExpertRAG] Cache hit")
        return cached

    # 2. Run RAG
    _init_rag()
    _rag_proxy.initiate_chat(
        _rag_assistant,
        message=_rag_proxy.message_generator,
        problem=query,
    )
    response = _rag_proxy._oai_messages[_rag_assistant][-1]["content"]

    # 3. Save to cache
    if query_embedding is not None:
        _save_expert_knowledge_cache(query, query_embedding, response)

    return response
