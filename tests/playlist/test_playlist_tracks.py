import pytest
import qobuz
import responses

from tests.resources.responses import playlist_get_tracks_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(playlist_id, limit=50, offset=0, extra=None):
    return (
        qobuz.api.API_URL
        + "playlist/get"
        + "?extra={}".format(extra)
        + "&playlist_id={}".format(playlist_id)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_playlist_tracks():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            get_url(
                playlist_id=playlist_get_tracks_json["id"], extra="tracks"
            ),
            json=playlist_get_tracks_json,
            status=200,
            match_querystring=True,
        )
        yield response_mock


@pytest.fixture
def playlist_item():
    return {
        "id": playlist_get_tracks_json["id"],
        "name": playlist_get_tracks_json["name"],
        "description": playlist_get_tracks_json["description"],
        "tracks_count": 0,
        "users_count": 0,
        "duration": 0,
        "created_at": 1431679485,
        "updated_at": 1431679485,
        "is_public": True,
        "is_collaborative": False,
        "owner": {"id": 12345, "name": "loris"},
    }


def test_playlist_tracks_len(app, playlist_item, response_playlist_tracks):
    playlist = qobuz.Playlist(playlist_item)

    assert len(playlist.get_tracks()) == 2


def test_playlist_tracks_type(app, playlist_item, response_playlist_tracks):
    playlist = qobuz.Playlist(playlist_item)

    for t in playlist.get_tracks():
        assert isinstance(t, qobuz.Track)


def test_playlist_tracks_conntent(app, playlist_item, response_playlist_tracks):
    playlist = qobuz.Playlist(playlist_item)
    tracks = playlist.get_tracks()

    track_items = playlist_get_tracks_json["tracks"]["items"]

    assert tracks[0].id == track_items[0]["id"]
    assert tracks[0].title == track_items[0]["title"]
    assert tracks[0].album == qobuz.Album(track_items[0]["album"])
    assert tracks[1].id == track_items[1]["id"]
    assert tracks[1].title == track_items[1]["title"]
    assert tracks[1].album == qobuz.Album(track_items[1]["album"])
