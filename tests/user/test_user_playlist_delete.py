import pytest
import qobuz
import responses

from tests.resources.fixtures import user, playlist
from tests.resources.responses import playlist_get_tracks_json
from tests.resources.responses import playlist_add_tracks_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(playlist_id, user_auth_token):
    return (
        qobuz.api.API_URL
        + "playlist/delete"
        + "?playlist_id={}".format(playlist_id)
        + "&user_auth_token={}".format(user_auth_token)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def test_playlist_delete(app, playlist, user):
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            get_url(playlist_id=playlist.id, user_auth_token=user.auth_token),
            json={"status": "success"},
            status=200,
            match_querystring=True,
        )

        assert user.playlist_delete(playlist)
