from sqlalchemy import Column, String, Integer, Text, UUID, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class WorkStatus(Base):
    __tablename__ = 'work_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
class User(Base):
    __tablename__ = 'users'

    id = Column(PGUUID(as_uuid=True), primary_key=True)
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

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
class Work(Base):
	__tablename__ = 'works'

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	title = Column(String(100), nullable=False)
	author = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
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

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    work_id = Column(PGUUID(as_uuid=True), ForeignKey('works.id'), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    work = relationship('Work')
    user = relationship('User')

class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    work_id = Column(PGUUID(as_uuid=True), ForeignKey('works.id'), nullable=False)
    num = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    file_path = Column(String(255))

    work = relationship('Work')

class UserInteraction(Base):
    __tablename__ = 'user_interactions'

    id = Column(Integer, primary_key=True)
    work_id = Column(PGUUID(as_uuid=True), ForeignKey('works.id'), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    is_saved = Column(Boolean, default=False, nullable=False)
    is_liked = Column(Boolean, default=False, nullable=False)
    is_viewed = Column(Boolean, default=False, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    work = relationship('Work')
    user = relationship("User", back_populates="interactions")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    chapter_id = Column(PGUUID(as_uuid=True), ForeignKey('chapters.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="comments")
    chapter = relationship('Chapter')
class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)

    # зворотній зв’язок
    work = relationship("Work", back_populates="ratings")
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)


class WorkTag(Base):
    __tablename__ = 'work_tags'

    work_id = Column(PGUUID(as_uuid=True), ForeignKey('works.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    work = relationship('Work', overlaps="tags,works")
    tag = relationship('Tag', overlaps="tags,works")

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)

    user = relationship("User", back_populates="sessions")
