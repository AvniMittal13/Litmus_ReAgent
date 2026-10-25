"""
Language to Models Mapping for 05_Text_Summarization
Generated from combined CSV data
Total languages: 57
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Amharic": ['mBART', 'mT5', 'multilingual transformer models'],
    "Arabic": ['DC+Synth', 'GPT-3.5', 'GPT-4', 'Gemma2', 'Lead-3', 'Llama3', 'Mixtral', 'Qwen-1.5', 'Summarize-then-Translate', 'Summarize→Translate', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'lead-3', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Azerbaijani": ['mBART', 'mT5', 'multilingual transformer models'],
    "Basque": ['Aya-Expanse-8B', 'DeepSeek models', 'EuroLLM-9B', 'EuroLLM?1.7B?IT', 'EuroLLM?9B', 'FLOR series', 'Gemma-2-9B', 'Latxa-7B-v1.2', 'Meta-Llama-3.1-8B', 'Meta?Llama?3.1?8B', 'Meta?Llama?3.1?8B?IT', 'Mistral-7B', 'Qwen2.5 series', 'Qwen2.5-14B-IT-GPTQ-Int8', 'Qwen2.5-32B-IT-GPTQ-Int4', 'Qwen2.5?1.5B', 'Qwen2.5?1.5B?IT', 'Qwen2.5?7B', 'RigoChat-7B-v2', 'Salamandra-7B', 'SmolLM2-1.7B', 'aya?expanse?8b', 'gemma?2?2b', 'gemma?2?2b?it', 'gemma?2?9b', 'gemma?2?9b?it', 'leniachat?qwen2?1.5B?v0', 'salamandra?2b', 'salamandra?2b?instruct', 'salamandra?7b', 'salamandra?7b?instruct'],
    "Bengali": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Burmese": ['mBART', 'mT5', 'multilingual transformer models'],
    "Catalan": ['Aya-Expanse-8B', 'DeepSeek models', 'EuroLLM-9B', 'EuroLLM?1.7B?IT', 'EuroLLM?9B', 'FLOR series', 'Gemma-2-9B', 'Latxa-7B-v1.2', 'Meta-Llama-3.1-8B', 'Meta?Llama?3.1?8B', 'Meta?Llama?3.1?8B?IT', 'Mistral-7B', 'Qwen2.5 series', 'Qwen2.5-14B-IT-GPTQ-Int8', 'Qwen2.5-32B-IT-GPTQ-Int4', 'Qwen2.5?1.5B', 'Qwen2.5?1.5B?IT', 'Qwen2.5?7B', 'RigoChat-7B-v2', 'Salamandra-7B', 'SmolLM2-1.7B', 'aya?expanse?8b', 'gemma?2?2b', 'gemma?2?2b?it', 'gemma?2?9b', 'gemma?2?9b?it', 'leniachat?qwen2?1.5B?v0', 'salamandra?2b', 'salamandra?2b?instruct', 'salamandra?7b', 'salamandra?7b?instruct'],
    "Catalna": ['Aya-Expanse-8B', 'DeepSeek models', 'EuroLLM-9B', 'EuroLLM?1.7B?IT', 'EuroLLM?9B', 'FLOR series', 'Gemma-2-9B', 'Latxa-7B-v1.2', 'Meta-Llama-3.1-8B', 'Meta?Llama?3.1?8B', 'Meta?Llama?3.1?8B?IT', 'Mistral-7B', 'Qwen2.5 series', 'Qwen2.5-14B-IT-GPTQ-Int8', 'Qwen2.5-32B-IT-GPTQ-Int4', 'Qwen2.5?1.5B', 'Qwen2.5?1.5B?IT', 'Qwen2.5?7B', 'RigoChat-7B-v2', 'Salamandra-7B', 'SmolLM2-1.7B', 'aya?expanse?8b', 'gemma?2?2b', 'gemma?2?2b?it', 'gemma?2?9b', 'gemma?2?9b?it', 'leniachat?qwen2?1.5B?v0', 'salamandra?2b', 'salamandra?2b?instruct', 'salamandra?7b', 'salamandra?7b?instruct'],
    "Chinese": ['Claude-3.5-Sonnet', 'DC+Synth', 'DeepSeek-R1', 'DeepSeek-v3', 'GPT-4o', 'Jirai-Qwen', 'Lead-3', 'Llama-3.1-8B', 'Qwen-14B', 'Qwen2.5-7B', 'RNN encoder-decoder', 'Recurrent Neural Networks', 'Summarize-then-Translate', 'Summarize→Translate', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'lead-3', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mT5', 'multilingual transformer models'],
    "Czech": ['mBART', 'mT5'],
    "Dutch": ['mBART', 'mT5'],
    "English": ['Anthropic-LM v4-s3', 'Centroid+mT5', 'Cohere xlarge v20220609', 'DC+Synth', 'DeepSeek-V2', 'GLM', 'GPT-3 ada v1', 'GPT-3 curie v1', 'GPT-3 davinci v1', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemma-1', 'Gemma2', 'Graph-ExtractGenerate', 'InstructGPT ada v1', 'InstructGPT curie v1', 'InstructGPT davinci v2', 'InternLM', 'Lead-3', 'Llama-3', 'Llama-3.1', 'Llama3', 'M-BERT', 'Mistral-v0.3', 'Mixtral', 'OPT 175B', 'Oracle', 'Phi-3', 'Pointer-Generator', 'Qwen-1.5', 'Random', 'Summarize-then-Translate', 'Summarize→Translate', 'TextRank', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'Yi-1.5', 'lead-3', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mBERT', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models', 'standard transformer'],
    "French": ['Centroid+mT5', 'Dolphin-2.6-Mistral-7B', 'Dolphin-2.6-Phi-2', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Graph-ExtractGenerate', 'LLaMA-2', 'Llama-2-7B-Chat', 'Llama-3.1', 'M-BERT', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-OpenOrca', 'Oracle', 'Phi-2', 'Pointer-Generator', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5', 'multilingual transformer models'],
    "Galician": ['Aya-Expanse-8B', 'DeepSeek models', 'EuroLLM-9B', 'EuroLLM?1.7B?IT', 'EuroLLM?9B', 'FLOR series', 'Gemma-2-9B', 'Latxa-7B-v1.2', 'Meta-Llama-3.1-8B', 'Meta?Llama?3.1?8B', 'Meta?Llama?3.1?8B?IT', 'Mistral-7B', 'Qwen2.5 series', 'Qwen2.5-14B-IT-GPTQ-Int8', 'Qwen2.5-32B-IT-GPTQ-Int4', 'Qwen2.5?1.5B', 'Qwen2.5?1.5B?IT', 'Qwen2.5?7B', 'RigoChat-7B-v2', 'Salamandra-7B', 'SmolLM2-1.7B', 'aya?expanse?8b', 'gemma?2?2b', 'gemma?2?2b?it', 'gemma?2?9b', 'gemma?2?9b?it', 'leniachat?qwen2?1.5B?v0', 'salamandra?2b', 'salamandra?2b?instruct', 'salamandra?7b', 'salamandra?7b?instruct'],
    "German": ['Centroid+mT5', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Graph-ExtractGenerate', 'Llama-3.1', 'M-BERT', 'Oracle', 'Pointer-Generator', 'Qwen 2.5-7B', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5'],
    "Gujarati": ['mBART', 'mT5', 'multilingual transformer models'],
    "Gujurati": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART-50', 'mT5-base', 'mT5-small'],
    "Hausa": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Hindi": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Igbo": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Indonesian": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Italian": ['mBART', 'mT5'],
    "Japanese": ['ChatGPT', 'DeepSeek-v3', 'Flan-T5', 'GPT-3', 'Jirai-Qwen', 'Llama-3.1-8B', 'NICT BERT base', 'Qwen2.5-7B', 'T5', 'Tohoku BERT base', 'Tohoku BERT large', 'Waseda RoBERTa large', 'XLM RoBERTa base', 'XLM RoBERTa large', 'mBART', 'mT5', 'multilingual transformer models'],
    "Kirundi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Korean": ['mBART', 'mT5', 'multilingual transformer models'],
    "Kyrgyz": ['mBART', 'mT5', 'multilingual transformer models'],
    "Marathi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Nepali": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Oromo": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Pashto": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Persian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Pidgin": ['mBART', 'mT5', 'multilingual transformer models'],
    "Portuguese": ['BLOOM', 'ChatGPT', 'Command-r-08-2024', 'DeepSeek', 'DeepSeek-V3', 'Enhancing-PT-SS', 'GPT-3', 'GPT-4', 'GPT-4o', 'GPT-4o mini', 'GPT3.5-Turbo', 'GPT4o-mini', 'MUSS-Unsupervised', 'Mistral', 'Mixtral', 'Qwen', 'Sabia-2-small', 'Sabia-3', 'Sabiá-3.1', 'aya-23-8b', 'deepseek-r1-distill-qwen-32b', 'deepseek-r1-distill-qwen-7b', 'gemma2-27b-it', 'llama-3.1-8b-instruct', 'mBART', 'mT5', 'mistral-7b-instruct-v0.3', 'multilingual transformer models', 'o1-mini', 'qwen2-72b-instruct', 'qwen2-7b-instruct', 'qwen2.5-14b-instruct', 'qwen2.5-32b-instruct', 'qwen2.5-7b-instruct', 'qwen2.5?7b-instruct'],
    "Punjabi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Russian": ['BLOOM', 'DC+Synth', 'DeepSeek', 'GPT-3', 'GPT-4', 'Gigachat', 'Lead-3', 'M-BERT', 'Mistral', 'Mixtral', 'Oracle', 'Pointer-Generator', 'Qwen', 'Random', 'Summarize-then-Translate', 'Summarize→Translate', 'TextRank', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'YandexGPT', 'lead-3', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mBERT', 'mT5', 'multilingual transformer models'],
    "Scottish Gaelic": ['mBART', 'mT5', 'multilingual transformer models'],
    "Serbian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Sinhala": ['mBART', 'mT5', 'multilingual transformer models'],
    "Somali": ['mBART', 'mT5', 'multilingual transformer models'],
    "Spanish": ['Aya-Expanse-8B', 'Centroid+mT5', 'DC+Synth', 'DeepSeek models', 'EuroLLM-9B', 'EuroLLM?1.7B?IT', 'EuroLLM?9B', 'FLOR series', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Gemma-2-9B', 'Graph-ExtractGenerate', 'Latxa-7B-v1.2', 'Lead-3', 'Llama-3.1', 'M-BERT', 'Meta-Llama-3.1-8B', 'Meta?Llama?3.1?8B', 'Meta?Llama?3.1?8B?IT', 'Mistral-7B', 'Oracle', 'Pointer-Generator', 'Qwen2.5 series', 'Qwen2.5-14B-IT-GPTQ-Int8', 'Qwen2.5-32B-IT-GPTQ-Int4', 'Qwen2.5?1.5B', 'Qwen2.5?1.5B?IT', 'Qwen2.5?7B', 'Random', 'RigoChat-7B-v2', 'Salamandra-7B', 'SmolLM2-1.7B', 'Summarize-then-Translate', 'Summarize→Translate', 'TextRank', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'aya?expanse?8b', 'gemma?2?2b', 'gemma?2?2b?it', 'gemma?2?9b', 'gemma?2?9b?it', 'lead-3', 'leniachat?qwen2?1.5B?v0', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mBERT', 'mT5', 'multilingual transformer models', 'salamandra?2b', 'salamandra?2b?instruct', 'salamandra?7b', 'salamandra?7b?instruct'],
    "Swahili": ['AfriBERTa', 'GPT-3.5', 'GPT-4', 'Gemma2', 'LLaMA3.1', 'Llama3', 'Mixtral', 'Qwen-1.5', 'Qwen2.5-7B/72B', 'XLM-R', 'mBART', 'mBART-50', 'mBERT', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Tamil": ['mBART', 'mT5', 'multilingual transformer models'],
    "Telugu": ['mBART', 'mT5', 'multilingual transformer models'],
    "Thai": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Tigrinya": ['mBART', 'mT5', 'multilingual transformer models'],
    "Turkish": ['DC+Synth', 'Lead-3', 'M-BERT', 'Oracle', 'Pointer-Generator', 'Random', 'Summarize-then-Translate', 'Summarize→Translate', 'TextRank', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'lead-3', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mBERT', 'mT5', 'multilingual transformer models'],
    "Ukrainian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Ukranian": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART-50', 'mT5-base', 'mT5-small'],
    "Urdu": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Uzbek": ['mBART', 'mT5', 'multilingual transformer models'],
    "Vietnamese": ['DC+Synth', 'GPT-3.5', 'GPT-4', 'Gemma2', 'Lead-3', 'Llama3', 'Mixtral', 'Qwen-1.5', 'Summarize-then-Translate', 'Summarize→Translate', 'Trans-Sum-G', 'Trans-Sum-R', 'Translate-then-Summarize', 'Translate→Summarize', 'lead-3', 'mBART', 'mBART cross-lingual fine-tuning', 'mBART monolingual fine-tuning', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Welsh": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "Yoruba": ['GPT-3.5', 'GPT-4', 'Gemma2', 'Llama3', 'Mixtral', 'Qwen-1.5', 'mBART', 'mBART-50', 'mT5', 'mT5-base', 'mT5-small', 'multilingual transformer models'],
    "arabic": ['standard transformer'],
    "french": ['standard transformer'],
    "german": ['standard transformer'],
    "spanish": ['standard transformer'],
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
        if isinstance(models, list):
            all_models.update(models)
        else:
            all_models.add(models)
    return sorted(list(all_models))


def get_language_statistics():
    """Get detailed statistics about language coverage."""
    stats = {}
    for language, models in LANGUAGE_MODELS_MAPPING.items():
        if isinstance(models, list):
            model_list = models
        else:
            model_list = [models] if models else []
        
        stats[language] = {
            'model_count': len(model_list),
            'models': sorted(model_list)
        }
    return stats


def get_model_statistics():
    """Get detailed statistics about model coverage."""
    model_counter = Counter()
    for models in LANGUAGE_MODELS_MAPPING.values():
        if isinstance(models, list):
            for model in models:
                model_counter[model] += 1
        else:
            model_counter[models] += 1
    
    return dict(model_counter.most_common())


def print_summary():
    """Print a summary of the mapping."""
    print(f"Task: 05_Text_Summarization")
    print(f"Total Languages: {TOTAL_LANGUAGES}")
    print(f"Total Unique Models: {TOTAL_UNIQUE_MODELS}")
    print("\nTop 10 languages by model count:")
    
    lang_stats = get_language_statistics()
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1]['model_count'], reverse=True)
