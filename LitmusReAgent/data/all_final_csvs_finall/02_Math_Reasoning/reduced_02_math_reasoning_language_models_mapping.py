"""
Language to Models Mapping for 02_math_reasoning (Reduced Dataset)
Generated from reduced CSV data
Total languages: 27
Total unique models: 91
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Arabic": ['ChatGPT-3.5-turbo', 'ChatGPT-4', 'ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-Pro', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-mini'],
    "Assamese": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Bengali": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Openhathi', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'XLM-RoBERTa'],
    "Chinese": ['AceMath-RL-7B', 'ChatGPT-4o-latest', 'Claude-3.7-Sonnet-thinking', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'Claude-4-Opus-20250514', 'Claude-4-Opus-20250514-thinking', 'Claude-4-Sonnet-20250514', 'DeepScaleR-Preview-1.5B', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-1.5B', 'DeepSeek-R1-Distill-7B', 'DeepSeek-R1-Distill-14B', 'DeepSeek-R1-Distill-32B', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-0528', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GLM-Z1-Air-32B', 'GPT-4.1', 'GPT-4.5-preview', 'GPT-4o', 'Gemini-2.5-Pro-Experimental-0325', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-Pro-Preview-06-05', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Light-R1-DS-7B', 'Light-R1-DS-14B', 'Light-R1-DS-32B', 'Llama-3.3-70B-Instruct', 'Llama-4-Maverick', 'OpenAI-o3-mini-high', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'OpenMath-Nemotron-1.5B', 'OpenMath-Nemotron-7B', 'OpenMath-Nemotron-14B', 'OpenMath-Nemotron-32B', 'OpenThinker2-7B', 'OpenThinker2-32B', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'Qwen3-0.6B-Think', 'Qwen3-4B-Think', 'Qwen3-30B-A3B-Think', 'Qwen3-235B-A22B-Think', 'STILL-3-Preview-1.5B', 'Skywork-OR1-Math-7B', 'Skywork-OR1-Preview-7B', 'Skywork-OR1-Preview-32B', 'o3-2025-04-16-high', 'o3-2025-04-16-medium', 'o3-mini', 'o3-pro', 'o4-mini-high'],
    "English": ['AceMath-RL-7B', 'ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepScaleR-Preview-1.5B', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-1.5B', 'DeepSeek-R1-Distill-7B', 'DeepSeek-R1-Distill-14B', 'DeepSeek-R1-Distill-32B', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GLM-Z1-Air-32B', 'GPT-4', 'GPT-4.5-preview', 'Gemini-2.5-Pro-Experimental-0325', 'Gemini-Pro', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'LLaMA-2-7B', 'LLeMMa-7B', 'Light-R1-DS-7B', 'Light-R1-DS-14B', 'Light-R1-DS-32B', 'Llama-3.3-70B-Instruct', 'MAmmoTH-7B', 'Mistral-7B', 'OpenAI-o3-mini-high', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'OpenHathi-7B', 'OpenMath-Nemotron-1.5B', 'OpenMath-Nemotron-7B', 'OpenMath-Nemotron-14B', 'OpenMath-Nemotron-32B', 'OpenThinker2-7B', 'OpenThinker2-32B', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'Qwen3-0.6B-Think', 'Qwen3-4B-Think', 'Qwen3-30B-A3B-Think', 'Qwen3-235B-A22B-Think', 'STILL-3-Preview-1.5B', 'Skywork-OR1-Math-7B', 'Skywork-OR1-Preview-7B', 'Skywork-OR1-Preview-32B', 'WizardMath-7B', 'o3-mini'],
    "German": ['ChatGPT-4o-latest', 'Claude-3.7-Sonnet-thinking', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'Claude-4-Opus-20250514', 'Claude-4-Opus-20250514-thinking', 'Claude-4-Sonnet-20250514', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-0528', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.1', 'GPT-4.5-preview', 'GPT-4o', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-Pro-Preview-06-05', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'Llama-4-Maverick', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-2025-04-16-high', 'o3-2025-04-16-medium', 'o3-mini', 'o3-pro', 'o4-mini-high'],
    "Gujarati": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Hindi": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'GPT-4', 'Gemini-Pro', 'Gemma', 'Gemma-Instruct', 'LLaMA-2-7B', 'LLeMMa-7B', 'Llama-3', 'Llama-3-Instruct', 'MAmmoTH-7B', 'Mistral-7B', 'OpenHathi-7B', 'Openhathi', 'WizardMath-7B', 'XLM-RoBERTa'],
    "Indonesian": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B'],
    "Italian": ['ANITA-8B-DPO', 'Camoscio-2-70B-instruct', 'ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'LLamantino-2-70B-chat', 'Llama-2-70B-chat', 'Llama-3-8B-instruct', 'Llama-3-70B-instruct', 'Llama-3.1-70B-instruct', 'Llama-3.1-405B-instruct', 'Llama-3.3-70B-Instruct', 'Minerva-3B', 'Mistral-7B-instruct', 'Mixtral-8x7B-instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B'],
    "Japanese": ['ChatGPT-4o-latest', 'Claude-3.7-Sonnet-thinking', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'Claude-4-Opus-20250514', 'Claude-4-Opus-20250514-thinking', 'Claude-4-Sonnet-20250514', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-0528', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.1', 'GPT-4.5-preview', 'GPT-4o', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-Pro-Preview-06-05', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'Llama-4-Maverick', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-2025-04-16-high', 'o3-2025-04-16-medium', 'o3-mini', 'o3-pro', 'o4-mini-high'],
    "Kannada": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Korean": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-mini'],
    "Malay": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B'],
    "Malayalam": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Marathi": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Odia": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Portuguese": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-mini'],
    "Punjabi": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Russian": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'GPT-4o', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'GigaChat-A3B', 'GigaChat2-Pro', 'GigaChat2-MAX', 'Llama', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Qwen', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B'],
    "Swahili": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B'],
    "Tamil": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Openhathi', 'XLM-RoBERTa'],
    "Telugu": ['Airavata', 'Aya-8-Instruct', 'Bloom', 'Bloomz', 'ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma', 'Gemma-Instruct', 'Llama-3', 'Llama-3-Instruct', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'Openhathi', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'XLM-RoBERTa'],
    "Thai": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-mini'],
    "Vietnamese": ['ChatGPT-4o-latest', 'Claude-3.7-sonnet', 'Claude-3.7-sonnet-thinking', 'DeepSeek-R1', 'DeepSeek-R1-Distill', 'DeepSeek-R1-Distill-Llama-8B', 'DeepSeek-R1-Distill-Qwen-1.5B', 'DeepSeek-R1-Distill-Qwen-14B', 'DeepSeek-R1-Distill-Qwen-32B', 'DeepSeek-R1-Distill-Qwen-7B', 'DeepSeek-R1-671B', 'DeepSeek-V3', 'GPT-4.5-preview', 'Gemini-2.0-flash-thinking', 'Gemini-2.5-pro', 'Gemma3-27B-IT', 'Llama-3.3-70B-Instruct', 'OpenAI-o1-mini', 'OpenAI-o3-mini-medium', 'QwQ-32B', 'Qwen-2.5-72B-Instruct', 'Qwen-2.5-Math-72B-Instruct', 'Qwen-2.5-Max', 'Qwen-3-235B-A22B-Thinking', 'Qwen-QwQ-32B', 'Qwen2.5-32B-Instruct', 'o3-mini'],
}

# Statistics
TOTAL_LANGUAGES = len(LANGUAGE_MODELS_MAPPING)
TOTAL_UNIQUE_MODELS = len(set(model for models in LANGUAGE_MODELS_MAPPING.values() for model in models))

def get_models_for_language(language):
    """Get all models benchmarked for a specific language."""
    return LANGUAGE_MODELS_MAPPING.get(language, [])

def get_languages_for_model(model):
    """Get all languages that a specific model has been benchmarked on."""
    return [lang for lang, models in LANGUAGE_MODELS_MAPPING.items() if model in models]

def get_all_languages():
    """Get all available languages."""
    return list(LANGUAGE_MODELS_MAPPING.keys())

def get_all_models():
    """Get all unique models."""
    all_models = set()
    for models in LANGUAGE_MODELS_MAPPING.values():
        all_models.update(models)
    return sorted(list(all_models))

def get_language_statistics():
    """Get detailed statistics about language coverage."""
    stats = {}
    for language, models in LANGUAGE_MODELS_MAPPING.items():
        stats[language] = {
            'model_count': len(models),
            'models': sorted(models)
        }
    return stats

def get_model_statistics():
    """Get detailed statistics about model coverage."""
    model_counter = Counter()
    for models in LANGUAGE_MODELS_MAPPING.values():
        for model in models:
            model_counter[model] += 1
    
    return dict(model_counter.most_common())

def print_summary():
    """Print a summary of the mapping."""
    print(f"Task: 02_math_reasoning (Reduced Dataset)")
    print(f"Total Languages: {TOTAL_LANGUAGES}")
    print(f"Total Unique Models: {TOTAL_UNIQUE_MODELS}")
    print("\nTop 10 languages by model count:")
    
    lang_stats = get_language_statistics()
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1]['model_count'], reverse=True)
    
    for i, (lang, stats) in enumerate(sorted_langs[:10]):
        print(f"  {i+1}. {lang}: {stats['model_count']} models")
    
    print("\nTop 10 models by language coverage:")
    model_stats = get_model_statistics()
    
    for i, (model, count) in enumerate(list(model_stats.items())[:10]):
        print(f"  {i+1}. {model}: {count} languages")

# Scenario Analysis Functions
def analyze_scenarios():
    """Analyze which interdependent scenarios are enabled by this reduced dataset."""
    scenarios = {
        'S1_direct': [],
        'S2_same_lang_diff_model': [],
        'S3_similar_lang_same_model': [],
        'S4_distant_lang_same_model': [],
        'S5_diff_lang_diff_model': []
    }
    
    # S1: Direct scenarios (languages with models)
    for lang, models in LANGUAGE_MODELS_MAPPING.items():
        if models:
            scenarios['S1_direct'].append((lang, models))
    
    # S2: Same language, different models
    for lang, models in LANGUAGE_MODELS_MAPPING.items():
        if len(models) > 1:
            scenarios['S2_same_lang_diff_model'].append((lang, models))
    
    # S3 & S4: Require domain knowledge for language similarity/distance
    # These would need additional language family data
    
    return scenarios

def get_scenario_summary():
    """Get a summary of enabled scenarios."""
    scenarios = analyze_scenarios()
    
    summary = {
        'S1_direct_count': len(scenarios['S1_direct']),
        'S2_same_lang_diff_model_count': len(scenarios['S2_same_lang_diff_model']),
        'total_language_model_pairs': sum(len(models) for models in LANGUAGE_MODELS_MAPPING.values())
    }
    
    return summary

if __name__ == "__main__":
    print_summary()
    print("\n" + "="*50)
    print("SCENARIO ANALYSIS")
    print("="*50)
    scenarios = analyze_scenarios()
    print(f"S1 (Direct): {len(scenarios['S1_direct'])} languages with models")
    print(f"S2 (Same lang, diff model): {len(scenarios['S2_same_lang_diff_model'])} languages with multiple models")
    
    scenario_summary = get_scenario_summary()
    print(f"\nTotal language-model pairs: {scenario_summary['total_language_model_pairs']}")
