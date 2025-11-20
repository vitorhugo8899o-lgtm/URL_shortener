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
        json={'email': 'novo_email@test.com', 'password': 'secretpassword'},
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
        json={'email': 'novo_email88@test.com', 'password': 'secretpassword'},
    )

    status = 401

    assert response.status_code == status
    assert "Invalid email or password" in response.json()['detail']


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
        json={'email': 'novo_email@test.com', 'password': 'secret88password'},
    )

    status = 401

    assert response.status_code == status
    assert "Invalid email or password" in response.json()['detail']
