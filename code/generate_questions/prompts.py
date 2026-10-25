"""
Prompt templates for question generation.
Contains both common prompt and scenario-specific prompts.
"""

# =============================================================================
# COMMON PROMPT (Recommended - for exact answer benchmarks)
# =============================================================================

COMMON_PROMPT = """
You are given a language-to-models mapping for a specific NLP task where ground truth benchmark data is available.

Task: {task_name}
Language-Model Mappings: {mappings}

---

### Goal

Generate benchmark evaluation questions that have **EXACT, SINGULAR answers** from the ground truth data.
Focus on **low-resource languages** when available in the mapping.

### Question Categories

#### Category 1: PREDICTIVE Questions (Numerical Answer)
Questions where the answer is ONE numerical score/value.

Templates:
- "What is the performance of {{model}} on {{task}} for {{language}}?"
- "What score does {{model}} achieve for {{task}} in {{language}}?"
- "How well does {{model}} perform on {{task}} for {{language}}?"

Examples:
- "What is the performance of GPT-4 on Code Generation for Hindi?"
- "What score does LLaMA-3 achieve for Machine Translation in Bengali?"

#### Category 2: QnA Questions (Single Categorical Answer)  
Questions where the answer is ONE exact model name or language name.

Templates:
- "Which model performs best for {{task}} in {{language}}?"
- "What is the top-performing model for {{task}} in {{language}}?"
- "For {{task}}, which language shows the best performance with {{model}}?"
- "Which model achieves the highest score for {{task}} in {{language}}?"

Examples:
- "Which model performs best for Code Generation in Hindi?"
- "Which language has the best performance for Math Reasoning with LLaMA-3?"

### Rules

1. **ONLY use languages and models from the provided mapping** - no invented data
2. **ONLY use EXACT model names and language names as written in the mapping** - do not modify, abbreviate, or add version numbers (e.g., if mapping has "Aya", do NOT use "Aya (33B)" or "Aya-33B"; if mapping has "DeepSeek-Coder-V2", do NOT use "DeepSeek-Coder-V2 (236B)")
3. **Data is available ONLY for specific language-model pairs** - each language maps to specific models that have been evaluated on it. A model listed for one language may NOT have data for another language. Use ONLY the exact (language, model) pairs from the mapping.
4. **CRITICAL: Respect the mapping structure** - if the mapping shows `Hindi: [GPT-4, LLaMA]`, then ONLY GPT-4 and LLaMA have data for Hindi. Do NOT generate questions about other models for Hindi. Questions MUST use exact language-model pairs as provided.
5. **EXCLUDE programming languages** - only natural languages (Hindi, French, Bengali, etc.)
6. **Prioritize low-resource languages** when available over high-resource ones (e.g., prefer Hindi, Bengali over English)
6. **Each question must have exactly ONE answer** - no comparisons or lists
7. **DO NOT specify metrics** in the question (no "accuracy", "F1", "BLEU", etc.)
8. Use exact task name provided
9. If multiple models/languages, list alphabetically comma-separated
10. Set empty string "" for missing fields
11. **Avoid questions like**:
   - "Compare X and Y" (multiple answers)
   - "What are the performances across..." (multiple values)
   - "List all models that..." (list answer)

### Output Distribution
- Generate exactly {num_predictive} PREDICTIVE questions
- Generate exactly {num_qna} QnA questions
- **Make questions as diverse as possible** - cover different pairs of languages and models from the mapping

### Output Format

Return **only JSON**:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str
        question_type: str  # Must be "Predictive" or "QnA"

    questions: list[Question]
```

Generate {num_questions} diverse questions covering different question types and language-model combinations.
Each question MUST have `question_type` set to either "Predictive" or "QnA".
"""


# =============================================================================
# SCENARIO-SPECIFIC PROMPTS (Original prompts from individual files)
# =============================================================================

