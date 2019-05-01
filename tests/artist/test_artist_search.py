import pytest
import qobuz
import responses

from tests.resources.responses import artist_search_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(query, limit=50, offset=0):
    return (
        qobuz.api.API_URL
        + "artist/search"
        + "?query={0}".format(query)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_search_empty():
    with responses.RequestsMock() as response_mock:
        url = get_url("")
        resp = {
            "query": "",
            "artists": {"limit": 50, "offset": 0, "total": 0, "items": []},
        }

        response_mock.add(
            responses.GET, url, json=resp, status=200, match_querystring=True
        )

        yield response_mock


@pytest.fixture
def response_search():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(artist_search_json["query"]),
            json=artist_search_json,
            status=200,
            match_querystring=True,
        )

        yield response_mock


def test_search_len(app, response_search):
    artists = qobuz.Artist.search(artist_search_json["query"])

    assert len(artists) != 0
    assert len(artists) == len(artist_search_json)


def test_search_found(app, response_search):
    artists = qobuz.Artist.search(artist_search_json["query"])

    assert artists[0].name == "MGMT"
    assert artists[0].picture is None
    assert artists[0].id == 118680
    assert artists[0].albums_count == 29
    assert artists[0].slug == "mgmt"


def test_search_empty(app, response_search_empty):
    artists = qobuz.Artist.search("")

    assert len(artists) == 0
