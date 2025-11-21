from typing import Annotated

from fastapi import Depends, HTTPException
from hashids import Hashids
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.endpoints.core.settings import Settings
from app.db.database import get_session
from app.db.models import URL
from app.schemas.schemas import URLCreate, URLResponse

setting = Settings()
Db = Annotated[Session, Depends(get_session)]
BASE_DOMAIN = 'https://meuencurtador.com/'
MIN_LENGTH = 5

hashids = Hashids(salt=setting.SECRET_KEY, min_length=MIN_LENGTH)


def create_url_record_and_get_id(
    url_data: URLCreate, user_id: int, db: Session
) -> URL:

    new_url = URL(
        original_url=str(url_data.url),
        short_code='TEMP',
        user_id=user_id,
        expires_at=None,
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

    url_record.clicks += 1
    db.commit()

    return url_record.original_url
