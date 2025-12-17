from sqlalchemy import Column, String, Integer, Text, Boolean, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.sql import func
from datetime import datetime
Base = declarative_base()

class WorkStatus(Base):
    __tablename__ = 'work_statuses'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15))
    avatar_path = Column(String(150))
    birth = Column(Integer)
    bio = Column(Text)

    works = relationship("Work", back_populates="author_user")
    interactions = relationship("UserInteraction", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    # models/user.py
    comment_reports = relationship(
        "CommentReport",
        back_populates="user"
    )

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

class Work(Base):
    __tablename__ = 'works'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author = Column(String(36), ForeignKey('users.id'), nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(Text)
    cover_path = Column(String(150))
    file_path = Column(String(150))
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    age_limit = Column(Integer)
    status_id = Column(Integer, ForeignKey('work_statuses.id'))

    ratings = relationship("Rating", back_populates="work")
    author_user = relationship("User", back_populates="works")
    category = relationship("Category", backref="works")
    status = relationship("WorkStatus", backref="works")
    tags = relationship("Tag", secondary="work_tags", backref="works", overlaps="work,tag")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_id = Column(String(36), ForeignKey('works.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    work = relationship('Work')
    user = relationship('User')

class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_id = Column(String(36), ForeignKey('works.id'), nullable=False)
    num = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    file_path = Column(String(255))

    work = relationship('Work')

class UserInteraction(Base):
    __tablename__ = 'user_interactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(String(36), ForeignKey('works.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    is_saved = Column(Boolean, default=False, nullable=False)
    is_liked = Column(Boolean, default=False, nullable=False)
    is_viewed = Column(Boolean, default=False, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    work = relationship('Work')
    user = relationship("User", back_populates="interactions")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    chapter_id = Column(String(36), ForeignKey('chapters.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="comments")
    chapter = relationship('Chapter')
    reports = relationship(
        "CommentReport",
        back_populates="comment",
        cascade="all, delete-orphan"
    )
class CommentReport(Base):
    __tablename__ = "comment_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    reason = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    comment = relationship("Comment", back_populates="reports")
    user = relationship("User", back_populates="comment_reports")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String(36), ForeignKey("works.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)

    work = relationship("Work", back_populates="ratings")
    user = relationship("User")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))  # додали поле для зв'язку
    category = relationship("Category")

class WorkTag(Base):
    __tablename__ = 'work_tags'
    work_id = Column(String(36), ForeignKey('works.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    work = relationship('Work', overlaps="tags,works")
    tag = relationship('Tag', overlaps="tags,works")

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)

    user = relationship("User", back_populates="sessions")

class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subscriber_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    subscribed_to_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    subscriber = relationship('User', foreign_keys=[subscriber_id], backref='subscriptions')
    subscribed_to = relationship('User', foreign_keys=[subscribed_to_id], backref='subscribers')

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class IdeaWork(Base):
    __tablename__ = "idea_works"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idea_id = Column(String(36), ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False)
    work_id = Column(String(36), ForeignKey("works.id", ondelete="CASCADE"), nullable=False)

