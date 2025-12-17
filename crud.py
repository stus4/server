from sqlalchemy.orm import Session, joinedload
from models import Work, UserInteraction

def get_liked_works(db: Session, user_id: str):
    interactions = db.query(UserInteraction)\
        .options(
            joinedload(UserInteraction.work)
            .joinedload(Work.category),
            joinedload(UserInteraction.work)
            .joinedload(Work.status),
            joinedload(UserInteraction.work)
            .joinedload(Work.tags),
            joinedload(UserInteraction.work)
            .joinedload(Work.author_user)
        )\
        .filter(UserInteraction.user_id == user_id, UserInteraction.is_liked == True)\
        .all()

    result = []
    for interaction in interactions:
        work = interaction.work
        result.append({
            "id": work.id,
            "title": work.title,
            "description": work.description,
            "cover_path": work.cover_path,
            "file_path": work.file_path,
            "created_at": work.created_at,
            "updated_at": work.updated_at,
            "age_limit": work.age_limit,
            "category": {
                "id": work.category.id,
                "name": work.category.name,
                "description": work.category.description
            } if work.category else None,
            "status": {
                "id": work.status.id,
                "name": work.status.name
            } if work.status else None,
            "tags": [{"id": tag.id, "name": tag.name} for tag in work.tags],
            "author": {
                "id": work.author_user.id,
                "name": work.author_user.name,
                "last_name": work.author_user.last_name,
                "username": work.author_user.username,
                "avatar_path": work.author_user.avatar_path
            } if work.author_user else None
        })
    return result

