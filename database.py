from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://stustop:ilovepespatron@localhost:3306/toread"
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
SYNC_DATABASE_URL = "mysql+pymysql://stustop:ilovepespatron@localhost:3306/toread"

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

SyncSessionLocal = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False)

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
