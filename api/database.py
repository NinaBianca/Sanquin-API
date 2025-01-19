import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import Session


# load env vars
load_dotenv()

# create engine
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
if not POSTGRES_SERVER:
    raise ValueError("POSTGRES_SERVER is not set")

engine = create_engine(
    POSTGRES_SERVER,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()