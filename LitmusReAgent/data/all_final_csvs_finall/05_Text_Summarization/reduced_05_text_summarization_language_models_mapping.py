"""
Language to Models Mapping for 05_text_summarization (Reduced Dataset)
Generated from reduced combined CSV data
Total languages: 48
Total unique models: 69
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Amharic": ['mBART', 'mT5', 'multilingual transformer models'],
    "Arabic": ['mBART', 'mT5', 'multilingual transformer models'],
    "Azerbaijani": ['mBART', 'mT5', 'multilingual transformer models'],
    "Bengali": ['mBART', 'mT5', 'multilingual transformer models'],
    "Burmese": ['mBART', 'mT5', 'multilingual transformer models'],
    "Chinese": ['Claude-3.5-Sonnet', 'DeepSeek-R1', 'DeepSeek-v3', 'GPT-4o', 'Jirai-Qwen', 'Llama-3.1-8B', 'Qwen-14B', 'Qwen2.5-7B', 'RNN encoder-decoder', 'Recurrent Neural Networks', 'mBART', 'mT5', 'multilingual transformer models'],
    "English": ['Anthropic-LM v4-s3', 'Centroid+mT5', 'Cohere xlarge v20220609', 'DeepSeek-V2', 'GLM', 'GPT-3 ada v1', 'GPT-3 curie v1', 'GPT-3 davinci v1', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemma-1', 'Graph-ExtractGenerate', 'InstructGPT ada v1', 'InstructGPT curie v1', 'InstructGPT davinci v2', 'InternLM', 'Lead-3', 'Llama-3', 'Llama-3.1', 'M-BERT', 'Mistral-v0.3', 'OPT 175B', 'Oracle', 'Phi-3', 'Pointer-Generator', 'Qwen-1.5', 'Random', 'TextRank', 'Yi-1.5', 'mBART', 'mBERT', 'mT5', 'multilingual transformer models', 'standard transformer'],
    "French": ['Centroid+mT5', 'Dolphin-2.6-Mistral-7B', 'Dolphin-2.6-Phi-2', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Graph-ExtractGenerate', 'LLaMA-2', 'Llama-2-7B-Chat', 'Llama-3.1', 'M-BERT', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-OpenOrca', 'Oracle', 'Phi-2', 'Pointer-Generator', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5', 'multilingual transformer models'],
    "German": ['Centroid+mT5', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Graph-ExtractGenerate', 'Llama-3.1', 'M-BERT', 'Oracle', 'Pointer-Generator', 'Qwen 2.5-7B', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5'],
    "Gujarati": ['mBART', 'mT5', 'multilingual transformer models'],
    "Hausa": ['mBART', 'mT5', 'multilingual transformer models'],
    "Hindi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Igbo": ['mBART', 'mT5', 'multilingual transformer models'],
    "Indonesian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Japanese": ['ChatGPT', 'DeepSeek-v3', 'Flan-T5', 'GPT-3', 'Jirai-Qwen', 'Llama-3.1-8B', 'NICT BERT base', 'Qwen2.5-7B', 'T5', 'Tohoku BERT base', 'Tohoku BERT large', 'Waseda RoBERTa large', 'XLM RoBERTa base', 'XLM RoBERTa large', 'mBART', 'mT5', 'multilingual transformer models'],
    "Kirundi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Korean": ['mBART', 'mT5', 'multilingual transformer models'],
    "Kyrgyz": ['mBART', 'mT5', 'multilingual transformer models'],
    "Marathi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Nepali": ['mBART', 'mT5', 'multilingual transformer models'],
    "Oromo": ['mBART', 'mT5', 'multilingual transformer models'],
    "Pashto": ['mBART', 'mT5', 'multilingual transformer models'],
    "Persian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Pidgin": ['mBART', 'mT5', 'multilingual transformer models'],
    "Portuguese": ['BLOOM', 'DeepSeek', 'GPT-3', 'GPT-4', 'Mistral', 'Mixtral', 'Qwen', 'mBART', 'mT5', 'multilingual transformer models'],
    "Punjabi": ['mBART', 'mT5', 'multilingual transformer models'],
    "Russian": ['BLOOM', 'DeepSeek', 'GPT-3', 'GPT-4', 'Lead-3', 'M-BERT', 'Mistral', 'Mixtral', 'Oracle', 'Pointer-Generator', 'Qwen', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5', 'multilingual transformer models'],
    "Scottish Gaelic": ['mBART', 'mT5', 'multilingual transformer models'],
    "Serbian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Sinhala": ['mBART', 'mT5', 'multilingual transformer models'],
    "Somali": ['mBART', 'mT5', 'multilingual transformer models'],
    "Spanish": ['Centroid+mT5', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Graph-ExtractGenerate', 'Lead-3', 'Llama-3.1', 'M-BERT', 'Oracle', 'Pointer-Generator', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5', 'multilingual transformer models'],
    "Swahili": ['mBART', 'mT5', 'multilingual transformer models'],
    "Tamil": ['mBART', 'mT5', 'multilingual transformer models'],
    "Telugu": ['mBART', 'mT5', 'multilingual transformer models'],
    "Thai": ['mBART', 'mT5', 'multilingual transformer models'],
    "Tigrinya": ['mBART', 'mT5', 'multilingual transformer models'],
    "Turkish": ['Lead-3', 'M-BERT', 'Oracle', 'Pointer-Generator', 'Random', 'TextRank', 'mBART', 'mBERT', 'mT5', 'multilingual transformer models'],
    "Ukrainian": ['mBART', 'mT5', 'multilingual transformer models'],
    "Urdu": ['mBART', 'mT5', 'multilingual transformer models'],
    "Uzbek": ['mBART', 'mT5', 'multilingual transformer models'],
    "Vietnamese": ['mBART', 'mT5', 'multilingual transformer models'],
    "Welsh": ['mBART', 'mT5', 'multilingual transformer models'],
    "Yoruba": ['mBART', 'mT5', 'multilingual transformer models'],
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
    print(f"Task: 05_text_summarization (Reduced Dataset)")
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
