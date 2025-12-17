from typing import List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Rating, Work, UserInteraction
from sqlalchemy.orm import joinedload
import logging
from routers.work_metadata import count_likes, count_views, count_reads, count_saves
from uuid import UUID
from .user_profile import has_interacted
router = APIRouter()

# 1. Матриця користувач-товар
def create_user_item_matrix(db: Session):
    ratings = db.query(Rating).all()
    data = [(str(r.user_id), str(r.work_id), r.rating) for r in ratings]
    df = pd.DataFrame(data, columns=['user_id', 'work_id', 'rating'])
    if df.empty:
        return pd.DataFrame()
    matrix = df.pivot(index='user_id', columns='work_id', values='rating').fillna(0)
    return matrix

# 2. Контентна подібність (по опису творів)
def calculate_content_similarity(works: List[Work]):
    descriptions = [w.description or '' for w in works]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    return cosine_similarity(tfidf_matrix)

# 3. Колаборативна подібність між користувачами
def calculate_user_similarity(user_item_matrix: pd.DataFrame):
    return cosine_similarity(user_item_matrix)

# 4. Рекомендації на основі опису (контент)
def get_content_based(user_id: str, works: List[Work], content_sim):
    user_rated_works = [w for w in works if str(user_id) in [str(r.user_id) for r in w.ratings]]
    if not user_rated_works:
        return works  # якщо користувач нічого не оцінював, повернути всі твори без сортування

    rated_indices = [works.index(w) for w in user_rated_works if w in works]

    # Обчислюємо середню схожість кожного твору до творів, які користувач оцінив
    similarity_scores = np.mean([content_sim[i] for i in rated_indices], axis=0)

    # Сортуємо індекси творів за спаданням схожості
    sorted_indices = np.argsort(similarity_scores)[::-1]

    # Повертаємо всі твори у порядку релевантності
    sorted_works = [works[i] for i in sorted_indices]

    return sorted_works


# 5. Рекомендації на основі інших користувачів (колаборативна)
def get_collaborative_based(user_id: str, matrix: pd.DataFrame, similarity):
    if user_id not in matrix.index:
        return []
    user_idx = matrix.index.get_loc(user_id)
    sim_scores = list(enumerate(similarity[user_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_users_idx = [i for i, _ in sim_scores[1:6]]
    top_users = matrix.iloc[top_users_idx]
    mean_scores = top_users.mean().sort_values(ascending=False)
    recommended_work_ids = mean_scores.index[:5].tolist()
    return recommended_work_ids

# 6. Гібридна функція
# 6. Гібридна функція з можливістю рекомендації за популярністю
def hybrid_recommendation(user_id: str, db: Session):
    works = db.query(Work).all()
    if not works:
        return []

    matrix = create_user_item_matrix(db)
    content_sim = calculate_content_similarity(works)
    collab_sim = calculate_user_similarity(matrix) if not matrix.empty else None

    content_recs = get_content_based(user_id, works, content_sim)
    collab_recs_ids = get_collaborative_based(user_id, matrix, collab_sim) if collab_sim is not None else []
    collab_recs = [w for w in works if str(w.id) in collab_recs_ids]

    if not collab_recs:
        print(f"Користувач {user_id} не має колаборативних рекомендацій, вибір за популярністю.")
        # Повертаємо всі твори
        results = works
    else:
        combined = list({w.id: w for w in content_recs + collab_recs}.values())
        results = combined  # без обрізки [:5]

    # Фільтруємо твори автора, що робить запит
    filtered_results = [w for w in results if w.author_user and str(w.author_user.id) != user_id]


    # Можна обмежити кількість рекомендованих творів, наприклад, до 10
    return filtered_results[:10]
@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str, db: Session = Depends(get_db)):
    try:
        recommendations = hybrid_recommendation(user_id, db)

        recommendations_data = []

        for work in recommendations:
            work_with_details = db.query(Work).options(
                joinedload(Work.category),
                joinedload(Work.author_user),
                joinedload(Work.tags)
            ).filter(Work.id == work.id).first()

            if not work_with_details:
                continue

            # ✅ Ось тут вже можемо використовувати work_with_details.id
            likes = count_likes(db, work_with_details.id)
            saves = count_saves(db, work_with_details.id)
            views = count_views(db, work_with_details.id)
            read = count_reads(db, work_with_details.id)

            # ✅ Виклики перевірки взаємодії
            is_liked = has_interacted(db, str(user_id), work_with_details.id, "like")
            is_saved = has_interacted(db, str(user_id), work_with_details.id, "save")
            is_viewed = has_interacted(db, str(user_id), work_with_details.id, "view")
            is_read = has_interacted(db, str(user_id), work_with_details.id, "read")

            work_data = {
                "id": str(work_with_details.id),
                "title": work_with_details.title,
                "description": work_with_details.description,
                "author": work_with_details.author_user.name if work_with_details.author_user else "Невідомий автор",
                "genres": [work_with_details.category.name] if work_with_details.category else [],
                "tags": [tag.name for tag in work_with_details.tags],
                "likes": likes,
                "views": views,
                "saved": saves,
                "read": read,
                "isLiked": is_liked,
                "isSaved": is_saved,
                "isViewed": is_viewed,
                "isRead": is_read,
            }
            recommendations_data.append(work_data)

        return recommendations_data

    except Exception as e:
        logging.error(f"Помилка отримання рекомендацій для {user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Не вдалося отримати рекомендації: {str(e)}")

