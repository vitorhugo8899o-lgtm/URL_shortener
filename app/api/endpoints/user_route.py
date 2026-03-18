from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.schemas import Message, Token, UserPublic, UserRegistry
from app.services.user_service import (
    alter_user_information,
    delete_user_bd,
    get_current_user,
    get_session,
    registry_user,
    verifying_credentials,
)

routh_auth = APIRouter(prefix='/users', tags=['Users'])
CurrentUser = Annotated[User, Depends(get_current_user)]
Db = Annotated[Session, Depends(get_session)]


@routh_auth.post(
    '/Registry', status_code=HTTPStatus.CREATED
)
async def create_user(user: Annotated[UserRegistry, Depends(registry_user)]) -> UserPublic:  # noqa: E501
    return UserPublic.model_validate(user)


@routh_auth.post('/Login', status_code=HTTPStatus.OK)
def login_user(token: Annotated[Token, Depends(verifying_credentials)]) -> Token:  # noqa: E501
    return Token.model_validate(token)


@routh_auth.put('/me', status_code=HTTPStatus.OK)
def alter_information(
    user_data: UserRegistry,
    current_user: CurrentUser,
    db: Db
) -> Message:
    return alter_user_information(
        user_data=user_data, current_user=current_user, db=db
    )


@routh_auth.delete(
    '/me', status_code=HTTPStatus.OK,
)
def delete_user(current_user: CurrentUser, db: Db) -> Message:

    return delete_user_bd(user_data=current_user, db=db)
