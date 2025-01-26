from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        orm_mode = True
        
class UserVoteInfo(BaseModel):
    poll_id: int
    poll_title: str
    option_id: int
    option_text: str

class UserProfileResponse(BaseModel):
    username: str
    email: str
    votes: List[UserVoteInfo]

    class Config:
        orm_mode = True

