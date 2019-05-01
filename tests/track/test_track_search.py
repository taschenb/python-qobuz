import pytest
import qobuz
import responses

from tests.resources.responses import track_search_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(query, limit=50, offset=0):
    return (
        qobuz.api.API_URL
        + "track/search"
        + "?query={}".format(query)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_track_search():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            get_url(query=track_search_json["query"]),
            json=track_search_json,
            status=200,
            match_querystring=True,
        )
        yield response_mock


def test_track_search_len(app, response_track_search):
    tracks = qobuz.Track.search(track_search_json["query"])

    assert len(tracks) == len(track_search_json["tracks"]["items"])


def test_track_search_type(app, response_track_search):
    tracks = qobuz.Track.search(track_search_json["query"])

    for t in tracks:
        assert isinstance(t, qobuz.Track)


def test_track_search_content(app, response_track_search):
    tracks = qobuz.Track.search(track_search_json["query"])

    track_items = track_search_json["tracks"]["items"]
    assert tracks[0] == qobuz.Track(track_items[0])
    assert tracks[1] == qobuz.Track(track_items[1])
