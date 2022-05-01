from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Any, Optional, List

from app.schemas import user

class QuizInstance(BaseModel):
    username: str

class QuizInstanceResponse(QuizInstance):
    id: int
    user_id: str
    created_at: datetime
    quiz_id: int
    
    class Config:
        orm_mode = True


class Assessment(BaseModel):
    title: str
    content: str
    id: int
    created_at: datetime
    owner_id: int
    due: Any
    
    class Config:
        orm_mode = True 
        
class AssessmentQuestion(BaseModel):
    question: str
    id: int
    quiz_id: int
    
    class Config:
        orm_mode = True 
    
class AssessmentAnswer(BaseModel):
    answer: str
    id: int
    question_id: int
    
    class Config:
        orm_mode = True

  
class AssessmentResult(BaseModel):  
    question: str
    posted_answer: str
    correct_answer: str
    correct: bool
    
class InstanceAnswer(BaseModel):
    instance_id: int
    answer_id: int
    user_id: str