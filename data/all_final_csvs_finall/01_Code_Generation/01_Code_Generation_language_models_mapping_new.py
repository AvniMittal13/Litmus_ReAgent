"""
Language to Models Mapping for 01_Code_Generation
Generated from combined CSV data (without Qwen3 Technical Report)
Total languages: 99
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]
# mHumanEval models: GPT-4o, Claude-3.5-Opus, GPT-3.5, DeepSeek-Coder-V2, WizardCoder, Aya

LANGUAGE_MODELS_MAPPING = {
    "Afrikaans": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Amharic": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Arabic": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Assamese": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Awadhi": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Basque": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Bengali": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'LLaMA-3.1-8B', 'LLaMA-3.1-70B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'Mistral-7B', 'Mistral-Small-24B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'Qwen-2.5-7B', 'Qwen-2.5-72B', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Bhojpuri": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Bodo": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Bosnian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Bulgarian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Burmese": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Catalan": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Cebuano": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Chhattisgarhi": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Chinese": ['Aya', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'CodeBERT', 'CodeGPT', 'CodeGeeX', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeGen2.5', 'CodeLlama', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder', 'DeepSeek-Coder-V2', 'Encoder-Decoder', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'GitHub Copilot', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Qwen-2.5-72B', 'StarCoder', 'Transformer Baseline', 'WizardCoder', 'XLM-R-Encoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Croatian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Czech": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Danish": ['Aya', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'DeepSeek-Coder-V2', 'Encoder-Decoder', 'GPT-3.5', 'GPT-4o', 'Transformer Baseline', 'WizardCoder', 'XLM-R-Encoder'],
    "Dari": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Dutch": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "English": ['24EU-7B', 'Airavata', 'Aya', 'Aya-expanse-8b', 'Bactrian-X', 'BLOOMZ-7B', 'CODEGEN-6.1B', 'CODEX-12B', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'Code-Millenials', 'CodeBERT', 'CodeGPT', 'CodeGeeX', 'CodeGeeX2', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeGen2.5', 'CodeLlama', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'CodeT5-base-220M', 'CppMini', 'DeepSeek-Coder', 'DeepSeek-Coder-V2', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'DigitalGenome-SLM', 'Encoder-Decoder', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'GPT-OSS-120B', 'Gemini-1.5', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Gemini-2.0-Flash-Thinking', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'Gemma-3-27b-it', 'Gemma-7B-IT', 'GitHub Copilot', 'GoScript', 'JSNinja', 'JavaGen', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'LLaMA-3.1-8B', 'LLaMA-3.1-70B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Llama-3.1-8B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-405B-Instruct', 'Llama-3.2-3B-Instruct', 'Llama-3.3-70B-Instruct', 'MBART', 'Micro-CodeLM', 'Mistral-7B', 'Mistral-Large-2', 'Mistral-Small-24B', 'Mixtral-8x7B-v0.1', 'Nemotron-Mini-4B-Instruct', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-4-340B-Instruct', 'PHPCraft', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'PolyCoder', 'PyCoder', 'Qwen-2.5-7B', 'Qwen-2.5-72B', 'Qwen2.5-7B-Instruct', 'Qwen2.5-72B-Instruct', 'Qwen2.5-Coder', 'RubyGem', 'SLT-Code', 'Sarvam-2B-v0.5', 'StarCoder', 'StarCoder2', 'SwiftCode', 'TAE', 'TRANX', 'Transformer Baseline', 'WizardCoder', 'XLM-R-Encoder', 'Yi-Coder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Estonian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Finnish": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "French": ['24EU-7B', 'Aya', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5-72B', 'WizardCoder', 'o1-mini', 'o1-preview'],
    "Ganda": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Garhwali": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Georgian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "German": ['24EU-7B', 'Aya', 'Bactrian-X', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Lima-X', 'Mixtral-8x7B-v0.1', 'WizardCoder'],
    "Greek": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Gujarati": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Haryanvi": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Hausa": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Hebrew": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Hindi": ['Airavata', 'Aya', 'Aya-expanse-8b', 'BLOOMZ-7B', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-OSS-120B', 'Gemini-1.5', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Gemini-2.0-Flash-Thinking', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'Gemma-3-27b-it', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Llama-3.1-8B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-405B-Instruct', 'Llama-3.2-3B-Instruct', 'Mistral-Large-2', 'Nemotron-Mini-4B-Instruct', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-4-340B-Instruct', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'Qwen-2.5-72B', 'Qwen2.5-7B-Instruct', 'Qwen2.5-72B-Instruct', 'Sarvam-2B-v0.5', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Hungarian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Igbo": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Indonesian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Italian": ['24EU-7B', 'Aya', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5-72B', 'WizardCoder', 'o1-mini', 'o1-preview'],
    "Japanese": ['Aya', 'Claude-3.5-Opus', 'CODEGEN-6.1B', 'CODEX-12B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'GitHub Copilot', 'LLaMA-7B', 'MBART', 'TAE', 'TRANX', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3'],
    "Javanese": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kannada": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Kazakh": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Khmer": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kinyarwanda": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Konkani": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Korean": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kurdish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Kyrgyz": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Lao": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Latvian": ['Aya', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'DeepSeek-Coder-V2', 'Encoder-Decoder', 'GPT-3.5', 'GPT-4o', 'Transformer Baseline', 'WizardCoder', 'XLM-R-Encoder'],
    "Lithuanian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Macedonian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Maithili": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Malay": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Malayalam": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Malvi": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Manipuri": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Marathi": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Marwari": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Nepali": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Norwegian": ['Aya', 'Claude-3.5-Opus', 'CodeBERT', 'CodeGPT', 'DeepSeek-Coder-V2', 'Encoder-Decoder', 'GPT-3.5', 'GPT-4o', 'Transformer Baseline', 'WizardCoder', 'XLM-R-Encoder'],
    "Odia": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Oromo": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Pashto": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Persian": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Polish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Portuguese": ['Aya', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'Mistral-Large-2', 'Qwen-2.5-72B', 'WizardCoder', 'o1-mini', 'o1-preview'],
    "Punjabi": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Rajasthani": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Romanian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Russian": ['Aya', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'CODEGEN-6.1B', 'CODEX-12B', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'MBART', 'Mistral-Large-2', 'Qwen-2.5-72B', 'TAE', 'TRANX', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Sango": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Sanskrit": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Santali": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Sardinian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Serbian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Shona": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Sindhi": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Sinhala": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Slovak": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Slovenian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Somali": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Spanish": ['24EU-7B', 'Aya', 'Bactrian-X', 'Claude-3-Haiku', 'Claude-3-Sonnet', 'Claude-3.5-Opus', 'Claude-3.5-Sonnet', 'CODEGEN-6.1B', 'CODEX-12B', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5-flash', 'Gemini-1.5-pro', 'Lima-X', 'Llama-3.1-405B', 'Llama-3.1-70B', 'Llama-3.1-8B', 'MBART', 'Mistral-Large-2', 'Mixtral-8x7B-v0.1', 'Qwen-2.5-72B', 'TAE', 'TRANX', 'WizardCoder', 'codellama/CodeLlama-7b-Instruct-hf', 'google/codegemma-7b-it', 'mistralai/Mistral-7B-Instruct-v0.3', 'o1-mini', 'o1-preview'],
    "Sundanese": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Swedish": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Tagalog": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Tamil": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Telugu": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Thai": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Tibetan": ['Airavata', 'BLOOMZ-7B', 'GPT-3.5', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Tsonga": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Turkish": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
    "Ukrainian": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Urdu": ['Airavata', 'Aya', 'BLOOMZ-7B', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-2.0-Flash-Thinking', 'Gemma-7B-IT', 'LLaMA-7B', 'LLaMA-13B', 'LLaMA-65B', 'PaLM-2-XXS', 'PaLM-2-XS', 'PaLM-2-S', 'PaLM-2-L', 'WizardCoder', 'mT5-B', 'mT5-L', 'mT5-XL', 'mT5-XXL'],
    "Uyghur": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Uzbek": ['Aya', 'Claude-3.5-Opus', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4o', 'WizardCoder'],
    "Vietnamese": ['Aya', 'Claude-3.5-Opus', 'CodeGen2-1B', 'CodeGen2-3.7B', 'CodeGen2-7B', 'CodeGen2-16B', 'CodeT5+-220M', 'CodeT5+-770M', 'CodeT5+-2B', 'DeepSeek-Coder-V2', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'WizardCoder'],
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
