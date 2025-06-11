from typing import List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Rating, Work
from sqlalchemy.orm import joinedload

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
    # Отримаємо всі твори, які оцінив цей користувач
    user_rated_works = [w for w in works if str(user_id) in [str(r.user_id) for r in w.ratings]]
    if not user_rated_works:
        return []

    rated_indices = [works.index(w) for w in user_rated_works if w in works]

    # Середнє подібності до інших творів
    similarity_scores = np.mean([content_sim[i] for i in rated_indices], axis=0)
    top_indices = np.argsort(similarity_scores)[::-1][:6]

    return [works[i] for i in top_indices if works[i] not in user_rated_works]

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

    # Контентні рекомендації
    content_recs = get_content_based(user_id, works, content_sim)

    # Колаборативні рекомендації
    collab_recs_ids = get_collaborative_based(user_id, matrix, collab_sim) if collab_sim is not None else []

    collab_recs = [w for w in works if str(w.id) in collab_recs_ids]

    # Якщо немає колаборативних рекомендацій, застосовуємо популярність
    if not collab_recs:
        print(f"Користувач {user_id} не має колаборативних рекомендацій, вибір за популярністю.")
        # Сортуємо твори по кількості оцінок та середньому рейтингу
        popular_works = db.query(Work, func.count(Rating.id).label('rating_count'), func.avg(Rating.rating).label('avg_rating')) \
            .join(Rating, Rating.work_id == Work.id) \
            .group_by(Work.id) \
            .order_by(func.count(Rating.id).desc(), func.avg(Rating.rating).desc()) \
            .limit(5) \
            .all()

        return [work[0] for work in popular_works]

    # Об'єднання та унікальність
    combined = list({w.id: w for w in content_recs + collab_recs}.values())[:5]
    return combined
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

            work_data = {
                "id": str(work_with_details.id),
                "title": work_with_details.title,
                "description": work_with_details.description,
                "author": work_with_details.author_user.name if work_with_details.author_user else "Невідомий автор",
                "genres": [work_with_details.category.name] if work_with_details.category else [],
                "tags": [tag.name for tag in work_with_details.tags],
            }
            recommendations_data.append(work_data)

        return recommendations_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не вдалося отримати рекомендації: {str(e)}")
