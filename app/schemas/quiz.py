from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from . import user

# Quiz schemas
class Quiz(BaseModel):
    title: str
    content: str
    

class QuizResponse(Quiz):
    id: int
    created_at: datetime
    owner_id: int
    owner: user.UserResponse
    
    class Config:
        orm_mode = True 
    

class Answer(BaseModel):
    answer: str
    correct: bool = False
    

class AnswerResponse(Answer):
    id: int
    created_at: datetime
    question_id: int
    
    class Config:
        orm_mode: True

class QuizQuestion(BaseModel): 
    question: str
    
    
class CreateQuizQuestion(QuizQuestion):
    answers: list[Answer]

    
class QuizQuestionResponse(QuizQuestion):
    id: int
    created_at: datetime
    quiz_id: int
    answers: list[AnswerResponse]
    
    class Config:
        orm_mode = True


class QuizQuestionAnswers(QuizQuestionResponse):
    answers: list[AnswerResponse]
    
    class Config:
        orm_mode = True