import pytest
import qobuz
import responses

from tests.resources.responses import playlist_search_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(query, limit=50, offset=0):
    return (
        qobuz.api.API_URL
        + "playlist/search"
        + "?query={0}".format(query)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_search():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(playlist_search_json["query"]),
            json=playlist_search_json,
            status=200,
            match_querystring=True,
        )

        yield response_mock


def test_search_len(app, response_search):
    playlists = qobuz.Playlist.search(playlist_search_json["query"])

    assert len(playlists) != 0
    assert len(playlists) == len(playlist_search_json["playlists"]["items"])


def test_search_content(app, response_search):
    playlists = qobuz.Playlist.search(playlist_search_json["query"])
    playlists_resp = playlist_search_json["playlists"]["items"]

    assert playlists[0].id == playlists_resp[0]["id"]
    assert playlists[0].name == playlists_resp[0]["name"]
    assert playlists[0].description == playlists_resp[0]["description"]
