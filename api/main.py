from fastapi import FastAPI, Response
from dotenv import load_dotenv
from routers import users, posts, donations, challenges

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
app.include_router(posts.router)
app.include_router(donations.router)
app.include_router(challenges.router)


@app.get("/")
async def root():
    return Response(
        content={
            "message": "Welcome to the Sanquin API! \n Visit /docs for the API documentation."
        },
        status_code=200,
    )

