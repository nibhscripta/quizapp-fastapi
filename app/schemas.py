from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


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
class QuizBase(BaseModel):
    title: str
    content: str
    
class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
        
    class Config:
        orm_mode = True
    

# JWT token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
