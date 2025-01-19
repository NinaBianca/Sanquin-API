from fastapi import FastAPI, Response
from dotenv import load_dotenv
from .routers import users, posts, donations, challenges
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis
import os
from contextlib import asynccontextmanager


try:
    load_dotenv()
except Exception as e:
    SystemExit(f"Error loading .env file: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.getenv("REDIS_URL")
    redis_client = redis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    yield

app = FastAPI(
    title="Sanquin API",
    description="API for the Sanquin project",
    version="0.1.0",
    redoc_url=None,
    docs_url="/docs",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(donations.router)
app.include_router(challenges.router)


@app.get("/")
async def root():
    return  "Welcome to the Sanquin API! \n Visit /docs for the API documentation."


