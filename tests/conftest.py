import pytest
from fastapi.testclient import TestClient
from hashids import Hashids
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.models import URL, User, table_registry
from app.main import app
from app.services.user_service import get_session, hash_password


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def override_get_session(session):
    def get_session_override():

        return session

    return get_session_override


@pytest.fixture
def client(override_get_session):

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client_test:
        yield client_test

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    raw_password = 'teste'
    user = User(
        username='teste@',
        email='teste@gmail.com',
        password=hash_password(raw_password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user, raw_password


@pytest.fixture
def token(client, user):
    user, raw_password = user

    login_data = {
        'username': user.email,
        'password': raw_password,
    }

    response = client.post('/auth/Login', data=login_data)
    return response.json()['access_token']


@pytest.fixture
def url(session, user):

    new_url = URL(
        original_url='https://www.example.com/long-page',
        short_code='TEMP',
        user_id=1,
        expires_at=None,
    )

    session.add(new_url)
    session.flush()

    hashids_instance = Hashids(salt='secret_key', min_length=5)
    short_code = hashids_instance.encode(new_url.id)

    new_url.short_code = short_code
    session.commit()
    session.refresh(new_url)

    return new_url
