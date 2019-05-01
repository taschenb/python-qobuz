import pytest
import qobuz
import responses

from tests.resources.fixtures import user
from tests.resources.responses import playlist_create_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_playlist_create_url(
    name, description=None, is_public=False, is_collaborative=False
):
    return (
        qobuz.api.API_URL
        + "playlist/create"
        + "?name={}".format(name)
        + "&is_public={}".format(is_public)
        + "&is_collaborative={}".format(is_collaborative)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_playlist_create():
    resp = playlist_create_json
    url = get_playlist_create_url(
        name=resp["name"],
        description=resp["description"],
        is_public=resp["is_public"],
        is_collaborative=resp["is_collaborative"],
    )

    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=url,
            json=resp,
            status=200,
            match_querystring=False,
        )

        yield response_mock


def test_user_playlist_create(app, user, response_playlist_create):
    resp = playlist_create_json
    playlist = user.playlist_create(
        name=resp["name"],
        description=resp["description"],
        is_public=resp["is_public"],
        is_collaborative=resp["is_collaborative"],
    )

    assert isinstance(playlist, qobuz.Playlist)
    assert playlist.id == resp["id"]
    assert playlist.name == resp["name"]
