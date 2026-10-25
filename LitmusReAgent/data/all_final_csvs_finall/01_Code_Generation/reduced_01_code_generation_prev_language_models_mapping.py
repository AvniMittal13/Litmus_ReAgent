"""
Language to Models Mapping for 01_code_generation_prev (Reduced Dataset)
Generated from reduced CSV data
Total languages: 27
Total unique models: 51
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Afrikaans": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Arabic": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Bulgarian": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Chinese": ['CodeBERT', 'CodeGPT', 'CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-4', 'Transformer Baseline', 'pretrained Transformer (encoder initialized with XLM-R)'],
    "Danish": ['CodeBERT', 'CodeGPT', 'Encoder-Decoder models', 'Transformer Baseline', 'pretrained Transformer (encoder initialized with XLM-R)'],
    "Dutch": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "English": ['24EU-7B', 'Bactrian-X variants', 'Code-Millenials', 'CodeBERT', 'CodeGPT', 'CodeGeeX2', 'CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeLlama', 'CodeT5+ (220M, 770M, 2B)', 'CodeT5-base (220M)', 'CppMini', 'DeepSeek-Coder', 'DigitalGenome-SLM', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-4', 'GPT-4 (as judge)', 'GoScript', 'JSNinja', 'JavaGen', 'Lima-X variants', 'Llama 3.3 70B-Instruct', 'Micro-CodeLM', 'Mixtral-8x7B-v0.1', 'PHPCraft', 'PolyCoder', 'PyCoder', 'Qwen2.5-Coder', 'RubyGem', 'SLT-Code', 'StarCoder2', 'SwiftCode', 'Transformer Baseline', 'WizardCoder', 'Yi-Coder', 'pretrained Transformer (encoder initialized with XLM-R)'],
    "Estonian": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Finnish": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "French": ['24EU-7B', 'Bactrian-X variants', 'CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4', 'GPT-4 (as judge)', 'Lima-X variants', 'Mixtral-8x7B-v0.1'],
    "German": ['24EU-7B', 'Bactrian-X variants', 'CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4', 'GPT-4 (as judge)', 'Lima-X variants', 'Mixtral-8x7B-v0.1'],
    "Greek": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Hebrew": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Hindi": ['Aya-expanse-8b', 'GPT-OSS-120B', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'Gemma-3-27b-it', 'Llama-3.1-405B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-8B-Instruct', 'Llama-3.2-3B-Instruct', 'Nemotron-4-340B-Instruct', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-Mini-4B-Instruct', 'Qwen2.5-72B-Instruct', 'Qwen2.5-7B-Instruct', 'Sarvam-2B-v0.5'],
    "Hungarian": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Indonesian": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Italian": ['24EU-7B', 'Bactrian-X variants', 'CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4', 'GPT-4 (as judge)', 'Lima-X variants', 'Mixtral-8x7B-v0.1'],
    "Latvian": ['CodeBERT', 'CodeGPT', 'Encoder-Decoder models', 'Transformer Baseline', 'pretrained Transformer (encoder initialized with XLM-R)'],
    "Malay": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Norwegian": ['CodeBERT', 'CodeGPT', 'Encoder-Decoder models', 'Transformer Baseline', 'pretrained Transformer (encoder initialized with XLM-R)'],
    "Persian": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Portuguese": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Russian": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Spanish": ['24EU-7B', 'Bactrian-X variants', 'CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4', 'GPT-4 (as judge)', 'Lima-X variants', 'Mixtral-8x7B-v0.1'],
    "Tagalog": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Turkish": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
    "Vietnamese": ['CodeGen2 (1B, 3.7B, 7B, 16B)', 'CodeT5+ (220M, 770M, 2B)', 'GPT-3.5', 'GPT-4'],
}

# Statistics
TOTAL_LANGUAGES = 27
TOTAL_UNIQUE_MODELS = 51

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
    print(f"Task: 01_code_generation_prev (Reduced Dataset)")
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
