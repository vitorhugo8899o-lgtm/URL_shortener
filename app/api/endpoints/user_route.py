from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.schemas import Token, UserRegistry
from app.services.user_service import (
    alter_user_information,
    delete_user_bd,
    get_current_user,
    get_session,
    registry_user,
    verifying_credentials,
)

routh_auth = APIRouter(prefix='/auth')
CurrentUser = Annotated[User, Depends(get_current_user)]
Db = Annotated[Session, Depends(get_session)]


@routh_auth.post('/Registry', status_code=HTTPStatus.CREATED)
async def create_user(user: Annotated[UserRegistry, Depends(registry_user)]):
    return user


@routh_auth.post('/Login', status_code=HTTPStatus.OK, response_model=Token)
def login_user(token: Annotated[Token, Depends(verifying_credentials)]):
    return token


@routh_auth.put('/alter', status_code=HTTPStatus.OK)
def alter_information(
    user_data: UserRegistry, current_user: CurrentUser, db: Db
):
    return alter_user_information(
        user_data=user_data, current_user=current_user, db=db
    )


@routh_auth.delete('/delete', status_code=HTTPStatus.OK)
def delete_user(current_user: CurrentUser, db: Db):

    return delete_user_bd(user_data=current_user, db=db)
