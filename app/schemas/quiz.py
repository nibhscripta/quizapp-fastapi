from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from . import user

# Quiz schemas
class Quiz(BaseModel):
    title: str
    content: str
    public: Optional[bool] = False
    due: Optional[datetime] = None
    

class QuizResponse(Quiz):
    id: int
    created_at: datetime
    owner_id: int
    owner: user.UserResponse
    public: bool
    
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
        orm_mode = True 
        

class QuizQuestion(BaseModel): 
    question: str

    
class QuizQuestionResponse(QuizQuestion):
    id: int
    created_at: datetime
    quiz_id: int
    
    class Config:
        orm_mode = True