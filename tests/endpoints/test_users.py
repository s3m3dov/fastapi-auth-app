from fastapi.testclient import TestClient

from core import settings
from main import app

from crud.user import get_by_email


client = TestClient(app)


def test_create_user() -> None:
    signup_data = {
        "email": settings.TEST_EMAIL,
        "password": settings.TEST_PASSWORD,
        "fullname": settings.TEST_FULLNAME
    }

    if get_by_email(settings.TEST_EMAIL):
        status_code_should_be = 400
    else:
        status_code_should_be = 200

    response = client.post(f"{settings.API_V1_STR}/signup/", json=signup_data)
    assert response.status_code == status_code_should_be

    if response.status_code == 200:
        content = response.json()
        assert "id" in content


def test_login() -> None:
    response = client.post(f"{settings.API_V1_STR}/login/", json=settings.TEST_LOGIN_DATA)
    assert response.status_code == 200

    tokens = response.json()

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["access_token"]
    assert tokens["refresh_token"]


def test_refresh_user_token() -> None:
    response = client.post(f"{settings.API_V1_STR}/login/", json=settings.TEST_LOGIN_DATA)
    tokens = response.json()

    old_access_token = tokens["access_token"]

    response = client.post(f"{settings.API_V1_STR}/refresh/", data=tokens)
    assert response.status_code == 200

    tokens = response.json()

    assert "access_token" in tokens
    assert tokens["access_token"]

    new_access_token = tokens["access_token"]
    assert new_access_token != old_access_token


def test_user_details() -> None:
    response = client.post(f"{settings.API_V1_STR}/login/", json=settings.TEST_LOGIN_DATA)
    tokens = response.json()

    response = client.get(f"{settings.API_V1_STR}/user/", data=tokens)
    assert response.status_code == 200

    content = response.json()
    assert "email" in content
    assert content["email"] == settings.TEST_EMAIL
    assert "fullname" in content
    assert content["fullname"] == settings.TEST_FULLNAME


def test_logout() -> None:
    response = client.post(f"{settings.API_V1_STR}/login/", json=settings.TEST_LOGIN_DATA)
    tokens = response.json()

    response = client.delete(f"{settings.API_V1_STR}/logout/", data=tokens)

    assert response.status_code == 200

    message = response.json()["msg"]
    assert message == "Successfully logged out."
