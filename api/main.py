from fastapi import FastAPI, Response, Security
from dotenv import load_dotenv
from routers import users, posts, donations, challenges
from services.auth import VerifyToken as auth 

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


@app.get("/private")
async def private(auth_result: str = Security(auth.verify)):
    return Response(
        content={"message": "This is a private route."},
        status_code=200,
    )
    
import http.client

conn = http.client.HTTPSConnection("dev-wuq2xo0zcl2ekwq2.us.auth0.com")

payload = "{\"client_id\":\"EWfpT7il4pe63FxUHytjgpxb6ttloqbo\",\"client_secret\":\"AQACtS7wKlTCaVZgJ6TMtgB-A0yJC1Zew94aeCPUTtmCG-fXwl9Ph0tLF6FNuGZz\",\"audience\":\"https://sanquin-api.onrender.com/auth\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
