import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


# load env vars
load_dotenv()

# create engine
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
if not POSTGRES_SERVER:
    raise ValueError("POSTGRES_SERVER is not set")

engine = create_engine(POSTGRES_SERVER)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()