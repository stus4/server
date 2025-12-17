from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers import auth, recommendations, work_metadata, popular, works, chapters, user_interactions, user, subscriptions, user_subscriptions, sessions, comments, comment_reports, ratings, ideas
from database import engine, Base

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

app = FastAPI()

# Додаємо CORS middleware першим
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на продакшені краще вказати конкретні адреси
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо роутери після middleware
app.include_router(work_metadata.router)
app.include_router(auth.router)
app.include_router(recommendations.router)
app.include_router(popular.router)
app.include_router(comments.router)
app.include_router(chapters.router)
app.include_router(work_metadata.router, prefix="/api/work-metadata", tags=["Work Metadata"])
app.include_router(works.router)
app.include_router(user_interactions.router)
app.include_router(user.router)
app.include_router(ideas.router)

app.include_router(ratings.router)
app.include_router(comment_reports.router)
app.include_router(sessions.router)

app.include_router(subscriptions.router)
app.include_router(user_subscriptions.router)
# Створення таблиць у базі даних
Base.metadata.create_all(bind=engine)
