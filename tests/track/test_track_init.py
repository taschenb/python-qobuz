import qobuz

from tests.resources.responses import track_search_json


qobuz.api.APP_ID = "request_from_api@qobuz.com"


def test_track_init():
    track_item = track_search_json["tracks"]["items"][0]

    track = qobuz.Track(track_item)

    assert track.id == track_item["id"]
    assert track.title == track_item["title"]
    assert track.album == qobuz.Album(track_item["album"])


def test_track_artist_lookup(track, artist):
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=qobuz.api.API_URL + "artist/get",
            json=artist_get_albums_json,
            status=200,
            match_querystring=False,
        )

        assert track.artist == qobuz.Artist(artist_get_albums_json)
