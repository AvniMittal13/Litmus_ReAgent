"""Utilities for normalizing text and metric names"""
import re
import string


def normalize_metric_name_v2(metric: str) -> str:
    """Normalize metric name with specific rules.
    
    Normalization rules:
    - All containing 'accuracy' -> 'accuracy'
    - All containing 'rouge' -> 'rouge'
    - All containing 'bleu' -> 'bleu'
    - All containing 'correlation' -> 'correlation'
    - All containing 'COMET' -> 'comet'
    - All containing 'chrF' -> 'chrF'
    - 'pass@1' -> 'accuracy'
    
    Args:
        metric: Raw metric name
        
    Returns:
        Normalized metric name
    """
    if not metric:
        return ""
    
    metric_lower = metric.lower().strip()
    
    # Apply normalization rules
    if 'pass@1' in metric_lower or 'pass@k' in metric_lower or "f1" in metric_lower:
        return 'accuracy'
    elif 'accuracy' in metric_lower or 'acc' in metric_lower:
        return 'accuracy'
    elif 'average language performance' in metric_lower:
        return 'rouge'
    elif 'rouge' in metric_lower:
        return 'rouge'
    elif 'bleu' in metric_lower:
        return 'bleu'
    elif 'correlation' in metric_lower:
        return 'correlation'
    elif 'comet' in metric_lower:
        return 'comet'
    elif 'chrf' in metric_lower:
        return 'chrF'
    else:
        # Keep original metric name, just normalize spacing
        normalized = re.sub(r'\s+', ' ', metric.strip())
        return normalized


def normalize_metric_name(metric: str) -> str:
    """Normalize metric name for comparison (legacy function).
    
    Args:
        metric: Raw metric name
        
    Returns:
        Normalized metric name (lowercase, no special chars)
    """
    if not metric:
        return ""
    
    # Convert to lowercase
    normalized = metric.lower().strip()
    
    # Remove special characters except @ (for pass@1)
    normalized = re.sub(r'[^\w\s@]', '', normalized)
    
    # Replace multiple spaces with single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Remove spaces around @
    normalized = re.sub(r'\s*@\s*', '@', normalized)
    
    return normalized


def normalize_answer_text(answer: str) -> str:
    """Normalize answer text for exact match comparison.
    
    Args:
        answer: Raw answer text
        
    Returns:
        Normalized answer text
    """
    if not answer:
        return ""
    
    # Convert to lowercase
    normalized = answer.lower().strip()
    
    # Remove punctuation
    normalized = normalized.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized


# Concept synonyms for domain-specific normalization
# Maps canonical term -> list of variations (all lowercase, no punctuation)
CONCEPT_SYNONYMS = {
    # Data-related
    'data scarcity': ['limited corpora', 'sparse data', 'lack of data', 'small dataset', 
                      'limited parallel', 'insufficient data', 'low resource', 'scarce data',
                      'data shortage', 'limited data', 'few examples', 'limited training data'],
    'data quality': ['noisy data', 'dirty data', 'quality issues', 'annotation errors', 
                     'labeling errors', 'label noise', 'data noise'],
    'parallel data': ['parallel corpora', 'aligned data', 'bitext', 'translation pairs',
                      'parallel corpus', 'bilingual data', 'parallel text'],
    'monolingual data': ['monolingual corpora', 'unlabeled data', 'monolingual corpus',
                         'unannotated data', 'raw text'],
    
    # Model-related
    'model absence': ['no model', 'missing model', 'unavailable model', 'lack of model',
                      'model unavailability', 'no available model', 'absent model'],
    'model limitations': ['model constraints', 'model weakness', 'performance limitations',
                          'model deficiency', 'capability limitations'],
    
    # Tokenization
    'tokenization': ['tokenizer', 'subword', 'bpe', 'wordpiece', 'sentencepiece', 
                     'segmentation', 'tokenization inefficiency', 'tokenizer absence',
                     'word segmentation', 'text segmentation'],
    
    # Translation approaches
    'pivot translation': ['pivot via', 'indirect translation', 'bridge language', 
                          'intermediary language', 'russian pivot', 'english pivot',
                          'pivot method', 'pivot approach', 'triangulation'],
    'transfer learning': ['cross lingual transfer', 'multilingual transfer', 'zero shot transfer',
                          'language transfer', 'crosslingual', 'knowledge transfer'],
    'back translation': ['backtranslation', 'reverse translation', 'round trip translation'],
    
    # Techniques
    'fine tuning': ['finetuning', 'fine tuning', 'adaptation', 'domain adaptation',
                    'task adaptation', 'model adaptation'],
    'data augmentation': ['augmentation', 'paraphrase', 'synthetic data',
                          'data synthesis', 'augmented data'],
    'prompt engineering': ['prompting', 'in context learning', 'few shot', 'zero shot',
                           'prompt tuning', 'prompt design'],
    
    # Evaluation/Error terms
    'errors': ['mismatch', 'error', 'mistakes', 'inaccuracy', 'disambiguation', 
               'ambiguity', 'incorrect', 'wrong', 'failure'],
    'low performance': ['poor performance', 'degradation', 'performance drop', 'decline',
                        'underperform', 'low accuracy', 'poor accuracy', 'weak performance'],
    
    # Challenges
    'linguistic distance': ['language distance', 'typological distance', 'language dissimilarity',
                            'distant languages', 'unrelated languages'],
    'vocabulary mismatch': ['vocab mismatch', 'lexical mismatch', 'word mismatch',
                            'vocabulary overlap', 'lexical overlap', 'oov', 'out of vocabulary'],
    'script difference': ['different script', 'script mismatch', 'writing system',
                          'orthographic difference', 'alphabet difference'],
    
    # Resources
    'dictionary': ['lexicon', 'wordlist', 'word list', 'glossary', 'vocabulary list',
                   'bilingual dictionary', 'manual dictionary'],
    'religious texts': ['bible', 'quran', 'religious corpus', 'scripture', 'religious data'],
}

