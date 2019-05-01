import pytest
import qobuz
import responses

from tests.resources.responses import playlist_create_json
from tests.resources.fixtures import playlist


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(playlist_id):
    return (
        qobuz.api.API_URL
        + "playlist/get"
        + "?playlist_id={}".format(playlist_id)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def test_playlist_init(app):
    playlist = qobuz.Playlist(playlist_create_json)

    assert playlist.id == playlist_create_json["id"]
    assert playlist.name == playlist_create_json["name"]
    assert playlist.description == playlist_create_json["description"]


def test_playlist_from_id(app, playlist):
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(playlist.id),
            json=playlist_create_json,
            status=200,
            match_querystring=True,
        )

        playlist_from_id = qobuz.Playlist.from_id(playlist.id)

    assert playlist_from_id == playlist
