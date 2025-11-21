from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import decode, encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.endpoints.core.settings import Settings
from app.db.database import get_session
from app.db.models import User
from app.schemas.schemas import Token, UserRegistry

oauth = OAuth2PasswordBearer(tokenUrl='/auth/Login')
setting = Settings()
Form_data = Annotated[OAuth2PasswordRequestForm, Depends()]

ph = PasswordHasher()


def hash_password(senha):
    return ph.hash(senha)


def verify_password(password: str, db_password: str):
    try:
        ph.verify(hash=db_password, password=password)
        return True

    except VerificationError:
        return False

    except Exception:  # pragma: no cover
        return False


def user_exist(user_data: UserRegistry, db: Session = Depends(get_session)):

    condition = (User.email == user_data.email) | (
        User.username == user_data.username
    )

    result = db.execute(select(User).where(condition))

    found_user = result.scalar_one_or_none()

    if found_user:
        if found_user.email == user_data.email:
            raise HTTPException(status_code=409, detail='Email already in use')
        if found_user.username == user_data.username:
            raise HTTPException(
                status_code=409, detail='Username already in use'
            )

    return user_data


async def registry_user(
    db: Session = Depends(get_session),
    user_data: UserRegistry = Depends(user_exist),
):

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def crete_token_acesses(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=setting.ACESSES_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, setting.SECRET_KEY, setting.ALGORITHM)
    return encode_jwt


def verifying_credentials(
    form_data: Form_data,
    db: Session = Depends(get_session),
):

    user = db.execute(
        select(User).where(User.email == form_data.username)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401, detail='Invalid email or password'
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401, detail='Invalid email or password'
        )

    access_token = crete_token_acesses(data={'sub': user.email})

    token = Token(access_token=access_token, token_type='Bearer')

    return token


def get_current_user(
    token: str = Depends(oauth), db: Session = Depends(get_session)
):

    try:
        payload = decode(
            token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM]
        )
        email_user = payload.get('sub')
        if not email_user:
            raise HTTPException(401, 'Invalid token')

    except (DecodeError, ExpiredSignatureError):
        raise HTTPException(401, 'Invalid token')

    user = db.execute(
        select(User).where(User.email == email_user)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(401, 'Invalid token')

    return user


def alter_user_information(
    user_data: UserRegistry,
    current_user: User,
    db: Session = Depends(get_session),
):
    try:
        if user_data.email != current_user.email:
            existing_user_by_email = db.execute(
                select(User).where(User.email == user_data.email)
            ).scalar_one_or_none()

            if existing_user_by_email:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Email already in use',
                )

        if user_data.username != current_user.username:
            existing_user_by_username = db.execute(
                select(User).where(User.username == user_data.username)
            ).scalar_one_or_none()

            if existing_user_by_username:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Username already in use',
                )

        current_user.email = user_data.email
        current_user.username = user_data.username

        if user_data.password:
            current_user.password = hash_password(user_data.password)

        db.commit()
        db.refresh(current_user)

        return 'Successful changes, welcome.'

    except HTTPException:
        raise

    except Exception as e:  # pragma: no cover
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Internal Error: {str(e)}',
        )


def delete_user_bd(
    user_data: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):

    user = db.execute(
        select(User).where(User.email == user_data.email)
    ).scalar_one_or_none()

    if not user:  # pragma: no cover
        raise HTTPException(409, 'User not found!')

    db.delete(user)
    db.commit()

    return {'detail': 'User successfully deleted!'}
