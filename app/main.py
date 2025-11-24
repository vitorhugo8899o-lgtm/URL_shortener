from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.url_route import routh
from app.api.endpoints.user_route import routh_auth

app = FastAPI()


app.include_router(routh_auth)
app.include_router(routh)
