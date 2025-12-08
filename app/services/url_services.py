from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from hashids import Hashids
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.endpoints.core.settings import Settings
from app.db.database import get_session
from app.db.models import URL, User
from app.schemas.schemas import URLCreate, URLResponse

setting = Settings()
Db = Annotated[Session, Depends(get_session)]
BASE_DOMAIN = 'https://meuencurtador.com/'
MIN_LENGTH = 5

hashids = Hashids(salt=setting.SECRET_KEY, min_length=MIN_LENGTH)


def create_url_record_and_get_id(
    url_data: URLCreate, user_id: int, db: Session
) -> URL:

    url_str = str(url_data.url) 

    condition = (URL.original_url == url_str)


    query_result = db.execute(select(URL).where(condition)).first()
    
    if query_result:
        existing_url = query_result[0] 
        raise HTTPException(status_code=409, detail="Url already exists")

    new_url = URL(
        original_url=str(url_data.url),
        short_code='TEMP',
        user_id=user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    )

    db.add(new_url)
    db.flush()

    return new_url


def update_url_short_code(
    db: Session, url_record: URL, short_code: str
) -> URL:

    url_record.short_code = short_code
    return url_record


def create_short_url(
    db: Session, url_data: URLCreate, user_id: int
) -> URLResponse:

    try:
        url_record = create_url_record_and_get_id(url_data, user_id, db)
        url_id = url_record.id

        short_code = hashids.encode(url_id)

        final_record = update_url_short_code(db, url_record, short_code)

        db.commit()

        return URLResponse(
            id=final_record.id,
            short_code=short_code,
            original_url=final_record.original_url,
        )

    except Exception:  # pragma: no cover
        db.rollback()
        raise


def get_url_shorter(db: Db, short_code: str) -> str:
    stmt = select(URL).where(URL.short_code == short_code)
    url_record = db.execute(stmt).scalar_one_or_none()

    if not url_record:
        raise HTTPException(status_code=404, detail='URL not found')

    now = datetime.now(timezone.utc)
    if url_record.expires_at and url_record.expires_at.replace(tzinfo=timezone.utc) < now:
        raise HTTPException(status_code=410, detail='Expired url')

    url_record.clicks += 1
    db.commit()

    return url_record.original_url


def get_url_user(current_user: User, db: Session):
    stmt = select(URL).where(URL.user_id == current_user.id)
    urls = db.execute(stmt).scalars().all()

    return {'urls': urls}


def delete_url_user(current_user: User, db: Session, id_url: int):
    stmt = select(URL).where(
    (URL.id == id_url) & (URL.user_id == current_user.id)
)

    url = db.scalar(stmt)

    if not url:
        raise HTTPException(status_code=404,detail='Url not found')
    
    db.delete(url)
    db.commit()

    return {'detail': 'URL successfully delete!'}