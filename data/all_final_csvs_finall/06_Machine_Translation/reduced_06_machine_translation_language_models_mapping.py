"""
Language to Models Mapping for 06_machine_translation (Reduced Dataset)
Generated from reduced CSV data
Total languages: 137
Total unique models: 138
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Acehnese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Afrikaans": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Albanian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Amharic": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Arabic": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-MT-systems'],
    "Aragonese": ['Various-systems'],
    "Aranese": ['Various-systems'],
    "Armenian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Assamese": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Asturian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'Various-systems'],
    "Azerbaijani": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Bambara": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Basque": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Baule": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Belarusian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Bengali": ['BongLLaMA', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'GPT-davinci-002', 'Gemini', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Google-Translate', 'IndicTrans2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'LibreTranslate', 'Llama-3.2-1B', 'Llama-3.2-3B', 'Mistral-Small-24B', 'Mistral-7B', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'Qwen-2.5-72B', 'Qwen-2.5-7B', 'Qwen2.5-1.5B', 'T5', 'TituLLM-1B', 'TituLLM-3B', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Bodo": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Bosnian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Brazilian-Portuguese": ['CLTeam', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4o-mini', 'Gemma-2-27B', 'HW-TSC', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Mistral-7B', 'Multitan-GML', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'SETU-ADAPT', 'SheffieldGATE', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'mBART-50'],
    "Bulgarian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Burmese": ['PaLM-X', 'XLM-R', 'mBERT', 'mT5'],
    "Catalan": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Chinese": ['Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek', 'DeepSeek-V2.5', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-Pro', 'Gemma-3-27B', 'Human-Translators', 'IndicTrans2', 'LibreTranslate', 'Llama-3.1-70B-Instruct', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen2', 'Qwen2.5-Coder-32B-Instruct', 'Seamless-M4T', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mT5'],
    "Chinese-Simplified": ['T5', 'XLM-R', 'mBart'],
    "Congolese-Swahili": ['Neural-machine-translation-models', 'cross-dialect-transfer-methods', 'semi-supervised-learning-approaches'],
    "Croatian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Czech": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Czech-Ukrainian": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "Danish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Dinka": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Dogri": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Dutch": ['CLTeam', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Mistral-7B', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "English": ['BongLLaMA', 'CLTeam', 'Claude-3', 'Claude3.5', 'DCUGenNLP', 'DeepSeek', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'DeepText-Lab', 'FT-W', 'FT-WC', 'GPT-2', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'GPT-davinci-002', 'Gemini', 'Gemini-2.0-Flash', 'Gemini-Pro', 'Gemma-3-27B', 'Gemma-2-27B', 'Google-Translate', 'HW-TSC', 'HindiLLM-Medium-355M', 'HindiLLM-Small-124M', 'Human-Translators', 'IndicBERT', 'IndicFT', 'IndicTrans2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Llama-3.2-1B', 'Llama-3.2-3B', 'Llama3-70B', 'Mistral-Small-24B', 'Mistral-7B', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'NVIDIA-NeMo', 'Online-A', 'Online-B', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen-2.5-72B', 'Qwen-2.5-7B', 'Qwen2', 'Qwen2.5-1.5B', 'SETU-ADAPT', 'Seamless-M4T', 'SheffieldGATE', 'T5', 'TituLLM-1B', 'TituLLM-3B', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'TransmissionMT', 'Unbabel-IT', 'Unbabel-Tower-70B', 'XLM-R', 'ZMT', 'iNLTK', 'mBART-50', 'mBERT', 'mBart', 'mT5'],
    "English-Chinese": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Czech": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-French": ['Transformer'],
    "English-German": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'Transformer', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Hebrew": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Japanese": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Russian": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "Esperanto": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Estonian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Ewe": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Faroese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Filipino": ['T5', 'XLM-R', 'mBart'],
    "Finnish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "French": ['CLTeam', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Mistral-7B', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Neural-machine-translation-models', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'cross-dialect-transfer-methods', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'semi-supervised-learning-approaches'],
    "Fulah": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Galician": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Georgian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "German": ['CLTeam', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Mistral-7B', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Greek": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Gujarati": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'NLLB-200', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'mT5', 'various-LLMs'],
    "Hausa": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Hebrew": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Hindi": ['Aya-expanse-8b', 'Claude3.5', 'FT-W', 'FT-WC', 'GPT-2', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-OSS-120B', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Gemma-2-27b-it', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'HindiLLM-Medium-355M', 'HindiLLM-Small-124M', 'Human-Translators', 'IndicBERT', 'IndicFT', 'IndicTrans2', 'LibreTranslate', 'Llama-3.1-405B-Instruct', 'Llama-3.1-8B-Instruct', 'Llama-3.2-3B-Instruct', 'Llama3-70B', 'NLLB', 'NLLB-200', 'NVIDIA-NeMo', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-Mini-4B-Instruct', 'Online-A', 'Online-B', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'Seamless-M4T', 'T5', 'TransmissionMT', 'Unbabel-Tower-70B', 'XLM-R', 'ZMT', 'iNLTK', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Hungarian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Icelandic": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Igbo": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'various-MT-systems'],
    "Indonesian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Irish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Italian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Japanese": ['Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek', 'DeepSeek-V2.5', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-Pro', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'Llama-3.1-70B-Instruct', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen2', 'Qwen2.5-Coder-32B-Instruct', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Javanese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Kannada": ['IndicTrans2', 'NLLB-200', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'mT5', 'various-LLMs'],
    "Kashmiri": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Kazakh": ['PaLM-X', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Khmer": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Kikuyu": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Kinyarwanda": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'M2M-100', 'NLLB-200', 'mBART-50', 'various-MT-systems'],
    "Konkani": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Korean": ['CLTeam', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Mistral-7B', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Kurdish-Kurmanji": ['T5', 'XLM-R', 'mBart'],
    "Lao": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Latvian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Lingala": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Lithuanian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Luganda": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'M2M-100', 'NLLB-200', 'mBART-50', 'various-MT-systems'],
    "Luxembourgish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Macedonian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Maithili": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Malay": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Malayalam": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Maltese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Manipuri": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Marathi": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'NLLB-200', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Mongolian": ['T5', 'XLM-R', 'mBart'],
    "Nepali": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBart', 'mT5', 'various-LLMs'],
    "Norwegian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Norwegian-Bokmal": ['IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'mBART', 'mBART50', 'mT5'],
    "Occitan": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Odia": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Oromo": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Pashto": ['T5', 'XLM-R', 'mBart'],
    "Persian": ['T5', 'XLM-R', 'mBart'],
    "Persian-Farsi": ['PaLM-X', 'XLM-R', 'mBERT', 'mT5'],
    "Polish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Portuguese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Punjabi": ['IndicTrans2', 'NLLB-200', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'mT5', 'various-LLMs'],
    "Romanian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Russian": ['GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Human-Translators', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'Seamless-M4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Sanskrit": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Santali": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Serbian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Shona": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Sindhi": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Sinhala": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Slovak": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Slovenian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Somali": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'various-MT-systems'],
    "Spanish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Standard-Swahili": ['Neural-machine-translation-models', 'cross-dialect-transfer-methods', 'semi-supervised-learning-approaches'],
    "Sundanese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Swahili": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-MT-systems'],
    "Swedish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Tagalog": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Tamil": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'NLLB-200', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Telugu": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Thai": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Tigrinya": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Turkish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Twi": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Ukrainian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Ukrainian-English": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "Urdu": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'NLLB-200', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Valencian": ['Various-systems'],
    "Vietnamese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Welsh": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Wolof": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Xhosa": ['IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'Opus-MT', 'mBART', 'mBART50', 'mT5'],
    "Yoruba": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBART-50', 'mBERT', 'mT5', 'various-MT-systems'],
    "Yoruba-English": ['Facebook-M2M', 'Google', 'neural-MT-models'],
    "Zulu": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
}

# Statistics (dynamically calculated)
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
    print(f"Task: 06_machine_translation (Reduced Dataset)")
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
