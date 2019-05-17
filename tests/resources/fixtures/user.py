import json
import pytest
import qobuz
import responses

from tests.user.test_user_login import get_url
from tests.resources.responses import user_login_json


@pytest.fixture
def user():
    username = "username"
    password = "password"

    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(username, password, None),
            json=user_login_json,
            status=200,
            match_querystring=False,
        )

        return qobuz.User(username, password)