SCENARIO1_PROMPT = """
You are given a language-to-models mapping for a specific NLP task where ground truth (GT) data is available.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show which models have been benchmarked on which languages for this task.
Each language maps to a list of models that have been evaluated on it.

### Goal

Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
Generate questions of the following types:

1. **Task + Model + Language**: Questions about specific model performance on specific language
2. **Task + Language**: Questions about how different models perform on a specific language  
3. **Task + Model**: Questions about how a specific model performs across languages
4. **Model + Language**: Questions about model performance on language (task implied)
5. **Task only**: Questions about overall task performance across languages/models

### Question Templates (adapt and vary phrasing):

1. *What is the performance of {{model}} on {{task}} for {{language}}?*
2. *How does {{model}} perform on {{task}} in {{language}}?*
3. *Compare {{model1}} and {{model2}} performance for {{language}} on {{task}} and tell which one is better*
4. *Which model performs best for {{task}} in {{language}}?*
7. *Which languages has the best performance for {{task}} for model {{model}}?*
8. *Which is the best performing model for {{task}} in {{language}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. For tasks like code generation, programming languages might be present as well. DO NOT generate questions for programming languages
2. **Use EXACT model names and language names as written** - do not modify, abbreviate, or add version numbers (e.g., if mapping has "Aya", do NOT use "Aya (33B)"; if mapping has "DeepSeek-Coder-V2", do NOT use "DeepSeek-Coder-V2 (236B)")
3. **Data exists ONLY for specific language-model pairs** - each language maps to specific models evaluated on it. Use ONLY the exact (language, model) pairs from the mapping
4. **CRITICAL: Respect the mapping structure** - if the mapping shows `Hindi: [GPT-4, LLaMA]`, then ONLY GPT-4 and LLaMA have data for Hindi. Do NOT generate questions about other models for Hindi. Questions MUST use exact language-model pairs as provided.
5. Use the exact task name provided
6. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
7. If task, model, or language is not present in a question, set it as `""` in the output
8. Questions must be clear, end with `?`, and avoid hallucinations. Use ONLY the information provided in the mapping
9. Generate diverse questions - avoid repetitive phrasing
10. Focus on realistic evaluation scenarios where GT data would be available

### Output Format

Return **only JSON** in this structure:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str
        question_type: str  # Must be "Predictive" or "QnA"

    questions: list[Question]
```

Generate {num_questions} diverse questions (half Predictive, half QnA). Each question MUST have `question_type` set.
"""


SCENARIO2_PROMPT = """
You are given a language-to-models mapping for a specific NLP task where ground truth (GT) data is NOT available.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show language-model combinations where benchmarks are MISSING.
Each language maps to models that have NOT been evaluated on it yet.

### Goal

Generate natural, varied evaluation questions for this task focusing on missing benchmarks and evaluation gaps.
Generate questions of the following types:

1. **Task + Model + Language**: Questions about specific model performance on specific language
2. **Task + Language**: Questions about how different models perform on a specific language  
3. **Model + Language**: Questions about model performance on language (task implied)

### Question Templates (adapt and vary phrasing):

1. *What is the performance of {{model}} on {{task}} for {{language}}?*
2. *How does {{model}} perform on {{task}} in {{language}}?*
3. *Which model performs best for {{task}} in {{language}}?*
4. *How does {{language}} performance vary across models for {{task}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. DO NOT generate questions for programming languages
2. **Use EXACT model names and language names as written** - do not modify, abbreviate, or add version numbers (e.g., if mapping has "DeepSeek-Coder-V2", do NOT use "DeepSeek-Coder-V2 (236B)")
3. **Each language maps to specific models** - use ONLY the exact (language, model) pairs from the mapping. Do not assume a model works for a language unless explicitly listed
4. **CRITICAL: Respect the mapping structure** - if the mapping shows `Hindi: [GPT-4, LLaMA]`, then ONLY GPT-4 and LLaMA are relevant for Hindi. Do NOT generate questions about other models for Hindi. Questions MUST use exact language-model pairs as provided.
5. Use the exact task name provided
6. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
7. If task, model, or language is not present in a question, set it as `""` in the output
8. Questions must be clear, end with `?`, and avoid hallucinations
9. Generate diverse questions - avoid repetitive phrasing
10. Focus on evaluation gaps and missing benchmarks where GT data is NOT available

### Output Format

Return **only JSON** in this structure:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str
        question_type: str  # Must be "Predictive" or "QnA"

    questions: list[Question]
```

Generate {num_questions} diverse questions (half Predictive, half QnA). Each question MUST have `question_type` set.
"""


