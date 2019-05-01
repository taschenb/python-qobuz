import pytest
import qobuz
import responses

from tests.resources.responses import album_search_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(query, limit=50, offset=0):
    return (
        qobuz.api.API_URL
        + "album/search"
        + "?query={}".format(query)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def albums_search_result():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(album_search_json["query"]),
            json=album_search_json,
            status=200,
            match_querystring=True,
        )

        yield qobuz.Album.search(album_search_json["query"])


def test_album_search_len(app, albums_search_result):
    assert len(albums_search_result) > 0


def test_album_search_type(app, albums_search_result):
    for album in albums_search_result:
        assert isinstance(album, qobuz.Album)


def test_album_search_content(app, albums_search_result):
    id = album_search_json["albums"]["items"][0]["id"]
    title = album_search_json["albums"]["items"][0]["title"]
    tracks_count = album_search_json["albums"]["items"][0]["tracks_count"]
    released_at = album_search_json["albums"]["items"][0]["released_at"]

    assert albums_search_result[0].id == id
    assert albums_search_result[0].title == title
    assert albums_search_result[0].tracks_count == tracks_count
    assert albums_search_result[0].released_at == released_at
