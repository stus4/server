from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    name: str
    last_name: str
    email: EmailStr
    password: str
    birth: Optional[str] = None
    phone_number: Optional[str] = None
    avatar_path: Optional[str] = None
    bio: Optional[str] = None

class RecommendationOut(BaseModel):
    id: str
    title: str
    author: str
    genres: List[str]
    tags: List[str]
class CommentCreate(BaseModel):
    content: str
    work_id: Optional[str] = None
    chapter_id: Optional[str] = None


class CommentOut(BaseModel):
    id: str
    user_id: str
    text: str
    created_at: datetime

    class Config:
        orm_mode = True


class ReportCommentRequest(BaseModel):
    reason: str
class UserOut(BaseModel):
    username: str


    class Config:
        orm_mode = True

class WorkOut(BaseModel):
    id: UUID
    title: str
    author: str
    description: Optional[str]
    cover_path: Optional[str]
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime
    category_id: Optional[int]
    age_limit: Optional[int]
    status_id: Optional[int]

    class Config:
        orm_mode = True


