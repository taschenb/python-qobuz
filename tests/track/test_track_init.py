import qobuz

from tests.resources.responses import track_search_json


qobuz.api.APP_ID = "request_from_api@qobuz.com"


def test_track_init():
    track_item = track_search_json["tracks"]["items"][0]

    track = qobuz.Track(track_item)

    assert track.id == track_item["id"]
    assert track.title == track_item["title"]
    assert track.album == qobuz.Album(track_item["album"])
