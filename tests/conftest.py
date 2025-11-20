import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.models import User, table_registry
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
    raw_password = 'teste'  # A senha original
    user = User(
        username='teste@',
        email='teste@gmail.com',
        # Hasheia a senha para armazenar no banco
        password=hash_password(raw_password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Retorna o objeto User E a senha original
    return user, raw_password


@pytest.fixture
def token(client, user):
    # Desempacota o User e a senha original
    user, raw_password = user

    login_data = {
        'username': user.email,
        'password': raw_password,  # Usa a senha original
    }

    response = client.post('/auth/Login', data=login_data)
    return response.json()['access_token']
