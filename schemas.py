from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from typing import ClassVar, Optional

class SessionCreate(BaseModel):
    user_id: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    expires_at: Optional[datetime]

class SessionResponse(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]

    class Config:
        orm_mode = True


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

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class AuthorOut(BaseModel):
    id: str
    name: str
    username: str

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class ReportCommentRequest(BaseModel):
    reason: str

class CommentReportCreate(BaseModel):
    comment_id: int
    reason: str


class CommentReportResponse(BaseModel):
    id: int
    comment_id: int
    user_id: Optional[str]
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True
class UserOut(BaseModel):
    username: str

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class WorkOut(BaseModel):
    id: str
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

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class ChapterCreate(BaseModel):
    title: str
    content: str
    num: int
    work_id: str


class ChapterSchema(BaseModel):
    id: Optional[str]  # якщо є id, можна і без нього
    title: str
    content: str
    work_id: str

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    num: Optional[int] = None


class ChapterOut(BaseModel):
    id: str
    title: str
    content: Optional[str] = None  # Зробити необов'язковим
    num: int
    work_id: str

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class WorkCreateSchema(BaseModel):
    title: str
    author_id: str
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
    tags: Optional[List[str]]
    age_limit: Optional[int]
    status_id: Optional[int]

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }

class WorkStatusOut(BaseModel):
    id: int
    name: str

    model_config: ClassVar[dict] = {"from_attributes": True}

class AuthorOut(BaseModel):
    id: str
    name: str
    username: str

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }
# schemas.py
class WorkResponseSchema(BaseModel):
    id: str
    title: str
    description: Optional[str]
    cover_path: Optional[str]
    file_path: Optional[str]
    category: Optional[int]  # замість category_id
    status_id: Optional[int]
    age_limit: Optional[int]
    author: str
    created_at: datetime
    updated_at: datetime

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }




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

    model_config: ClassVar[dict] = {
        "from_attributes": True
    }


class InteractionStats(BaseModel):
    likes: int
    views: int
    reads: int
    saved: int
class RatingCreate(BaseModel):
    work_id: str
    rating: int = Field(..., ge=1, le=5)  # ⭐ 1–5

class RatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5)

class RatingOut(BaseModel):
    id: int
    work_id: str
    user_id: str
    rating: int

    class Config:
        from_attributes = True

class RatingResponse(BaseModel):
    id: int
    work_id: UUID
    user_id: UUID
    rating: int

    class Config:
        orm_mode = True
class IdeaCreate(BaseModel):
    title: str
    description: str

class IdeaResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str
    created_at: datetime

    class Config:
        orm_mode = True
class IdeaWorkCreate(BaseModel):
    idea_id: UUID
    work_id: UUID

class IdeaWorkResponse(BaseModel):
    id: UUID
    idea_id: UUID
    work_id: UUID

    class Config:
        orm_mode = True
WorkResponseSchema.model_rebuild()
