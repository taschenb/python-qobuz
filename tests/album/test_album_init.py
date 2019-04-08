import qobuz
import responses

from tests.resources.responses import album_get_json


def test_album_init():
    album = qobuz.Album(album_get_json)

    assert album.id == album_get_json["id"]
    assert album.title == album_get_json["title"]
    assert album.tracks_count == album_get_json["tracks_count"]
    assert album.released_at == album_get_json["released_at"]
    assert album.artist == qobuz.Artist(album_get_json["artist"])
