import pytest
import qobuz
import responses

from tests.resources.responses import album_featured_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(type, limit=50, offset=0):
    return (
        qobuz.api.API_URL
        + "album/getFeatured"
        + "?type={}".format(type)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def albums_featured_result():
    featured_type = "new_releases"
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(featured_type),
            json=album_featured_json,
            status=200,
            match_querystring=True,
        )

        yield qobuz.Album.get_featured(featured_type)


def test_album_featured_len(app, albums_featured_result):
    assert len(albums_featured_result) > 0


def test_album_featured_type(app, albums_featured_result):
    for album in albums_featured_result:
        assert isinstance(album, qobuz.Album)


def test_album_featured_content(app, albums_featured_result):
    id = album_featured_json["albums"]["items"][0]["id"]
    title = album_featured_json["albums"]["items"][0]["title"]
    tracks_count = album_featured_json["albums"]["items"][0]["tracks_count"]
    released_at = album_featured_json["albums"]["items"][0]["released_at"]

    assert albums_featured_result[0].id == id
    assert albums_featured_result[0].title == title
    assert albums_featured_result[0].tracks_count == tracks_count
    assert albums_featured_result[0].released_at == released_at
