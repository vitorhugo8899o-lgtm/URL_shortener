from http import HTTPStatus

from app.db.models import URL


def test_create_url_short(client, token):
    response = client.post(
        '/shorther_url/create_url',
        headers={'Authorization': f'Bearer {token}'},
        json={'url': 'https://youtu.be/ufAmIBRFohM?si=KDc-ijsQhj9Uqle-'},
    )

    status = HTTPStatus.CREATED

    json = response.json()

    print(json['short_code'])

    assert response.status_code == status
    assert 'short_code' in json
    assert 'id' in json
    assert 'original_url' in json


def test_get_url_by_short_code_success(url, session):

    retrieved_url = session.get(URL, url.id)

    assert retrieved_url is not None
    assert retrieved_url.short_code == url.short_code
    assert retrieved_url.original_url == 'https://www.example.com/long-page'


def test_redirect_url_success(client, url, session, token):

    redirect_path = f'/shorther_url/{url.short_code}'

    response = client.get(
        redirect_path,
        headers={'Authorization': f'Bearer {token}'},
        follow_redirects=False,
    )

    status = 307

    assert response.status_code == status

    assert response.headers['location'] == url.original_url

    session.refresh(url)
    assert url.clicks == 1


def test_redirect_url_not_found(client, token):

    non_existent_code = 'NAO_EXISTE'
    redirect_path = f'/shorther_url/{non_existent_code}'

    response = client.get(
        redirect_path,
        headers={'Authorization': f'Bearer {token}'},
        follow_redirects=False,
    )

    status = 404

    assert response.status_code == status
    assert response.json() == {'detail': 'URL not found'}


def test_get_urls_user(client, token):
    url = client.post(
        '/shorther_url/create_url',
        headers={'Authorization': f'Bearer {token}'},
        json={'url': 'https://youtu.be/ufAmIBRFohM?si=KDc-ijsQhj9Uqle-'},
    )

    print(url)

    response = client.get(
        '/shorther_url/get_my_urls',
        headers={'Authorization': f'Bearer {token}'},
    )

    json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'urls' in json


def test_delete_url(client, token):
    create = client.post(
        '/shorther_url/create_url',
        headers={'Authorization': f'Bearer {token}'},
        json={'url': 'https://youtu.be/ufAmIBRFohM?si=KDc-ijsQhj9Uqle-'},
    )

    print(create.json())

    data = create.json()

    url_id = data['id']

    assert isinstance(url_id, int)

    response = client.delete(
        f'/shorther_url/Delete_URL?url_id={url_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'URL successfully delete!' in response.json()['message']


def test_url_delete_not_found(client, token):
    response = client.delete(
        f'/shorther_url/Delete_URL?url_id={12}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'Url not found' in response.json()['detail']


def test_same_url(client, token):
    create1 = client.post(
        '/shorther_url/create_url',
        headers={'Authorization': f'Bearer {token}'},
        json={'url': 'https://youtu.be/ufAmIBRFohM?si=KDc-ijsQhj9Uqle-'},
    )

    print(create1)

    create2 = client.post(
        '/shorther_url/create_url',
        headers={'Authorization': f'Bearer {token}'},
        json={'url': 'https://youtu.be/ufAmIBRFohM?si=KDc-ijsQhj9Uqle-'},
    )

    assert create2.status_code == HTTPStatus.CONFLICT
    assert 'Url already exists' in create2.json()['detail']
