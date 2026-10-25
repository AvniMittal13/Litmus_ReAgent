"""
Pydantic models for question generation.
"""
import uuid
from pydantic import BaseModel, Field
from typing import List, Literal


class Question(BaseModel):
    complete_question: str
    task: str
    models: str
    languages: str
    question_type: Literal["Predictive", "QnA"]


class QuestionsGenerated(BaseModel):
    questions: List[Question]
