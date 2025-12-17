from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .user_profile import get_current_user_id
from models import UserSubscription, User
from uuid import uuid4

router = APIRouter(prefix="/user-subscriptions", tags=["User Subscriptions"])
@router.post("/{target_user_id}")
def subscribe_user(target_user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user_id)):
    if current_user == target_user_id:
        raise HTTPException(status_code=400, detail="Cannot subscribe to yourself")

    subscription = db.query(UserSubscription).filter_by(subscriber_id=current_user, subscribed_to_id=target_user_id).first()
    if subscription:
        db.delete(subscription)
        db.commit()
        return {"detail": "Unsubscribed successfully"}
    else:
        new_sub = UserSubscription(subscriber_id=current_user, subscribed_to_id=target_user_id)
        db.add(new_sub)
        db.commit()
        return {"detail": "Subscribed successfully"}

# Список підписників користувача
@router.get("/{user_id}/subscribers")
def get_subscribers(user_id: str, db: Session = Depends(get_db)):
    subs = db.query(UserSubscription).filter_by(subscribed_to_id=user_id).all()
    return {"subscribers": [s.subscriber_id for s in subs]}

# Список користувачів, на яких підписаний користувач
@router.get("/{user_id}/subscriptions")
def get_subscriptions(user_id: str, db: Session = Depends(get_db)):
    subs = db.query(UserSubscription).filter_by(subscriber_id=user_id).all()
    return {"subscriptions": [s.subscribed_to_id for s in subs]}
@router.get("/followers/{user_id}")
def get_followers_count(user_id: str, db: Session = Depends(get_db)):
    count = db.query(UserSubscription).filter(UserSubscription.subscribed_to_id == user_id).count()
    return {"user_id": user_id, "followers_count": count}

@router.get("/following/{user_id}")
def get_following_count(user_id: str, db: Session = Depends(get_db)):
    count = db.query(UserSubscription).filter(UserSubscription.subscriber_id == user_id).count()
    return {"user_id": user_id, "following_count": count}
@router.get("/friends/{user_id}")
def get_friends(user_id: str, db: Session = Depends(get_db)):
    # отримуємо список користувачів, за якими стежить user_id
    following = db.query(UserSubscription.subscribed_to_id).filter(
        UserSubscription.subscriber_id == user_id
    ).subquery()

    # отримуємо взаємні підписки: хто стежить за user_id і за ким він стежить
    friends = db.query(User).join(
        UserSubscription,
        (User.id == UserSubscription.subscriber_id) &
        (UserSubscription.subscribed_to_id == user_id)
    ).filter(User.id.in_(following)).all()

    return [{"id": u.id, "username": u.username, "name": u.name, "last_name": u.last_name} for u in friends]
