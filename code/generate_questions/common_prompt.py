prompt_scenario_improved = """
You are given a language-to-models mapping for a specific NLP task where ground truth benchmark data is available.

Task: {task_name}
Language-Model Mappings: {mappings}

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
2. **EXCLUDE programming languages** - only natural languages (Hindi, French, Bengali, etc.)
3. **Prioritize low-resource languages** when available over high-resource ones (e.g., prefer Hindi, Swahili, Bengali over English)
4. **Each question must have exactly ONE answer** - no comparisons or lists
5. **DO NOT specify metrics** in the question (no "accuracy", "F1", "BLEU", etc.)
6. Use exact task name provided
7. If multiple models/languages, list alphabetically comma-separated
8. Set empty string "" for missing fields
9. **Avoid questions like**:
   - "Compare X and Y" (multiple answers)
   - "What are the performances across..." (multiple values)
   - "List all models that..." (list answer)

### Output Distribution
- Generate approximately {num_predictive} PREDICTIVE questions
- Generate approximately {num_qna} QnA questions

### Output Format

Return **only JSON**:

```py
class QuestionsGenerated(BaseModel):
    class Question(BaseModel):
        complete_question: str
        task: str
        models: str  
        languages: str

    questions: list[Question]
```

Generate {num_questions} diverse questions covering different question types and language-model combinations.
"""