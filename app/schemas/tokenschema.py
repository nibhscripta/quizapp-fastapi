from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# JWT token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None