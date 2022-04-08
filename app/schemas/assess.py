from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class Assessment(BaseModel):
    title: str
    content: str
    id: int
    created_at: datetime
    owner_id: int
    
    class Config:
        orm_mode = True 
        
class AssessmentQuestion(BaseModel):
    question: str
    id: int
    quiz_id: int
    
class AssessmentAnswer(BaseModel):
    answer: str
    id: int
    question_id: int