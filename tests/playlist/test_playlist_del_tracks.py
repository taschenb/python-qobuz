import pytest
import qobuz
import responses

from tests.resources.fixtures import user, playlist
from tests.resources.responses import playlist_get_tracks_json
from tests.resources.responses import playlist_add_tracks_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(playlist_id, user_auth_token, track_ids=""):
    return (
        qobuz.api.API_URL
        + "playlist/deleteTracks"
        + "?playlist_id={}".format(playlist_id)
        + "&track_ids={}".format(track_ids)
        + "&user_auth_token={}".format(user_auth_token)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def test_playlist_del_tracks(app, playlist, user):
    track_ids = ",".join(
        [str(t["id"]) for t in playlist_get_tracks_json["tracks"]["items"]]
    )

    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            get_url(
                playlist_id=playlist_add_tracks_json["id"],
                user_auth_token=user.auth_token,
                track_ids=track_ids,
            ),
            json={"status": "success"},
            status=200,
            match_querystring=True,
        )

        tracks = [
            qobuz.Track(t) for t in playlist_get_tracks_json["tracks"]["items"]
        ]

        # Match playlist-ids to add to the correct id
        playlist.id = playlist_add_tracks_json["id"]

        playlist.del_tracks(tracks, user)
