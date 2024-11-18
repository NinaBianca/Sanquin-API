from fastapi import FastAPI
from dotenv import load_dotenv
from routers import users

load_dotenv()


app = FastAPI()
app.include_router(users.router)


@app.get("/")
async def root():
    return {
        200: {
            "message": "Welcome to the Sanquin API! \n Visit /docs for the API documentation."
        }
    }
