import pytest
import qobuz
import responses

from tests.resources.responses import artist_search_json
from tests.resources.fixtures import artist


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(artist_id):
    return (
        qobuz.api.API_URL
        + "artist/get"
        + "?artist_id={}".format(artist_id)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def test_artist_init(app):
    artist_item = artist_search_json["artists"]["items"][0]

    artist = qobuz.Artist(artist_item)

    assert artist.id == artist_item["id"]
    assert artist.name == artist_item["name"]
    assert artist.picture == artist_item["picture"]
    assert artist.slug == artist_item["slug"]
    assert artist.albums_count == artist_item["albums_count"]


def test_artist_from_id(app):
    artist_item = artist_search_json["artists"]["items"][0]

    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(artist_item["id"]),
            json=artist_item,
            status=200,
            match_querystring=True,
        )

        artist_from_id = qobuz.Artist.from_id(artist_item["id"])

    assert artist_from_id == qobuz.Artist(artist_item)


def test_artist_type(app, artist):
    assert artist.type == "artist"
