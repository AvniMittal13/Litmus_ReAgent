"""
Language to Models Mapping for 01_code_generation (Reduced Dataset)
Generated from reduced CSV data
Total languages: 33
Total unique models: 77
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Afrikaans": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Arabic": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Bulgarian": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Chinese": ['Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'CodeBERT', 'CodeGPT', 'CodeGeeX', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeGen2.5', 'CodeLlama', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder', 'Encoder-Decoder', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Qwen-2.5-72B', 'StarCoder', 'Transformer-Baseline', 'CodeLlama-7b-Instruct-hf', 'CodeGemma-7b-it', 'Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview', 'XLM-R-Encoder'],
    "Danish": ['CodeBERT', 'CodeGPT', 'Encoder-Decoder', 'Transformer-Baseline', 'XLM-R-Encoder'],
    "Dutch": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "English": ['24EU-7B', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'Code-Millenials', 'CodeBERT', 'CodeGPT', 'CodeGeeX', 'CodeGeeX2', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeGen2.5', 'CodeLlama', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'CodeT5-base-220M', 'CppMini', 'DeepSeek-Coder', 'DigitalGenome-SLM', 'Encoder-Decoder', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4-judge', 'GPT-4o', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'GoScript', 'JSNinja', 'JavaGen', 'LLaMA-7B', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Llama-3.3-70B-Instruct', 'MBART', 'Micro-CodeLM', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'PHPCraft', 'PolyCoder', 'PyCoder', 'Qwen-2.5-72B', 'Qwen2.5-Coder', 'RubyGem', 'SLT-Code', 'StarCoder', 'StarCoder2', 'SwiftCode', 'TAE', 'TRANX', 'Transformer-Baseline', 'WizardCoder', 'Yi-Coder', 'CodeLlama-7b-Instruct-hf', 'CodeGemma-7b-it', 'Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview', 'XLM-R-Encoder'],
    "Estonian": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Finnish": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "French": ['24EU-7B', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4', 'GPT-4-judge', 'GPT-4o', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5-72B', 'o1-mini', 'o1-preview'],
    "German": ['24EU-7B', 'Bactrian-X', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4', 'GPT-4-judge', 'Lima-X', 'Mixtral-8x7B-v0.1'],
    "Greek": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Hebrew": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Hindi": ['Aya-expanse-8b', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'GPT-4', 'GPT-4o', 'GPT-OSS-120B', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'Gemma-3-27b-it', 'LLaMA-7B', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Llama-3.1-405B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-8B-Instruct', 'Llama-3.2-3B-Instruct', 'Mistral-Large-2', 'Nemotron-4-340B-Instruct', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-Mini-4B-Instruct', 'Qwen-2.5-72B', 'Qwen2.5-72B-Instruct', 'Qwen2.5-7B-Instruct', 'Sarvam-2B-v0.5', 'CodeLlama-7b-Instruct-hf', 'CodeGemma-7b-it', 'Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Hungarian": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Indonesian": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Italian": ['24EU-7B', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4', 'GPT-4-judge', 'GPT-4o', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5-72B', 'o1-mini', 'o1-preview'],
    "Japanese": ['GPT-4', 'MBART', 'TAE', 'TRANX', 'CodeLlama-7b-Instruct-hf', 'CodeGemma-7b-it', 'Mistral-7B-Instruct-v0.3'],
    "Latvian": ['CodeBERT', 'CodeGPT', 'Encoder-Decoder', 'Transformer-Baseline', 'XLM-R-Encoder'],
    "Malay": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Marathi": ['Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'LLaMA-7B'],
    "Norwegian": ['CodeBERT', 'CodeGPT', 'Encoder-Decoder', 'Transformer-Baseline', 'XLM-R-Encoder'],
    "Persian": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Portuguese": ['Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Qwen-2.5-72B', 'o1-mini', 'o1-preview'],
    "Punjabi": ['Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'LLaMA-7B'],
    "Russian": ['Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'MBART', 'Mistral-Large-2', 'Qwen-2.5-72B', 'TAE', 'TRANX', 'CodeLlama-7b-Instruct-hf', 'CodeGemma-7b-it', 'Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Sanskrit": ['Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'LLaMA-7B'],
    "Spanish": ['24EU-7B', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4', 'GPT-4-judge', 'GPT-4o', 'Gemini-1.5-Flash', 'Gemini-1.5-Pro', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'MBART', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5-72B', 'TAE', 'TRANX', 'CodeLlama-7b-Instruct-hf', 'CodeGemma-7b-it', 'Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Tagalog": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Tamil": ['Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'LLaMA-7B'],
    "Turkish": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
    "Urdu": ['Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'LLaMA-7B'],
    "Vietnamese": ['CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'GPT-3.5', 'GPT-4'],
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
    print(f"Task: 01_code_generation (Reduced Dataset)")
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
