from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.db.models import User
from app.schemas.schemas import URLCreate, URlList, URLResponse
from app.services.url_services import (
    create_short_url,
    get_url_shorter,
    get_url_user,
)
from app.services.user_service import get_current_user

routh = APIRouter(prefix='/shorther_url', tags=['URLS'])
Db = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routh.post(
    '/get_url', status_code=HTTPStatus.CREATED, response_model=URLResponse
)
def create_url_short_for_user(
    url: URLCreate, current_user: CurrentUser, db: Db
):

    return create_short_url(db=db, url_data=url, user_id=current_user.id)


@routh.get('/get_my_urls', status_code=HTTPStatus.OK, response_model=URlList)
def show_my_urls(current_user: CurrentUser, db: Db):
    return get_url_user(current_user, db)


@routh.get('/{short_code}')
def redirect_to_original_url(
    current_user: CurrentUser, short_code: str, db: Db
):

    original_url = get_url_shorter(db, short_code)

    return RedirectResponse(url=original_url, status_code=307)
