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

class OptionCreate(BaseModel):
    text: str

class OptionResponse(BaseModel):
    id: int
    text: str
    poll_id: int

    class Config:
        orm_mode = True
        
class OptionInput(BaseModel):
    text: str  
    
class PollCreate(BaseModel):
    title: str
    description: str
    options: List[OptionInput]

class PollResponse(PollCreate):
    id: int
    owner_id: int
    options: List[OptionResponse] = []

    class Config:
        orm_mode = True

class Vote(BaseModel):
    option_id: int
    
class PollListResponse(BaseModel):
    id: int
    title: str
    description: str
    votes_count: int = Field(0, description="Votes count")

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    content: str
    tonality: Optional[str] = None

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    user_id: int
    poll_id: int
    
    class Config:
        orm_mode = True