"""
Language to Models Mapping for 06_Machine_Translation
Generated from combined CSV data
Total languages: 169
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "AR→EN": ['BLOOMZ', 'GPT-3.5', 'GPT-4', 'Jais-13b-chat', 'SOTA NMT'],
    "Abkhazian": ['NLLB-200 family (Dense 3.3B, 1.3B, Distilled 1.3B, 600M, MoE 54.5B)'],
    "Acehnese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Afar": ['NLLB-200 family (Dense 3.3B, 1.3B, Distilled 1.3B, 600M, MoE 54.5B)'],
    "Afrikaans": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Albanian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T'],
    "Amharic": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Arabic": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train', 'various-MT-systems'],
    "Aragonese": ['Various-systems'],
    "Aranese": ['Various-systems'],
    "Armenian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T'],
    "Asante-Twi": ['LibreTranslate', 'NLLB', 'Opus-MT', 'mBART50'],
    "Assamese": ['Adam-optimizer', 'Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek-V2.5', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-1.5-Pro', 'IndicTrans2', 'IndicTrans2-baseline', 'Llama-3.1-70B-Instruct', 'M2M-100', 'Multilingual-Transformer-35-layer', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen2.5-72B-Instruct', 'SeamlessM4T', 'Transformer', 'mBART-50', 'mT5', 'multilingual-baseline', 'no-models', 'various-LLMs'],
    "Asturian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio', 'Various-systems'],
    "Azerbaijani": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T'],
    "Bambara": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Basque": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Baule": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Belarusian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio'],
    "Bengali": ['BongLLaMA', 'ChatGPT-GPT-3.5-4', 'Claude-3', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'GPT-davinci-002', 'Gemini', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Google', 'Google-Translate', 'IndicTrans2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'LibreTranslate', 'Llama-3.2-1B', 'Llama-3.2-3B', 'M2M-100', 'M2M-100-various-sizes', 'MSFT', 'Mistral-Small-24B', 'Mistral-7B', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen-2.5-72B', 'Qwen-2.5-7B', 'Qwen2.5-1.5B', 'SeamlessM4T', 'T5', 'TituLLM-1B', 'TituLLM-3B', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Bislama": ['NLLB-200-family'],
    "Bodo": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Bosnian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T'],
    "Brazilian-Portuguese": ['CLTeam', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4o-mini', 'Gemma-2-27B', 'HW-TSC', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'Mistral-7B', 'Multitan-GML', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'SETU-ADAPT', 'SheffieldGATE', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'mBART-50'],
    "Bulgarian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Burmese": ['NLLB-200-family', 'PaLM-X', 'XLM-R', 'mBERT', 'mT5'],
    "Catalan": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Cebuano": ['M2M-100-various-sizes', 'NLLB-200-family'],
    "Chichewa": ['NLLB-200-family'],
    "Chinese": ['Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek', 'DeepSeek-V2.5', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemini-Pro', 'Gemma-3-27B', 'Human-Translators', 'IndicTrans2', 'LibreTranslate', 'Llama-3.1-70B-Instruct', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen2', 'Qwen2.5-Coder-32B-Instruct', 'Seamless-M4T', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Congolese-Swahili": ['Neural-machine-translation-models', 'cross-dialect-transfer-methods', 'semi-supervised-learning-approaches'],
    "Corsican": ['NLLB-200-family'],
    "Croatian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Czech": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Czech-Ukrainian": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "Danish": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Dari": ['NLLB-200-family'],
    "Dinka": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Dogri": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Dutch": ['CLTeam', 'Claude-3', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'M2M-100', 'M2M-100-various-sizes', 'Mistral-7B', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SeamlessM4T', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "EN→AR": ['AraT5', 'BLOOMZ', 'ChatGPT', 'GPT-3.5', 'GPT-4', 'Jais-13b-chat', 'LLaMA-3-70B', 'SOTA NMT'],
    "English": ['Adam-optimizer', 'BongLLaMA', 'CLTeam', 'Claude-3', 'Claude-3.5-Sonnet', 'Claude3.5', 'DCUGenNLP', 'DeepSeek', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'DeepSeek-V2.5', 'DeepText-Lab', 'FT-W', 'FT-WC', 'GPT-2', 'GPT-3.5', 'GPT-3.5-Turbo', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'GPT-davinci-002', 'Gemini', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemini-1.5-Pro', 'Gemini-Pro', 'Gemma-3-27B', 'Gemma-2-27B', 'Google-Translate', 'HW-TSC', 'HindiLLM-Medium-355M', 'HindiLLM-Small-124M', 'Human-Translators', 'IndicBERT', 'IndicFT', 'IndicTrans2', 'IndicTrans2-baseline', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'Llama-3-8B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-8B', 'Llama-3.2-1B', 'Llama-3.2-3B', 'Llama3-70B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Mistral-Small-24B', 'Mistral-7B', 'Multilingual-LSTM-encoder', 'Multilingual-Transformer-35-layer', 'Multilingual-bag-of-words-encoder', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'NVIDIA-NeMo', 'Online-A', 'Online-B', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen-2.5-72B', 'Qwen-2.5-7B', 'Qwen2', 'Qwen2.5-1.5B', 'Qwen2.5-72B-Instruct', 'SETU-ADAPT', 'Seamless-M4T', 'SeamlessM4T', 'SheffieldGATE', 'T5', 'TituLLM-1B', 'TituLLM-3B', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer', 'Transformer-25-6', 'TransmissionMT', 'Unbabel-IT', 'Unbabel-Tower-70B', 'XLM-R', 'ZMT', 'iNLTK', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'multilingual-baseline', 'no-models', 'translate-test', 'translate-train'],
    "English-Chinese": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Czech": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-French": ['Transformer'],
    "English-German": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'Transformer', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Hebrew": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Japanese": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "English-Russian": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "Esperanto": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Estonian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Ewe": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'NLLB-200-family', 'Qwen-2-Audio'],
    "Faroese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Farsi": ['ChatGPT-GPT-3.5-4', 'Google', 'MSFT'],
    "Filipino": ['NLLB-200-family', 'T5', 'XLM-R', 'mBart'],
    "Finnish": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "French": ['CLTeam', 'Claude-3', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Mistral-7B', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Neural-machine-translation-models', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SeamlessM4T', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'cross-dialect-transfer-methods', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'semi-supervised-learning-approaches', 'translate-test', 'translate-train'],
    "Fulah": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Galician": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'Qwen-2-Audio'],
    "Georgian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "German": ['CLTeam', 'Claude-3', 'DCUGenNLP', 'DeepText-Lab', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-8B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Mistral-7B', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SETU-ADAPT', 'SeamlessM4T', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Greek": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Guarani": ['NLLB-200-family'],
    "Gujarati": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'mT5', 'various-LLMs'],
    "Gulf": ['AraT5', 'BLOOMZ', 'ChatGPT', 'GPT-3.5', 'GPT-4', 'Jais-13b-chat', 'LLaMA-3-70B', 'SOTA NMT'],
    "Haitian-Creole": ['M2M-100-various-sizes', 'NLLB-200-family'],
    "Hausa": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'NLLB-200-family', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Hebrew": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Hindi": ['Aya-expanse-8b', 'Claude-3', 'Claude3.5', 'FT-W', 'FT-WC', 'GPT-2', 'GPT-3.5-Turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-OSS-120B', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Gemma-2-27b-it', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'HindiLLM-Medium-355M', 'HindiLLM-Small-124M', 'Human-Translators', 'IndicBERT', 'IndicFT', 'IndicTrans2', 'LibreTranslate', 'Llama-3.1-405B-Instruct', 'Llama-3.1-8B-Instruct', 'Llama-3.2-3B-Instruct', 'Llama3-70B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'NVIDIA-NeMo', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-Mini-4B-Instruct', 'Online-A', 'Online-B', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Seamless-M4T', 'SeamlessM4T', 'T5', 'TransmissionMT', 'Unbabel-Tower-70B', 'XLM-R', 'ZMT', 'iNLTK', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train', 'various-LLMs'],
    "Hmong": ['NLLB-200-family'],
    "Hungarian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Icelandic": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Igbo": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'various-MT-systems'],
    "Ilocano": ['NLLB-200-family'],
    "Indonesian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Irish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Italian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Japanese": ['Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek', 'DeepSeek-V2.5', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemini-Pro', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'Llama-3.1-70B-Instruct', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen2', 'Qwen2.5-Coder-32B-Instruct', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5'],
    "Javanese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Jinghpaw": ['LibreTranslate', 'NLLB', 'Opus-MT', 'mBART50'],
    "Kannada": ['IndicTrans2', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'mT5', 'various-LLMs'],
    "Kashmiri": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Kazakh": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'SeamlessM4T', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Khasi": ['Adam-optimizer', 'Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek-V2.5', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-1.5-Pro', 'IndicTrans2', 'IndicTrans2-baseline', 'Llama-3.1-70B-Instruct', 'M2M-100', 'Multilingual-Transformer-35-layer', 'NLLB-200', 'PaLM-2', 'Qwen2.5-72B-Instruct', 'SeamlessM4T', 'Transformer', 'multilingual-baseline', 'no-models'],
    "Khmer": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBart'],
    "Kikuyu": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Kinyarwanda": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'M2M-100', 'NLLB-200', 'NLLB-200-family', 'mBART-50', 'various-MT-systems'],
    "Konkani": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Korean": ['Adam-optimizer', 'CLTeam', 'Claude-3', 'Claude-3.5-Sonnet', 'DCUGenNLP', 'DeepSeek-V2.5', 'DeepText-Lab', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'GPT-4o-mini', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemini-1.5-Pro', 'Gemma-3-27B', 'Gemma-2-27B', 'HW-TSC', 'IndicTrans2', 'IndicTrans2-baseline', 'LibreTranslate', 'Llama-3-8B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-8B', 'M2M-100', 'M2M-100-various-sizes', 'Mistral-7B', 'Multilingual-Transformer-35-layer', 'Multitan-GML', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'NLLB-3.3B', 'NLLB-3.3B-Baseline', 'NLLB-600M', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen2.5-72B-Instruct', 'SETU-ADAPT', 'SeamlessM4T', 'SheffieldGATE', 'T5', 'Tower-7B', 'TowerInstruct-7B-v0.2', 'Transformer', 'Transformer-25-6', 'Unbabel-IT', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'multilingual-baseline'],
    "Kurdish": ['M2M-100-various-sizes', 'NLLB-200-family', 'T5', 'XLM-R', 'mBart'],
    "Kyrgyz": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T'],
    "Lao": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio'],
    "Latin": ['M2M-100-various-sizes', 'NLLB-200-family'],
    "Latvian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Levantine": ['AraT5', 'BLOOMZ', 'ChatGPT', 'GPT-3.5', 'GPT-4', 'Jais-13b-chat', 'LLaMA-3-70B', 'SOTA NMT'],
    "Lingala": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Lithuanian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Luganda": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'M2M-100', 'NLLB-200', 'mBART-50', 'various-MT-systems'],
    "Luxembourgish": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio'],
    "MSA": ['AraT5', 'BLOOMZ', 'ChatGPT', 'GPT-3.5', 'GPT-4', 'Jais-13b-chat', 'LLaMA-3-70B', 'SOTA NMT'],
    "Macedonian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Maghrebi": ['AraT5', 'BLOOMZ', 'ChatGPT', 'GPT-3.5', 'GPT-4', 'Jais-13b-chat', 'LLaMA-3-70B', 'SOTA NMT'],
    "Maithili": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Malagasy": ['M2M-100-various-sizes', 'NLLB-200-family'],
    "Malay": ['ChatGPT-GPT-3.5-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Google', 'M2M-100-various-sizes', 'MSFT', 'NLLB-200-family', 'PaLM-X', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Malayalam": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Maltese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio'],
    "Manipuri": ['Adam-optimizer', 'Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek-V2.5', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-1.5-Pro', 'IndicTrans2', 'IndicTrans2-baseline', 'Llama-3.1-70B-Instruct', 'M2M-100', 'Multilingual-Transformer-35-layer', 'NLLB-200', 'PaLM-2', 'Qwen2.5-72B-Instruct', 'SeamlessM4T', 'Transformer', 'mBART-50', 'mT5', 'multilingual-baseline', 'no-models', 'various-LLMs'],
    "Marathi": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Mizo": ['Adam-optimizer', 'Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek-V2.5', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'Gemini-1.5', 'Gemini-1.5-Pro', 'IndicTrans2', 'IndicTrans2-baseline', 'Llama-3.1-70B-Instruct', 'M2M-100', 'Multilingual-Transformer-35-layer', 'NLLB-200', 'PaLM-2', 'Qwen2.5-72B-Instruct', 'SeamlessM4T', 'Transformer', 'multilingual-baseline', 'no-models'],
    "Mongolian": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Nepali": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBart', 'mT5', 'various-LLMs'],
    "Norwegian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Norwegian-Bokmal": ['IndicTrans2', 'LibreTranslate', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'mBART', 'mBART50', 'mT5'],
    "Occitan": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Odia": ['IndicTrans2', 'NLLB-200', 'mBART-50', 'mT5', 'various-LLMs'],
    "Oriya": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T'],
    "Oromo": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Pashto": ['M2M-100-various-sizes', 'NLLB-200-family', 'T5', 'XLM-R', 'mBart'],
    "Persian": ['M2M-100-various-sizes', 'NLLB-200-family', 'PaLM-X', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5'],
    "Polish": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Portuguese": ['ChatGPT', 'Claude-3', 'DeepL', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Google-Translate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'Yandex.Translate', 'mBART-50', 'mBERT', 'mBart', 'mT5'],
    "Portuguese-Emakhuwa": ['Various-participant-systems'],
    "Punjabi": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'mT5', 'various-LLMs'],
    "Quechua": ['NLLB-200-family'],
    "Romanian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Russian": ['ChatGPT', 'Claude-3', 'DeepL', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Google-Translate', 'Human-Translators', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Seamless-M4T', 'SeamlessM4T', 'T5', 'XLM-R', 'Yandex.Translate', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Samoan": ['NLLB-200-family'],
    "Sanskrit": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Santali": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Serbian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Sesotho": ['NLLB-200-family'],
    "Shona": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'NLLB-200-family', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Sindhi": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'IndicTrans2', 'M2M-100', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'SeamlessM4T', 'mBART-50', 'mT5', 'various-LLMs'],
    "Sinhala": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Slovak": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Slovenian": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Somali": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART-50', 'mBart', 'various-MT-systems'],
    "South-Azerbaijani": ['LibreTranslate', 'NLLB', 'Opus-MT', 'mBART50'],
    "Spanish": ['Adam-optimizer', 'Claude-3', 'Claude-3.5-Sonnet', 'DeepSeek-V2.5', 'GPT-3.5-turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemini-1.5-Pro', 'Gemma-3-27B', 'IndicTrans2', 'IndicTrans2-baseline', 'Llama-3.1-70B-Instruct', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-Transformer-35-layer', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'Qwen2.5-72B-Instruct', 'SeamlessM4T', 'T5', 'Transformer', 'XLM-R', 'mBERT', 'mBart', 'mT5', 'multilingual-baseline', 'translate-test', 'translate-train'],
    "Standard-Swahili": ['Neural-machine-translation-models', 'cross-dialect-transfer-methods', 'semi-supervised-learning-approaches'],
    "Sundanese": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio'],
    "Swahili": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train', 'various-MT-systems'],
    "Swedish": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBart'],
    "Tagalog": ['ChatGPT-GPT-3.5-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Google', 'MSFT', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBERT', 'mT5'],
    "Tajik": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T'],
    "Tamil": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Telugu": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART-50', 'mBART50', 'mBERT', 'mBart', 'mT5', 'various-LLMs'],
    "Thai": ['ChatGPT-GPT-3.5-4', 'Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Google', 'IndicTrans2', 'LibreTranslate', 'M2M-100', 'M2M-100-various-sizes', 'MSFT', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Tigrinya": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Turkish": ['ChatGPT-GPT-3.5-4', 'Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'Google', 'M2M-100', 'M2M-100-various-sizes', 'MSFT', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Turkmen": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'NLLB-200', 'PaLM-2', 'SeamlessM4T'],
    "Twi": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'NLLB-200', 'Qwen-2-Audio', 'mBART-50', 'various-MT-systems'],
    "Ukrainian": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'IndicTrans2', 'LibreTranslate', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'Qwen-2-Audio', 'T5', 'XLM-R', 'mBART', 'mBART50', 'mBart', 'mT5'],
    "Ukrainian-English": ['AIRC', 'ANVITA', 'CUNI-DOCTRANSFORMER', 'CUNI-GA', 'CUNI-TRANSFORMER', 'GPT4-5SHOT', 'GTCOM', 'HW-TSC', 'IOL-RESEARCH', 'LAN-BRIDGEMT', 'LANGUAGEX', 'MUNI-NLP', 'NAIST-NICT', 'NLLB-GREEDY', 'NLLB-MBR-BLEU', 'ONLINE-A', 'ONLINE-B', 'ONLINE-G', 'ONLINE-M', 'ONLINE-W', 'ONLINE-Y', 'PROMT', 'SKIM', 'SRPH', 'TEAMKYB', 'UPCITE-CLILLF', 'UVA-LTL', 'YISHU'],
    "Urdu": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'IndicTrans2', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBART-50', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train', 'various-LLMs'],
    "Uzbek": ['Claude-3', 'GPT-4', 'Gemini-1.5', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'SeamlessM4T'],
    "Valencian": ['Various-systems'],
    "Vietnamese": ['Claude-3', 'GPT-4', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemini-1.5', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'Machine-Translation-baselines', 'Multilingual-LSTM-encoder', 'Multilingual-bag-of-words-encoder', 'NLLB-200', 'NLLB-200-family', 'PaLM-2', 'PaLM-X', 'Qwen-2-Audio', 'SeamlessM4T', 'T5', 'XLM-R', 'mBERT', 'mBart', 'mT5', 'translate-test', 'translate-train'],
    "Wolof": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'Qwen-2-Audio'],
    "Xhosa": ['IndicTrans2', 'LibreTranslate', 'M2M-100-various-sizes', 'NLLB', 'NLLB-200', 'NLLB-200-family', 'Opus-MT', 'mBART', 'mBART50', 'mT5'],
    "Yiddish": ['NLLB-200-family'],
    "Yoruba": ['AfriCOMET', 'AfroXLM-R', 'COMET', 'GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100', 'M2M-100-various-sizes', 'NLLB-200', 'NLLB-200-family', 'PaLM-X', 'Qwen-2-Audio', 'XLM-R', 'mBART-50', 'mBERT', 'mT5', 'various-MT-systems'],
    "Yoruba-English": ['Facebook-M2M', 'Google', 'neural-MT-models'],
    "Zulu": ['GPT-4o', 'GPT-4o-Audio', 'Gemini-2.0-Flash', 'Gemma-3-27B', 'M2M-100-various-sizes', 'NLLB-200-family', 'Qwen-2-Audio'],
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
    print(f"Task: 06_Machine_Translation")
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

if __name__ == "__main__":
    print_summary()
