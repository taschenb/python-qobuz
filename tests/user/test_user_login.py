import pytest
import qobuz
import responses

from tests.resources.responses import user_login_json


qobuz.api.APP_ID = "request_from_api@qobuz.com"


USERNAME = user_login_json["user"]["login"]
AUTH_TOKEN = user_login_json["user_auth_token"]
PASSWORD = "123456789"


def get_url(username, password):
    return (
        qobuz.api.API_URL
        + "user/login"
        + "?username={}".format(username)
        + "&password={}".format(qobuz.User._hash_password(password))
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_login():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(USERNAME, PASSWORD),
            json=user_login_json,
            status=200,
            match_querystring=True,
        )

        yield response_mock


@pytest.fixture
def user(response_login):
    return qobuz.User(USERNAME, PASSWORD)


def test_user_password_hashing():
    pwd = {"plain": "123456789", "md5": "25f9e794323b453885f5181f1b624d0b"}

    assert qobuz.User._hash_password(pwd["plain"]) == pwd["md5"]


def test_user_login(response_login):
    user = qobuz.User(USERNAME, PASSWORD)

    assert user.username == USERNAME
    assert user.auth_token == user_login_json["user_auth_token"]
