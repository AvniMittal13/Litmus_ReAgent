"""
Language to Models Mapping for 01_Code_Generation
Generated from combined CSV data
Total languages: 79
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Afrikaans": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Amharic": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Arabic": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Basque": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Bengali": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'WizardCoder'],
    "Bosnian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Bulgarian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Burmese": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Catalan": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Cebuano": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Chinese": ['Aya', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'CodeGeeX', 'CodeGen2', 'CodeGen2.5', 'CodeLlama', 'CodeT5+', 'DeepSeek-Coder', 'DeepSeek-Coder-V2', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'GitHub Copilot', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'Mistral Large 2', 'Qwen-2.5 72B', 'StarCoder', 'Transformer Baseline', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview', 'pretrained Transformer'],
    "Croatian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Czech": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Danish": ['Aya', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'DeepSeek-Coder-V2', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-4o', 'Transformer Baseline', 'WizardCoder', 'pretrained Transformer'],
    "Dari": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Dutch": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "English": ['24EU-7B', 'Aya', 'Bactrian-X variants', 'CODEGEN 6.1B', 'CODEX 12B', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'Code-Millenials', 'CodeBERT', 'CodeGPT', 'CodeGeeX', 'CodeGeeX2', 'CodeGen2', 'CodeGen2.5', 'CodeLlama', 'CodeT5+', 'CodeT5-base', 'CppMini', 'DeepSeek-Coder', 'DeepSeek-Coder-V2', 'DigitalGenome-SLM', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'GitHub Copilot', 'GoScript', 'JSNinja', 'JavaGen', 'LLaMA 7B', 'Lima-X variants', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'Llama 3.3 70B-Instruct', 'MBART', 'Micro-CodeLM', 'Mistral Large 2', 'Mixtral-8x7B-v0.1', 'PHPCraft', 'PolyCoder', 'PyCoder', 'Qwen-2.5 72B', 'Qwen2.5-Coder', 'RubyGem', 'SLT-Code', 'StarCoder', 'StarCoder2', 'SwiftCode', 'TAE', 'TRANX', 'Transformer Baseline', 'WizardCoder', 'Yi-Coder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview', 'pretrained Transformer'],
    "Estonian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Finnish": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "French": ['24EU-7B', 'Aya', 'Bactrian-X variants', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'Lima-X variants', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'Mistral Large 2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5 72B', 'WizardCoder', 'o1-mini', 'o1-preview'],
    "Ganda": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Georgian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "German": ['24EU-7B', 'Aya', 'Bactrian-X variants', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Lima-X variants', 'Mixtral-8x7B-v0.1', 'WizardCoder'],
    "Greek": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Hausa": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Hebrew": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Hindi": ['Aya', 'Aya-expanse-8b', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'GPT-OSS-120B', 'Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'Gemma-3-27b-it', 'LLaMA 7B', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'Llama-3.1-405B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-8B-Instruct', 'Llama-3.2-3B-Instruct', 'Mistral Large 2', 'Nemotron-4-340B-Instruct', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-Mini-4B-Instruct', 'Qwen-2.5 72B', 'Qwen2.5-72B-Instruct', 'Qwen2.5-7B-Instruct', 'Sarvam-2B-v0.5', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Hungarian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Igbo": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Indonesian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Italian": ['24EU-7B', 'Aya', 'Bactrian-X variants', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'Lima-X variants', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'Mistral Large 2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5 72B', 'WizardCoder', 'o1-mini', 'o1-preview'],
    "Japanese": ['Aya', 'CODEGEN 6.1B', 'CODEX 12B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GitHub Copilot', 'MBART', 'TAE', 'TRANX', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3'],
    "Javanese": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kannada": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'WizardCoder'],
    "Kazakh": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Khmer": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kinyarwanda": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Korean": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kurdish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kyrgyz": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Lao": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Latvian": ['Aya', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'DeepSeek-Coder-V2', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-4o', 'Transformer Baseline', 'WizardCoder', 'pretrained Transformer'],
    "Lithuanian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Macedonian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Malay": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Malayalam": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'WizardCoder'],
    "Marathi": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'LLaMA 7B', 'WizardCoder'],
    "Nepali": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'WizardCoder'],
    "Norwegian": ['Aya', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'DeepSeek-Coder-V2', 'Encoder-Decoder models', 'GPT-3.5', 'GPT-4o', 'Transformer Baseline', 'WizardCoder', 'pretrained Transformer'],
    "Odia": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'WizardCoder'],
    "Oromo": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Persian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Polish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Portuguese": ['Aya', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'Mistral Large 2', 'Qwen-2.5 72B', 'WizardCoder', 'o1-mini', 'o1-preview'],
    "Punjabi": ['Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'LLaMA 7B'],
    "Romanian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Russian": ['Aya', 'CODEGEN 6.1B', 'CODEX 12B', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'MBART', 'Mistral Large 2', 'Qwen-2.5 72B', 'TAE', 'TRANX', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Sango": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Sanskrit": ['Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'LLaMA 7B'],
    "Sardinian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Serbian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Shona": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Sindhi": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Sinhala": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Slovak": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Slovenian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Somali": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Spanish": ['24EU-7B', 'Aya', 'Bactrian-X variants', 'CODEGEN 6.1B', 'CODEX 12B', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5 Sonnet', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5 flash', 'Gemini-1.5 pro', 'Lima-X variants', 'Llama 3.1 405B', 'Llama 3.1 70B', 'Llama 3.1 8B', 'MBART', 'Mistral Large 2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5 72B', 'TAE', 'TRANX', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Sundanese": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Swedish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Tagalog": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Tamil": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5-turbo', 'GPT-4o', 'Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'LLaMA 7B', 'Tamil-LLaMA-13B', 'Tamil-LLaMA-70B', 'Tamil-LLaMA-7B', 'WizardCoder'],
    "Telugu": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'WizardCoder'],
    "Thai": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Tsonga": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Turkish": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Ukrainian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Urdu": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-4o', 'Gemini 1.5', 'Gemini 2.0 Flash Thinking', 'LLaMA 7B', 'WizardCoder'],
    "Uyghur": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Uzbek": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Vietnamese": ['Aya', 'Claude-3.5-Opus', 'CodeGen2', 'CodeT5+', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Yiddish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
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
    return sorted(all_models)


def get_language_statistics():
    """Get statistics about each language's model coverage."""
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
    print(f"Task: 01_Code_Generation")
    print(f"Total Languages: {TOTAL_LANGUAGES}")
    print(f"Total Unique Models: {TOTAL_UNIQUE_MODELS}")


if __name__ == "__main__":
    print_summary()