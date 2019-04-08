import qobuz

from tests.resources.responses import artist_search_json
from tests.resources.fixtures import artist


def test_artist_init():
    artist_item = artist_search_json["artists"]["items"][0]

    artist = qobuz.Artist(artist_item)

    assert artist.id == artist_item["id"]
    assert artist.name == artist_item["name"]
    assert artist.picture == artist_item["picture"]
    assert artist.slug == artist_item["slug"]
    assert artist.albums_count == artist_item["albums_count"]
