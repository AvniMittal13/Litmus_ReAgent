"""
Language to Models Mapping for 04_classification_nli (Reduced Dataset)
Generated from reduced CSV data
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Akan": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Algerian Arabic": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base'],
    "Amharic": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Arabic": ['BERT', 'BERT-Large', 'BERTimbau', 'C4AI Command R+', 'FLAN-T5', 'GPT-4', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'ML Ensemble', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-R Base', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'mMiniLM-L12xH384', 'machine-translation based baseline', 'multilingual BERT', 'norBERT'],
    "Assamese": ['AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama2', 'Mistral', 'MuRIL', 'PaLM-2', 'Sarvam 1', 'Tamil-Llama', 'XLM-R', 'XLM-RoBERTa', 'mBERT', 'mT5'],
    "Bambara": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Bemba": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Bengali": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'Bangla BERT Base', 'BanglaBERT', 'BongLLaMA', 'BongLLaMA-3B', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'DistilBERT', 'GPT-3.5', 'GPT-3.5 Turbo', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'GeminiPro', 'Gemma', 'Gemma-2-2B', 'IndicBART', 'IndicBERT', 'LLaMA-3.1-8B', 'LLaMA-3.1-70B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'Llama', 'Llama-3.2-1B', 'Llama-3.2-3B', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'Mistral-7B', 'Mistral-Small-24B', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'Phi', 'Qwen', 'Qwen-2.5-1.5B', 'Qwen-2.5-7B', 'Qwen-2.5-72B', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'TituLLM-1B', 'TituLLM-3B', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sahajBERT', 'sequence-to-sequence models'],
    "Bulgarian": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'Unicoder', 'XLM', 'XLM-R', 'mBERT'],
    "Burmese": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Chichewa": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Chinese": ['ALBERT-base', 'ALBERT-large', 'ALBERT-tiny', 'ALBERT-xlarge', 'ALBERT-xxlarge', 'ALBERT?tiny', 'ALBERT?xxlarge', 'BERT', 'BERT-base', 'BERT-wwm-ext', 'BERT?base', 'BERT?wwm?ext?base', 'BERTimbau', 'BOW', 'Baichuan2-13b-Chat', 'Baichuan2-7b-Base', 'Baichuan2-7b-Chat', 'Bloomz-mt-176B', 'ChatGLM-6B', 'ChatGLM-6b', 'ChatGLM2-6b', 'ChatGPT', 'Chinese-Alpaca-13B', 'Chinese-LLaMA-13B', 'Chinese-LLaVA', 'Claude-instant-v1.0', 'Claude-v1.3', 'CogAgent-Chat', 'ERNIE-Bot-0615', 'ERNIE-Bot-turbo-0725', 'ERNIE-base', 'ERNIE?base', 'ESIM', 'Emu2-Chat', 'FLAN-T5', 'GLM-130B', 'GPT-3.5-turbo-0301', 'GPT-4', 'GPT-4-0314', 'GPT-4-0613', 'GPT-4V', 'Gemini-Pro', 'InternVL-Chat-V1.1', 'InternVL-Chat-ViT-6B-Vicuna-13B', 'InternVL-Chat-ViT-6B-Vicuna-7B', 'LLaMA-65B', 'LLaMA-7b', 'ML Ensemble', 'MOSS', 'Qwen-VL-7B-Chat', 'Qwen-VL-PLUS', 'RoBERTa', 'RoBERTa-large', 'RoBERTa-wwm-ext', 'RoBERTa-wwm-large', 'RoBERTa?large', 'RoBERTa?wwm?ext?base', 'RoBERTa?wwm?ext?large', 'SPHINX-MoE', 'Unicoder', 'Vicuna-7b', 'VisCPM', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'XLNet-mid', 'XLNet?mid', 'Yi-VL-34B', 'Yi-VL-6B', 'italianBERT', 'mBERT', 'mBert', 'mPLUG-OWL2', 'multilingual BERT', 'norBERT', 'random models'],
    "Chokwe": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Czech": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Dutch": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'Unicoder', 'XLM', 'XLM-R', 'mBERT'],
    "Dyula": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Egyptian Arabic": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "English": ['Airavata', 'BERT', 'BERT-Large', 'BERTimbau', 'BOW', 'Baichuan2-13b-Chat', 'Baichuan2-7b-Base', 'Baichuan2-7b-Chat', 'C4AI Command R+', 'ChatGLM-6b', 'ChatGLM2-6b', 'ChatGPT 3.5/4', 'DeepSeek-R1-14B', 'DeepSeek-R1-70B', 'ERNIE-Bot-0615', 'ERNIE-Bot-turbo-0725', 'ESIM', 'FLAN-T5', 'GPT-3.5-turbo-0301', 'GPT-4', 'GPT-4-0314', 'GPT-4-0613', 'GPT-4o', 'GPT-4o-mini', 'Gemini Pro', 'Gemini-Pro', 'IndicBART', 'IndicBERT', 'LLaMA-3.1-8B', 'LLaMA-3.1-70B', 'LLaMA-3.2-3B', 'LLaMA-3.3-70B', 'LLaMA-7b', 'LLaMA2-7B', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Llama-3.1-8B-Instruct', 'ML Ensemble', 'MahaMarathi', 'Mistral-7B', 'Mistral Large', 'Mistral-Small-24B', 'Mistral-v3-7B', 'MuRIL', 'Navarasa', 'OpenHathi', 'Qwen-2.5-7B', 'Qwen-2.5-72B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RemBERT', 'RoBERTa', 'TamilLlama', 'Unicoder', 'Vicuna-7b', 'XLM', 'XLM-R', 'XLM-R Base', 'XLM-RoBERTa', 'instruction-tuned models', 'italianBERT', 'mBERT', 'mBert', 'mMiniLM-L12xH384', 'machine-translation based baseline', 'multilingual BERT', 'multilingual BERT variants', 'norBERT', 'random models', 'sequence-to-sequence models'],
    "Ewe": ['AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Fon": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Fongbe": ['AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "French": ['BERT', 'BERTimbau', 'BOW', 'C4AI Command R+', 'ChatGPT 3.5/4', 'ESIM', 'FLAN-T5', 'GPT-4', 'Gemini Pro', 'LLaMA2-7B', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'ML Ensemble', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'mBert', 'multilingual BERT', 'norBERT', 'random models'],
    "German": ['BERT', 'BERT-Large', 'BERTimbau', 'BOW', 'C4AI Command R+', 'ChatGPT 3.5/4', 'ESIM', 'FLAN-T5', 'GPT-4', 'Gemini Pro', 'LLaMA2-7B', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'ML Ensemble', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-R Base', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'mBert', 'mMiniLM-L12xH384', 'machine-translation based baseline', 'multilingual BERT', 'norBERT', 'random models'],
    "Ghomálá'": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Greek": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'Unicoder', 'XLM', 'XLM-R', 'mBERT'],
    "Gujarati": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Hausa": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Hindi": ['Airavata', 'AryaBhatta', 'BERT', 'BERT-Large', 'BERTimbau', 'BLOOMZ', 'C4AI Command R+', 'FLAN-T5', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Llama-3.1-8B-Instruct', 'Llama2', 'ML Ensemble', 'MahaMarathi', 'Mistral', 'Mistral Large', 'Mistral-v3-7B', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RemBERT', 'RoBERTa', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'Unicoder', 'XLM', 'XLM-R', 'XLM-R Base', 'XLM-RoBERTa', 'instruction-tuned models', 'italianBERT', 'mBERT', 'mMiniLM-L12xH384', 'mT5', 'machine-translation based baseline', 'multilingual BERT', 'multilingual BERT variants', 'norBERT', 'sequence-to-sequence models'],
    "Hungarian": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Igbo": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Italian": ['BERT', 'BERTimbau', 'ChatGPT 3.5/4', 'FLAN-T5', 'GPT-4', 'Gemini Pro', 'LLaMA2 7B', 'ML Ensemble', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'norBERT', 'random models'],
    "Japanese": ['BERT', 'BERTimbau', 'BOW', 'ChatGPT 3.5/4', 'ESIM', 'FLAN-T5', 'GPT-4', 'Gemini Pro', 'LLaMA2 7B', 'ML Ensemble', 'RoBERTa', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'mBert', 'multilingual BERT', 'norBERT', 'random models'],
    "Kabiyè": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Kabyle": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Kamba": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Kannada": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Kikongo": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Kikuyu": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Kimbundu": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Kinyarwanda": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Korean": ['BERT', 'BERTimbau', 'BOW', 'C4AI Command R+', 'ESIM', 'FLAN-T5', 'GPT-4', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'ML Ensemble', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RoBERTa', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'mBert', 'multilingual BERT', 'norBERT'],
    "Lingala": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Luba-Kasai": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Luganda": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Lugbara": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Luo": ['AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Malay": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Malayalam": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Mandarin Chinese": ['ChatGPT 3.5/4', 'Gemini Pro', 'LLaMA2 7B'],
    "Marathi": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Moroccan Arabic": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base'],
    "Mossi": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Mozambican Portuguese": ['AfriBERTa-large', 'AfroXLMR-base', 'AfroXLMR-large', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base'],
    "Nigerian Fulfulde": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Nigerian Pidgin": ['AfriBERTa-large', 'AfroXLMR-base', 'AfroXLMR-large', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base'],
    "Northern Sotho": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Norwegian": ['BERT', 'BERTimbau', 'FLAN-T5', 'GPT-4', 'ML Ensemble', 'RoBERTa', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'norBERT'],
    "Nyanja": ['AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "N'Ko": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Odia": ['AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama2', 'Mistral', 'MuRIL', 'PaLM-2', 'Sarvam 1', 'Tamil-Llama', 'XLM-R', 'XLM-RoBERTa', 'mBERT', 'mT5'],
    "Oromo": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Polish": ['C4AI Command R+', 'ChatGPT 3.5/4', 'Gemini Pro', 'LLaMA2-7B', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'Unicoder', 'XLM', 'XLM-R', 'mBERT'],
    "Portuguese": ['BERT', 'BERTimbau', 'C4AI Command R+', 'ChatGPT 3.5/4', 'FLAN-T5', 'GPT-4', 'Gemini Pro', 'LLaMA2-7B', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'ML Ensemble', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'norBERT'],
    "Punjabi": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Romanian": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Rundi.": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Russian": ['ChatGPT 3.5/4', 'Gemini Pro', 'LLaMA2 7B', 'Unicoder', 'XLM', 'XLM-R', 'mBERT', 'random models'],
    "Serbo-Croatian": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Shona": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Simplified Chinese": ['BERT-Large', 'XLM', 'XLM-R Base', 'mMiniLM-L12xH384', 'machine-translation based baseline', 'multilingual BERT'],
    "Slovak": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B'],
    "Somali": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Spanish": ['BERT', 'BERT-Large', 'BERTimbau', 'BOW', 'C4AI Command R+', 'ChatGPT 3.5/4', 'ESIM', 'FLAN-T5', 'GPT-4', 'Gemini Pro', 'LLaMA2-7B', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'ML Ensemble', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-R Base', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'mBert', 'mMiniLM-L12xH384', 'machine-translation based baseline', 'multilingual BERT', 'norBERT', 'random models'],
    "Swahili": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'Unicoder', 'XLM', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mBERT', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Tamasheq": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Tamazight": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Tamil": ['Airavata', 'AryaBhatta', 'BLOOMZ', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'mT5', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Telugu": ['Airavata', 'AryaBhatta', 'BERT', 'BERTimbau', 'BLOOMZ', 'FLAN-T5', 'GPT-3.5', 'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GeminiPro', 'Gemma', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'Llama2', 'ML Ensemble', 'MahaMarathi', 'Mistral', 'MuRIL', 'Navarasa', 'OpenHathi', 'PaLM-2', 'RemBERT', 'RoBERTa', 'Sarvam 1', 'Tamil-Llama', 'TamilLlama', 'TeBERT', 'XLM-R', 'XLM-RoBERTa', 'facebook/bart-large-mnli', 'instruction-tuned models', 'italianBERT', 'mBERT', 'mT5', 'multilingual BERT variants', 'norBERT', 'sequence-to-sequence models'],
    "Thai": ['C4AI Command R+', 'Llama-3.1-Instruct-70B', 'Llama-3.1-Instruct-8B', 'Mistral Large', 'Mistral-v3-7B', 'Qwen-2.5-Instruct-7B', 'Qwen-2.5-Instruct-72B', 'Unicoder', 'XLM', 'XLM-R', 'mBERT'],
    "Tigrinya": ['AfriBERTa-large', 'AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Tunisian Arabic": ['AfroLLaMA', 'Aya-101', 'GPT-4o', 'Gemini-1.5-Pro', 'Gemma-2', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B'],
    "Turkish": ['BERT', 'BERTimbau', 'FLAN-T5', 'GPT-4', 'ML Ensemble', 'RoBERTa', 'Unicoder', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'italianBERT', 'mBERT', 'norBERT'],
    "Twi": ['AfriBERTa-large', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Urdu": ['Airavata', 'GPT-4o', 'GPT-4o-mini', 'IndicBART', 'IndicBERT', 'Llama-3.1-8B-Instruct', 'MahaMarathi', 'MuRIL', 'Navarasa', 'OpenHathi', 'RemBERT', 'TamilLlama', 'Unicoder', 'XLM', 'XLM-R', 'XLM-RoBERTa', 'instruction-tuned models', 'mBERT', 'multilingual BERT variants', 'sequence-to-sequence models'],
    "Vietnamese": ['BERT-Large', 'Unicoder', 'XLM', 'XLM-R', 'XLM-R Base', 'mBERT', 'mMiniLM-L12xH384', 'machine-translation based baseline', 'multilingual BERT'],
    "Wolof": ['AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Xhosa": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
    "Xitsonga": ['AfriBERTa-large', 'AfroXLMR-base', 'AfroXLMR-large', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base'],
    "Yoruba": ['AfriBERTa-large', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'XLM-R-base', 'XLM-R-large', 'XLM-T-base', 'mDeBERTaV3-base', 'mT0-XXL-MT'],
    "Zulu": ['AfroLLaMA', 'AfroXLMR-76L', 'AfroXLMR-base', 'AfroXLMR-large', 'Aya-101', 'BLOOMZ-7B', 'Claude OPUS', 'Command-R (August version)', 'GPT-3.5-Turbo', 'GPT-4-Turbo', 'GPT-4o', 'GPT-4o-08-06', 'GPT-4o-mini', 'Gemini-1.5-Pro', 'Gemini-1.5-Pro', 'Gemma-2', 'Gemma-2-27B', 'Gemma-2-9B', 'LLaMA-3.1-70B', 'LLaMA-3.1-8B', 'LLaMa-3-8B', 'LLaMa-3.1-70B', 'LLaMa-3.1-8B', 'LLaMaX-3-8B', 'Serengeti', 'XLM-R', 'mT0-XXL-MT'],
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
    print(f"Task: 04_classification_nli (Reduced Dataset)")
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
