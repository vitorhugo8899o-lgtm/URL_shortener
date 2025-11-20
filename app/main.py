from fastapi import FastAPI

from app.api.endpoints.user_route import routh_auth

app = FastAPI()
app.include_router(routh_auth)
