from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.schemas import Token, UserRegistry
from app.services.user_service import registry_user, verifying_credentials

routh_auth = APIRouter(prefix='/auth')


@routh_auth.post('/Registry', status_code=HTTPStatus.CREATED)
async def create_user(user: Annotated[UserRegistry, Depends(registry_user)]):
    return user


@routh_auth.post('/Login', status_code=HTTPStatus.OK, response_model=Token)
def login_user(token: Annotated[Token, Depends(verifying_credentials)]):
    return token
