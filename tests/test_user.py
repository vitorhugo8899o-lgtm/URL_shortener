from http import HTTPStatus


def test_create_user(client):

    response = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste85',
            'email': 'Email@st774ring.com',
            'password': 'senhasecreta',
        },
    )

    status = 201

    user = response.json()

    print(user)

    assert response.status_code == status
    assert 'username' in user
    assert 'email' in user
    assert 'id' in user


def test_username_exist(client):
    client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unico',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    response = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unico',
            'email': 'outro_email@test.com',
            'password': 'senhasecreta',
        },
    )

    status = 409

    assert response.status_code == status
    assert 'Username already in use' in response.json()['detail']


def test_email_exist(client):
    client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unic8o',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    response = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unico',
            'email': 'novo_email@test.com',
            'password': 'senhasecreta',
        },
    )

    status = 409

    assert response.status_code == status
    assert 'Email already in use' in response.json()['detail']


def test_create_token(client):
    create = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unic8o',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    print(create.json())

    response = client.post(
        '/auth/Login',
        data={'username': 'novo_email@test.com', 'password': 'secretpassword'},
    )

    status = 200

    assert response.status_code == status
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_information_invalide_email(client):
    create = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unic8o',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    print(create)

    response = client.post(
        '/auth/Login',
        data={
            'username': 'novo_email88@test.com',
            'password': 'secretpassword',
        },
    )

    status = 401

    assert response.status_code == status
    assert 'Invalid email or password' in response.json()['detail']


def test_information_invalide_password(client):
    create = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unic8o',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    print(create)

    response = client.post(
        '/auth/Login',
        data={
            'username': 'novo_email@test.com',
            'password': 'secret88password',
        },
    )

    status = 401

    assert response.status_code == status
    assert 'Invalid email or password' in response.json()['detail']


def test_alter_user(client, token):
    alter = {
        'username': 'Teste_Unic8o',
        'email': 'novo_email@test.com',
        'password': 'secretpassword',
    }

    response = client.put(
        '/auth/alter', headers={'Authorization': f'Bearer {token}'}, json=alter
    )

    response_data = response.json()
    assert 'Successful changes, welcome.' in response_data


def test_erro_current_user(client, token):
    alter = {
        'username': 'Teste_Unic8o',
        'email': 'novo_email@test.com',
        'password': 'secretpassword',
    }

    token = (
        'eyJhbGciOiJIUzI1NiI'
        'sInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwI'
        'joxNzYzNzY0OTM3fQ.'
        '_sfixfpQSxptnq0fmz_BNC89-88DJrggStwkrlS4COI'
    )

    response = client.put(
        '/auth/alter', headers={'Authorization': f'Bearer {token}'}, json=alter
    )

    status = 401

    response_data = response.json()
    assert response.status_code == status
    assert response_data['detail'] == 'Invalid token'


def test_decode_token_erro(client):
    alter = {
        'username': 'Teste_Unic8o',
        'email': 'novo_email@test.com',
        'password': 'secretpassword',
    }

    token = 'shgdoasdbaosdb.342134sdfdsff.q3sadbs'

    response = client.put(
        '/auth/alter', headers={'Authorization': f'Bearer {token}'}, json=alter
    )

    status = 401

    response_data = response.json()
    assert response.status_code == status
    assert response_data['detail'] == 'Invalid token'


def test_alter_email_exist(client, token):
    create = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unic8o',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    print(create)

    alter = {
        'username': 'Teste_Unic8o',
        'email': 'novo_email@test.com',
        'password': 'secretpassword',
    }

    response = client.put(
        '/auth/alter', headers={'Authorization': f'Bearer {token}'}, json=alter
    )

    response_data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response_data['detail'] == 'Email already in use'


def test_alter_username_exist(client, token):
    create = client.post(
        '/auth/Registry',
        json={
            'username': 'Teste_Unic8o',
            'email': 'novo_email@test.com',
            'password': 'secretpassword',
        },
    )

    print(create)

    alter = {
        'username': 'Teste_Unic8o',
        'email': 'novo_email7@test.com',
        'password': 'secretpassword',
    }

    response = client.put(
        '/auth/alter', headers={'Authorization': f'Bearer {token}'}, json=alter
    )

    response_data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response_data['detail'] == 'Username already in use'


def test_delete_user(client, token):

    response = client.delete(
        '/auth/delete', headers={'Authorization': f'Bearer {token}'}
    )

    response_data = response.json()

    status = 200

    assert response.status_code == status
    assert response_data['detail'] == 'User successfully deleted!'
