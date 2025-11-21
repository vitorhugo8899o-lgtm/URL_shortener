from http import HTTPStatus

from app.db.models import URL


def test_create_url_short(client, token):
    response = client.post(
        '/shorther_url/get_url',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'url': 'https://gemini.google.com/app/68cbce004f96d4f1?hl=pt-BR'
        },
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
