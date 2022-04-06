from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# User model schemas
#response sent when a particular user data is retrieved   
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

# Quiz schemas
class Quiz(BaseModel):
    title: str
    content: str
    

class QuizResponse(Quiz):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
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
    answers: list[Answer]
    
    
class QuizQuestionResponse(QuizQuestion):
    id: int
    created_at: datetime
    quiz_id: int
    
    class Config:
        orm_mode = True


# JWT token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