# Word-level synonyms: maps variations to canonical word
# Each word in text is replaced individually
WORD_SYNONYMS = {
    # Language/Linguistic
    'language': ['linguistic', 'lingual', 'multilingual', 'crosslingual', 'monolingual'],
    
    # Error/Problem terms
    'error': ['errors', 'discrepancy', 'discrepancies', 'mismatch', 'mismatches', 
              'mistake', 'mistakes', 'issue', 'issues', 'problem', 'problems',
              'inconsistency', 'inconsistencies', 'ambiguity', 'ambiguities'],
    
    # Scarcity/Lack terms
    'scarcity': ['shortage', 'lack', 'absence', 'insufficient', 'limited', 'sparse',
                 'scarce', 'unavailable', 'missing', 'deficiency'],
    
    # Data terms
    'data': ['dataset', 'datasets', 'corpora', 'corpus', 'resource', 'resources'],
    
    # Model terms
    'model': ['models', 'system', 'systems', 'architecture', 'architectures'],
    
    # Performance terms
    'performance': ['accuracy', 'quality', 'effectiveness', 'capability'],
    'low': ['poor', 'weak', 'bad', 'degraded', 'limited'],
    'high': ['good', 'strong', 'excellent', 'improved'],
    
    # Transfer terms
    'transfer': ['adaptation', 'adapt', 'translate', 'convert', 'transform'],
    
    # Tokenization terms  
    'tokenization': ['tokenizer', 'tokenizers', 'segmentation', 'segmenter'],
    
    # Training terms
    'training': ['finetuning', 'tuning', 'learning', 'optimization'],
    
    # Vocabulary terms
    'vocabulary': ['vocab', 'lexicon', 'lexical', 'dictionary', 'wordlist'],
    
    # Script/Writing terms
    'script': ['orthography', 'orthographic', 'writing', 'alphabet'],
    
    # Parallel/Aligned terms
    'parallel': ['aligned', 'bitext', 'bilingual'],
}


def normalize_word(word: str) -> str:
    """Normalize a single word using word synonyms.
    
    Args:
        word: Single word (lowercase, no punctuation)
        
    Returns:
        Canonical form of the word
    """
    if not word:
        return word
    
    for canonical, synonyms in WORD_SYNONYMS.items():
        if word == canonical or word in synonyms:
            return canonical
    
    return word


def normalize_concept(text: str) -> str:
    """Normalize text by replacing synonym words with canonical terms.
    
    First applies word-level normalization, then phrase-level.
    
    Args:
        text: Normalized text (lowercase, no punctuation)
        
    Returns:
        Text with synonyms replaced by canonical terms
    """
    if not text:
        return text
    
    # Step 1: Word-level normalization
    words = text.split()
    normalized_words = [normalize_word(w) for w in words]
    result = ' '.join(normalized_words)
    
    # Step 2: Phrase-level normalization (for multi-word concepts)
    for canonical, synonyms in CONCEPT_SYNONYMS.items():
        for synonym in synonyms:
            if synonym in result:
                result = result.replace(synonym, canonical)
    
    return result


def split_comma_separated(text: str) -> list:
    """Split comma-separated values and normalize each.
    
    Args:
        text: Comma-separated text
        
    Returns:
        List of normalized values (with concept normalization)
    """
    if not text:
        return []
    
    parts = [p.strip() for p in text.split(',')]
    # Apply both text normalization and concept normalization
    normalized = []
    for p in parts:
        if p:
            norm_text = normalize_answer_text(p)
            norm_concept = normalize_concept(norm_text)
            normalized.append(norm_concept)
    return normalized


