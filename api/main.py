from fastapi import FastAPI

app = FastAPI()

from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from routers import users, challenges, donations, posts
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from models.user import User
from models.donation import Donation
from models.challenge import Challenge
from models.challenge_user import ChallengeUser
from models.kudos import Kudos
from models.post import Post
from datetime import datetime
from fastapi import Depends

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    load_dotenv()
except Exception as e:
    SystemExit(f"Error loading .env file: {e}")


app = FastAPI(
    title="Sanquin API",
    description="API for the Sanquin project",
    version="0.1.0",
    redoc_url=None,
    docs_url="/docs",
)

app.include_router(users.router)
app.include_router(challenges.router)
app.include_router(donations.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return JSONResponse(
        content={
            "message": "Welcome to the Sanquin API! \n Visit /docs for the API documentation.",
        },
        status_code=200,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)