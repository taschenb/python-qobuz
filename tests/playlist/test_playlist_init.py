import qobuz
import responses

from tests.resources.responses import playlist_create_json


def test_playlist_init():
    playlist = qobuz.Playlist(playlist_create_json)

    assert playlist.id == playlist_create_json["id"]
    assert playlist.name == playlist_create_json["name"]
    assert playlist.description == playlist_create_json["description"]
