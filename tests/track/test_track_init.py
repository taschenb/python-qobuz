import pytest
import qobuz
import responses

from tests.resources.responses import track_search_json, artist_get_albums_json
from tests.resources.fixtures import artist, track


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def test_track_init(app):
    track_item = track_search_json["tracks"]["items"][0]

    track = qobuz.Track(track_item)

    assert track.id == track_item["id"]
    assert track.title == track_item["title"]
    assert track.album == qobuz.Album(track_item["album"])
    assert track.duration == track_item["duration"]
    assert track.media_number == track_item["media_number"]
    assert track.track_number == track_item["track_number"]


def test_track_type(app, track):
    assert track.type == "track"


def test_track_artist_lookup(app, track, artist):
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=qobuz.api.API_URL + "artist/get",
            json=artist_get_albums_json,
            status=200,
            match_querystring=False,
        )

        assert track.artist == qobuz.Artist(artist_get_albums_json)
