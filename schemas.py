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

class AuthorOut(BaseModel):
    id: UUID
    name: str
    username: str
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
    author_user: AuthorOut
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
        from_attributes = True
class ChapterCreate(BaseModel):
    title: str
    content: str
    num: int
    work_id: UUID

class ChapterSchema(BaseModel):
    id: Optional[UUID]  # якщо є id, можна і без нього
    title: str
    content: str
    work_id: UUID

    class Config:
        orm_mode = True

class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    num: Optional[int] = None

class ChapterOut(BaseModel):
    id: UUID
    title: str
    content: str
    num: int
    work_id: UUID



class WorkCreateSchema(BaseModel):

    title: str
    author_id: UUID
    description: Optional[str] = None
    cover_path: Optional[str] = None
    file_path: Optional[str] = None
    category_id: Optional[int] = None
    age_limit: Optional[int] = None
    status_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class WorkUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    cover_path: Optional[str]
    file_path: Optional[str]
    category_id: Optional[int]
    tags: Optional[List[UUID]]
    age_limit: Optional[int]
    status_id: Optional[int]

    class Config:
        orm_mode=True

class WorkResponseSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    cover_path: Optional[str]
    file_path: Optional[str]
    category_id: Optional[int]
    status_id: Optional[int]
    age_limit: Optional[int]
    author: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
class UserProfileOut(BaseModel):
    id: str
    name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    avatar_path: Optional[str]
    birth: Optional[int]
    bio: Optional[str]

    class Config:
        orm_mode = True
class InteractionStats(BaseModel):
    likes: int
    views: int
    reads: int
    saved: int

