"""
Language to Models Mapping for 03_qa_vqa (Reduced Dataset)
Generated from reduced CSV data
Total languages: 79
Total unique models: 159
"""

from collections import Counter

# Language to Models Mapping
# Format: language: [list of models benchmarked on this language]

LANGUAGE_MODELS_MAPPING = {
    "Afrikaans": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Arabic": ['M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'bert', 'mBERT'],
    "Arammba": ['DistilBERT'],
    "Bambara": ['DistilBERT'],
    "Basque": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Bengali": ['BLOOMZ-7B', 'DistilBERT', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'MMTE', 'PaLM-2-L', 'XLM', 'XLM-R', 'mBERT'],
    "Bisu (bzi)": ['DistilBERT'],
    "Bozo": ['DistilBERT'],
    "Bulgarian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Burmese": ['DistilBERT', 'MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Cebuano": ['DistilBERT'],
    "Chinese": ['Claude-3.5 Sonnet', 'DeepSeek-V3 (MoE)', 'GPT-4', 'GPT-4o', 'Gemini 1.5', 'LLaMA 3.1', 'LLaMA-3.1 405B', 'Llama', 'Llava-Llama-3', 'Llava1.5', 'M-BERT', 'MMTE', 'Mistral', 'Qwen 2', 'Qwen-VL-Chat', 'Qwen2.5-72B', 'Unicoder LC', 'X-Llava', 'XLM', 'XLM-R', 'XLM-R base', 'bert', 'mBERT'],
    "Czech": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'c4ai-command-r-35B-v01'],
    "Dangaura Tharu": ['DistilBERT'],
    "Danish": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Dotyali": ['DistilBERT'],
    "Dutch": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "English": ['AgentFly', 'Aquila-VL2', 'Aria-MoE', 'Attention-based soft layer sharing mechanism', 'Aya-23-8B', 'Bi-LSTM', 'Bi-linear attention with residual connection', 'BioMistral', 'Bloom-7b1', 'Bloomz-7b1', 'CNN', 'ChatGPT-4o', 'ChatGPT-o1', 'Claude-3.5 Sonnet', 'Claude-3.5-Sonnet', 'Custom deep CNN-RNN architecture', 'DeepSeek-Janus-1B', 'DeepSeek-Janus-7B', 'DeepSeek-V3 (MoE)', 'DistilBERT', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Faster R-CNN (object-level features)', 'GLM-4.5', 'GPT-3', 'GPT-4', 'GPT-4o', 'GPT-4o-1120', 'Gemini 1.5', 'Gemini-2.0-Flash-Experimental', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Grok-3', 'InternVL-2.5', 'InternVL-2.5-38B', 'InternVL2-8B', 'InternVL3/3.5', 'LLaMA', 'LLaMA 3.1', 'LLaMA-3.1 405B', 'LLaMA-3.2-3B', 'LLaMA2', 'LLaVA-NeXT-7B', 'Llama', 'Llama-3.2-Vision', 'Llama-3.2-Vision-11B', 'Llava-Llama-3', 'Llava1.5', 'LlavaOneVision', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'MiniCPM', 'Mistral', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Mobile-Agent-v3', 'Molmo', 'Multilingual word embeddings', 'OPT (6.7B–30B)', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Ovis-2-16B', 'Ovis-2-34B', 'Ovis-2-8B', 'Ovis1.6-Gemma2', 'Ovis1.6-Gemma2-28B', 'PMC-LLaMA', 'PaliGemma2-ft-docci', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Phi-3.5-vision', 'Pixtral', 'Pixtral-12B', 'QVQ-72B-Preview', 'Qwen 2', 'Qwen-2.5-VL', 'Qwen-VL-Chat', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Qwen2.5-3B', 'Qwen2.5-72B', 'Qwen2.5-VL-72B-Instruct', 'Qwen2.5VL-3B', 'Qwen2.5VL-7B', 'Qwen3 (all configs)', 'ResNet101 (image-level features)', 'Self-attention (multi-head)', 'SmolVLM-500M', 'Tesseract OCR', 'UI-TARS', 'Unicoder LC', 'UnifiedQA (0.7B/3B/11B)', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'X-Llava', 'XLM', 'XLM-R', 'XLM-R base', 'bert', 'c4ai-command-r-35B-v01', 'mBERT', 'mPLUG-DocOwl2-8B', 'mT5', 'rStar2-Agent'],
    "Estonian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Finnish": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "French": ['Aya-23-8B', 'BioMistral', 'Bloom-7b1', 'Bloomz-7b1', 'DistilBERT', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'LLaMA2', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'PMC-LLaMA', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Georgian": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "German": ['Aquila-VL2', 'Aria-MoE', 'Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'Claude-3.5-Sonnet', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'GPT-4o-1120', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'InternVL-2.5', 'InternVL-2.5-38B', 'Llama-3.2-Vision', 'LlavaOneVision', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'MiniCPM', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Molmo', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Ovis-2-16B', 'Ovis-2-34B', 'Ovis-2-8B', 'Ovis1.6-Gemma2', 'Ovis1.6-Gemma2-28B', 'PaliGemma2-ft-docci', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Phi-3.5-vision', 'Pixtral', 'Qwen-2.5-VL', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'bert', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Greek": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Gujarati": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'PaLM-2-L'],
    "Haitian Creole": ['DistilBERT'],
    "Hausa": ['DistilBERT'],
    "Hebrew": ['M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Highland Oaxaca Chontal": ['DistilBERT'],
    "Hindi": ['Attention-based soft layer sharing mechanism', 'Aya-expanse-8b', 'BLOOMZ-7B', 'Bi-LSTM', 'Bi-linear attention with residual connection', 'CNN', 'Custom deep CNN-RNN architecture', 'Faster R-CNN (object-level features)', 'GPT-2 Medium', 'GPT-2 Small', 'GPT-3.5 Turbo', 'GPT-4', 'GPT-4o', 'GPT-OSS-120B', 'Gemma-2-2b-it', 'Gemma-2-9b-it', 'Gemma-3-27b-it', 'Gemma-7B-IT', 'HindiLLM-Medium', 'HindiLLM-Small', 'INLP', 'IndicBERT', 'IndicFT', 'InternVL2-8B', 'Krutrim-spectre-v2', 'LLaMA-3.2-3B', 'LLaMA-65B', 'LLaVA-NeXT-7B', 'Llama-3.1-405B-Instruct', 'Llama-3.1-70B-Instruct', 'Llama-3.1-8B-Instruct', 'Llama-3.2-3B-Instruct', 'Llama-3.2-90B-Vision-Instruct', 'Llama-3.2-Vision-11B', 'M-BERT', 'MMTE', 'Mistral-7B-Instruct-v0.2', 'Multilingual word embeddings', 'Nemotron-4-Mini-Hindi-4B-Instruct', 'Nemotron-Mini-4B-Instruct', 'OpenHermes-2.5-Mistral-7B', 'PaLM-2-L', 'Qwen2.5-3B', 'Qwen2.5-72B-Instruct', 'Qwen2.5VL-3B', 'Qwen2.5VL-7B', 'ResNet101 (image-level features)', 'Sarvam-2B-Hindi-v0.5', 'Self-attention (multi-head)', 'SmolVLM-500M', 'Tesseract OCR', 'Unicoder LC', 'Wiki+CommonCrawl FT-WC', 'Wikipedia FT-W', 'XLM', 'XLM-R', 'XLM-R base', 'XLM-RoBERTa', 'bert', 'iNLTK', 'mBERT', 'mPLUG-DocOwl2-8B'],
    "Hinglish (code-mixed)": ['Attention-based soft layer sharing mechanism', 'Bi-LSTM', 'Bi-linear attention with residual connection', 'CNN', 'Faster R-CNN (object-level features)', 'Multilingual word embeddings', 'ResNet101 (image-level features)', 'Self-attention (multi-head)'],
    "Huba": ['DistilBERT'],
    "Hungarian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Indonesian": ['DistilBERT', 'M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Italian": ['AgentFly', 'Aya-23-8B', 'BioMistral', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'GLM-4.5', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'InternVL3/3.5', 'LLaMA2', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Mobile-Agent-v3', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'PMC-LLaMA', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Qwen3 (all configs)', 'UI-TARS', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT', 'rStar2-Agent'],
    "Japanese": ['GPT-4', 'GPT-4o', 'Gemini 1.5', 'LLaMA 3.1', 'M-BERT', 'MMTE', 'Qwen 2', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Jarai": ['DistilBERT'],
    "Javanese": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "K'iche'": ['DistilBERT'],
    "Kagayanen": ['DistilBERT'],
    "Kairak": ['DistilBERT'],
    "Kannada": ['BLOOMZ-7B', 'DistilBERT', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'PaLM-2-L'],
    "Kaqchikel": ['DistilBERT'],
    "Kazakh": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Korean": ['DistilBERT', 'GPT-4', 'GPT-4o', 'Gemini 1.5', 'LLaMA 3.1', 'Llama', 'Llava-Llama-3', 'Llava1.5', 'M-BERT', 'MMTE', 'Qwen 2', 'Qwen-VL-Chat', 'Unicoder LC', 'X-Llava', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Kyrgyz": ['DistilBERT'],
    "Latvian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'c4ai-command-r-35B-v01'],
    "Lithuanian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'c4ai-command-r-35B-v01'],
    "Malay": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Malayalam": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'MMTE', 'PaLM-2-L', 'XLM', 'XLM-R', 'mBERT'],
    "Mam": ['DistilBERT'],
    "Mamara Senoufo": ['DistilBERT'],
    "Marathi": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'MMTE', 'PaLM-2-L', 'XLM', 'XLM-R', 'mBERT'],
    "Maru": ['DistilBERT'],
    "Nepali": ['BLOOMZ-7B', 'DistilBERT', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'PaLM-2-L'],
    "Newari": ['DistilBERT'],
    "Persian": ['DistilBERT', 'MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Polish": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Portuguese": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'DistilBERT', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Punjabi": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'PaLM-2-L'],
    "Q'anjob'al": ['DistilBERT'],
    "Q'eqchi'": ['DistilBERT'],
    "Romanian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'c4ai-command-r-35B-v01'],
    "Russian": ['DistilBERT', 'M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Slovak": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'c4ai-command-r-35B-v01'],
    "Slovenian": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'c4ai-command-r-35B-v01'],
    "Soninke": ['DistilBERT'],
    "Sos Kundi": ['DistilBERT'],
    "Spanish": ['Aya-23-8B', 'BioMistral', 'Bloom-7b1', 'Bloomz-7b1', 'DistilBERT', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'LLaMA2', 'M-BERT', 'MMTE', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'PMC-LLaMA', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R', 'XLM-R base', 'bert', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Swahili": ['M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Swedish": ['Aya-23-8B', 'Bloom-7b1', 'Bloomz-7b1', 'EuroLLM-1.7B', 'EuroLLM-1.7B-Instruct', 'Gemma-1.1-7b-Instruct', 'Gemma-2-27b-Instruct', 'Gemma-2-9b-Instruct', 'Gemma-7b', 'M-BERT', 'Meta-Llama-2-13B-Chat', 'Meta-Llama-2-7B', 'Meta-Llama-2-7B-Chat', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-Instruct', 'Meta-Llama-3.1-70B-Instruct', 'Meta-Llama-3.1-8B', 'Meta-Llama-3.1-8B-Instruct', 'Mistral-7B-Instruct-v0.1', 'Mistral-7B-Instruct-v0.2', 'Mistral-7B-Instruct-v0.3', 'Mistral-7B-v0.1', 'Mistral-7B-v0.3', 'Mistral-NeMo-Minitron-8B-Base', 'Mistral-Nemo-Base-12.2B', 'Mistral-Nemo-Instruct-12.2B', 'Mixtral-8x7B-Instruct-v0.1', 'Mixtral-8x7B-v0.1', 'Occiglot-7b-eu5', 'Occiglot-7b-eu5-Instruct', 'Pharia-1-LLM-7B-control', 'Pharia-1-LLM-7B-control-aligned', 'Phi-3-medium-14B-128k-Instruct', 'Phi-3-medium-14B-4k-Instruct', 'Phi-3-mini-3.8B-128k-Instruct', 'Phi-3-mini-4k-Instruct', 'Qwen2-7B', 'Qwen2-7B-Instruct', 'Unicoder LC', 'Vicuna-13b-v1.5', 'Vicuna-33b-v1.3', 'XLM', 'XLM-R base', 'c4ai-command-r-35B-v01', 'mBERT'],
    "Tagalog": ['DistilBERT', 'MMTE', 'XLM', 'XLM-R', 'mBERT'],
    "Tamil": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'MMTE', 'PaLM-2-L', 'XLM', 'XLM-R', 'mBERT'],
    "Telugu": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'MMTE', 'PaLM-2-L', 'XLM', 'XLM-R', 'mBERT'],
    "Thai": ['DistilBERT', 'M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Turkish": ['M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'mBERT'],
    "Urdu": ['BLOOMZ-7B', 'GPT-4', 'Gemma-7B-IT', 'LLaMA-65B', 'M-BERT', 'MMTE', 'PaLM-2-L', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'XLM-RoBERTa-XL', 'mBERT', 'mT5'],
    "Vietnamese": ['M-BERT', 'MMTE', 'Unicoder LC', 'XLM', 'XLM-R', 'XLM-R base', 'bert', 'mBERT'],
    "Yoruba": ['MMTE', 'XLM', 'XLM-R', 'mBERT'],
}

# Statistics
TOTAL_LANGUAGES = 79
TOTAL_UNIQUE_MODELS = 159

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
    print(f"Task: 03_qa_vqa (Reduced Dataset)")
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