# Common model name aliases for fuzzy matching
MODEL_ALIASES = {
    'gpt4': ['gpt-4', 'gpt 4', 'chatgpt4', 'chatgpt-4', 'openai gpt4'],
    'gpt35': ['gpt-3.5', 'gpt 3.5', 'chatgpt35', 'chatgpt-3.5-turbo', 'gpt35turbo'],
    'claude': ['claude-3', 'claude3', 'anthropic claude'],
    'llama': ['llama2', 'llama-2', 'llama 2', 'meta llama'],
    'bloom': ['bloomz', 'bigscience bloom'],
    'mt5': ['mt5 xxl', 'mt5xxl', 'google mt5'],
    'palm': ['palm2', 'palm-2', 'google palm'],
    'gemini': ['google gemini', 'gemini pro'],
}


def normalize_model_name(name: str) -> str:
    """Normalize model name for fuzzy matching.
    
    Removes version numbers, hyphens, and common suffixes.
    """
    if not name:
        return ""
    
    normalized = name.lower().strip()
    # Remove punctuation except hyphens initially
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    # Remove common suffixes
    for suffix in ['instruct', 'chat', 'turbo', 'latest', 'dpo', 'rl', 'base']:
        normalized = re.sub(rf'\b{suffix}\b', '', normalized)
    # Remove numbers at end (version numbers)
    normalized = re.sub(r'\d+[bB]?\s*$', '', normalized)
    # Remove hyphens and extra spaces
    normalized = re.sub(r'[-\s]+', '', normalized)
    return normalized.strip()


def fuzzy_match_model(pred: str, gt: str) -> bool:
    """Check if model names match with fuzzy logic.
    
    Handles variations like GPT-4 vs GPT4 vs ChatGPT-4.
    """
    pred_norm = normalize_model_name(pred)
    gt_norm = normalize_model_name(gt)
    
    if not pred_norm or not gt_norm:
        return False
    
    # Direct match after normalization
    if pred_norm == gt_norm:
        return True
    
    # Check containment
    if pred_norm in gt_norm or gt_norm in pred_norm:
        return True
    
    # Check aliases
    for canonical, aliases in MODEL_ALIASES.items():
        all_forms = [canonical] + [normalize_model_name(a) for a in aliases]
        if pred_norm in all_forms and gt_norm in all_forms:
            return True
        # Check if either matches any alias
        for form in all_forms:
            if form in pred_norm or pred_norm in form:
                if form in gt_norm or gt_norm in form:
                    return True
    
    return False


def fuzzy_match_language(pred: str, gt: str) -> bool:
    """Check if language names match with fuzzy logic."""
    pred_norm = normalize_answer_text(pred)
    gt_norm = normalize_answer_text(gt)
    
    if not pred_norm or not gt_norm:
        return False
    
    # Direct match
    if pred_norm == gt_norm:
        return True
    
    # Containment
    if pred_norm in gt_norm or gt_norm in pred_norm:
        return True
    
    return False


# Lazy-loaded sentence transformer model for semantic matching
_semantic_model = None

def get_semantic_model():
    """Lazy load sentence transformer model."""
    global _semantic_model
    if _semantic_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("Loaded semantic similarity model: all-MiniLM-L6-v2")
        except ImportError:
            print("Warning: sentence-transformers not installed. Semantic matching disabled.")
            _semantic_model = False  # Mark as unavailable
    return _semantic_model


def semantic_similarity_match(pred_values: list, gt_values: list, threshold: float = 0.95) -> dict:
    """Check semantic similarity between pred and gt value lists.
    
    Args:
        pred_values: List of predicted values (normalized strings)
        gt_values: List of ground truth values (normalized strings)
        threshold: Cosine similarity threshold for match (default 0.95)
        
    Returns:
        Dict with matched indices and scores
    """
    model = get_semantic_model()
    
    if model is False or not pred_values or not gt_values:
        return {'matched_gt': set(), 'matched_pred': set(), 'match_pairs': []}
    
    try:
        from sentence_transformers import util
        
        # Encode all values
        pred_embeddings = model.encode(pred_values, convert_to_tensor=True)
        gt_embeddings = model.encode(gt_values, convert_to_tensor=True)
        
        # Compute cosine similarity matrix
        sim_matrix = util.cos_sim(pred_embeddings, gt_embeddings)
        
        matched_gt = set()
        matched_pred = set()
        match_pairs = []
        
        # Find matches above threshold (greedy matching)
        for i, pred_val in enumerate(pred_values):
            if i in matched_pred:
                continue
            for j, gt_val in enumerate(gt_values):
                if j in matched_gt:
                    continue
                similarity = sim_matrix[i][j].item()
                if similarity >= threshold:
                    matched_gt.add(j)
                    matched_pred.add(i)
                    match_pairs.append({
                        'pred': pred_val,
                        'gt': gt_val,
                        'similarity': round(similarity, 4)
                    })
                    break
        
        return {
            'matched_gt': matched_gt,
            'matched_pred': matched_pred,
            'match_pairs': match_pairs
        }
        
    except Exception as e:
        print(f"Semantic matching error: {e}")
        return {'matched_gt': set(), 'matched_pred': set(), 'match_pairs': []}