SCENARIO3_PROMPT = """
You are given a language-to-models mapping for a specific NLP task where similar language data is available for inference.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show which models can potentially be evaluated on which languages using similar language data.
Each language maps to a list of models that could be evaluated on it using similar language benchmarks.

### Goal

Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
These questions should focus on cross-lingual transfer and similar language evaluation scenarios.
Generate questions of the following types:

1. **Task + Model + Language**: Questions about model performance on specific language using similar language data
2. **Task + Language**: Questions about how different models perform on a specific language via transfer  
3. **Model + Language**: Questions about model performance on language using transfer (task implied)

### Question Templates (adapt and vary phrasing):

1. *How would {{model}} perform on {{task}} for {{language}} using similar language data?*
2. *Can {{model}} transfer {{task}} performance from similar languages to {{language}}?*
3. *What is the cross-lingual performance of {{model}} on {{task}} for {{language}}?*
4. *How does {{language}} {{task}} performance compare using similar language transfer?*
5. *Which models show best cross-lingual transfer for {{task}} to {{language}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. DO NOT generate questions for programming languages
2. **Use EXACT model names and language names as written** - do not modify, abbreviate, or add version numbers
3. **Each language maps to specific models** - use ONLY the exact (language, model) pairs from the mapping. Do not assume a model works for a language unless explicitly listed
4. **CRITICAL: Respect the mapping structure** - if the mapping shows `Hindi: [GPT-4, LLaMA]`, then ONLY GPT-4 and LLaMA are relevant for Hindi. Do NOT generate questions about other models for Hindi. Questions MUST use exact language-model pairs as provided.
5. Use the exact task name provided
6. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
7. If task, model, or language is not present in a question, set it as `""` in the output
8. Questions must be clear, end with `?`, and avoid hallucinations
9. Generate diverse questions - avoid repetitive phrasing
10. Focus on cross-lingual transfer and similar language evaluation scenarios

### Output Format

Return **only JSON** in this structure:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str
        question_type: str  # Must be "Predictive" or "QnA"

    questions: list[Question]
```

Generate {num_questions} diverse questions (half Predictive, half QnA). Each question MUST have `question_type` set.
"""


SCENARIO4_PROMPT = """
You are given a language-to-models mapping for a specific NLP task where distant language transfer is needed.

Task: {task_name}
Language-Model Mappings: {mappings}

The mappings show which models can potentially be evaluated on which languages using distant language transfer.
Each language maps to a list of models that could be evaluated on it using distant (non-similar) language benchmarks.

### Goal

Generate natural, varied evaluation questions for this task using the language-model combinations from the mapping. 
These questions should focus on distant cross-lingual transfer scenarios where similar languages are NOT available.
Generate questions of the following types:

1. **Task + Model + Language**: Questions about model performance on specific language using distant language transfer
2. **Task + Language**: Questions about how different models perform on a specific language via distant transfer
3. **Model + Language**: Questions about model performance on language using distant transfer (task implied)

### Question Templates (adapt and vary phrasing):

1. *How would {{model}} perform on {{task}} for {{language}} using distant language transfer?*
2. *Can {{model}} transfer {{task}} performance from distant languages to {{language}}?*
3. *What is the distant cross-lingual performance of {{model}} on {{task}} for {{language}}?*
4. *How does {{language}} {{task}} performance compare using distant language transfer?*
5. *Which models show best distant cross-lingual transfer for {{task}} to {{language}}?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. DO NOT generate questions for programming languages
2. **Use EXACT model names and language names as written** - do not modify, abbreviate, or add version numbers
3. **Each language maps to specific models** - use ONLY the exact (language, model) pairs from the mapping. Do not assume a model works for a language unless explicitly listed
4. **CRITICAL: Respect the mapping structure** - if the mapping shows `Hindi: [GPT-4, LLaMA]`, then ONLY GPT-4 and LLaMA are relevant for Hindi. Do NOT generate questions about other models for Hindi. Questions MUST use exact language-model pairs as provided.
5. Use the exact task name provided
6. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
7. If task, model, or language is not present in a question, set it as `""` in the output
8. Questions must be clear, end with `?`, and avoid hallucinations
9. Generate diverse questions - avoid repetitive phrasing
10. Focus on distant cross-lingual transfer scenarios where similar languages are NOT available

### Output Format

Return **only JSON** in this structure:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str
        question_type: str  # Must be "Predictive" or "QnA"

    questions: list[Question]
```

Generate {num_questions} diverse questions (half Predictive, half QnA). Each question MUST have `question_type` set.
"""


