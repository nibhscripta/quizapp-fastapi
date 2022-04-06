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