SCENARIO5_PROMPT = """
You are given a language-to-models mapping for a specific NLP task where both the language AND the model are NOT available in the system's accessible data.

Task: {task_name}
Language-Model Mappings: {mappings}

This is **Scenario 5: Different Language, Different Model (Both Unavailable)**
The mappings show language-model combinations where:
- The language is NOT available in the accessible data (Lav)
- The model is also NOT available for ANY language in the accessible data
- These combinations exist only in the ground truth (Lgt) but not in Lav

### Goal

Generate natural, varied evaluation questions for this task focusing on scenarios where we need to evaluate performance but have NO direct data for either the language or the model.

Generate questions of the following types:

1. **Zero-Shot Evaluation**: Questions about evaluating without any available data
2. **Model-Language Gap**: Questions about missing model support for specific languages
3. **Resource Limitation**: Questions about working with completely unavailable combinations

### Question Templates (adapt and vary phrasing):

1. *How can we estimate {{model}} performance on {{language}} when neither is available in our data?*
2. *What is the expected performance of {{model}} for {{task}} in {{language}}?*
3. *Can we evaluate {{model}} on {{language}} without any direct benchmark data?*
4. *What approaches exist for assessing {{task}} performance in {{language}} using {{model}}?*
5. *How would {{model}} handle {{task}} for {{language}} based on related benchmarks?*

### Rules

1. **Only use languages and models from the provided mapping** - do not invent new ones. Generate questions of only natural languages. DO NOT generate questions for programming languages
2. **Use EXACT model names and language names as written** - do not modify, abbreviate, or add version numbers
3. **Each language maps to specific models** - use ONLY the exact (language, model) pairs from the mapping. Do not assume a model works for a language unless explicitly listed
4. **CRITICAL: Respect the mapping structure** - if the mapping shows `Hindi: [GPT-4, LLaMA]`, then ONLY GPT-4 and LLaMA are relevant for Hindi. Do NOT generate questions about other models for Hindi. Questions MUST use exact language-model pairs as provided.
5. Use the exact task name provided
6. If multiple models/languages in a question, list them alphabetically, comma-separated (no spaces)
7. If task, model, or language is not present in a question, set it as `""` in the output
8. Questions must be clear, end with `?`, and avoid hallucinations
9. Generate diverse questions - avoid repetitive phrasing
10. Focus on scenarios where BOTH language AND model are unavailable

### Output Format

Return **only JSON** in this structure:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str
        question_type: str  # Must be "Predictive" or "QnA"

    questions: list[Question]
```

Generate {num_questions} diverse questions (half Predictive, half QnA). Each question MUST have `question_type` set.
"""


# =============================================================================
# PROMPT REGISTRY
# =============================================================================

SCENARIO_PROMPTS = {
    1: SCENARIO1_PROMPT,
    2: SCENARIO2_PROMPT,
    3: SCENARIO3_PROMPT,
    4: SCENARIO4_PROMPT,
    5: SCENARIO5_PROMPT,
}

SCENARIO_NAMES = {
    1: "GT_available",
    2: "same_language_different_model",
    3: "similar_language_same_model",
    4: "distant_language_same_model",
    5: "different_language_different_model",
}


def get_prompt(scenario: int, use_common_prompt: bool = True) -> str:
    """
    Get the appropriate prompt for a scenario.
    
    Args:
        scenario: Scenario number (1-5)
        use_common_prompt: If True, use the common prompt; else use scenario-specific
    
    Returns:
        Prompt template string
    """
    if use_common_prompt:
        return COMMON_PROMPT
    return SCENARIO_PROMPTS.get(scenario, COMMON_PROMPT)


def get_scenario_name(scenario: int) -> str:
    """Get the human-readable name for a scenario."""
    return SCENARIO_NAMES.get(scenario, f"scenario_{scenario}")
