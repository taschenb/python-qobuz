# -*- coding: utf-8 -*-
import pytest
import qobuz
import responses

from tests.resources.responses import artist_get_albums_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_url(artist_id, offset=0, limit=50):
    return (
        qobuz.api.API_URL
        + "artist/get"
        + "?artist_id={}".format(artist_id)
        + "&extra={}".format("albums")
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_all_albums():
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_url(artist_get_albums_json["id"]),
            json=artist_get_albums_json,
            status=200,
            match_querystring=True,
        )
        yield response_mock


def test_artist_albums_len(app, response_all_albums):
    artist = qobuz.Artist(artist_get_albums_json)

    assert len(artist.get_all_albums()) == 25


def test_artist_albums_type(app, response_all_albums):
    artist = qobuz.Artist(artist_get_albums_json)

    for a in artist.get_all_albums():
        assert isinstance(a, qobuz.Album)


def test_artist_album_content(app, response_all_albums):
    artist = qobuz.Artist(artist_get_albums_json)

    albums = artist.get_all_albums()

    assert albums[0].id == "0886443927087"
    assert albums[0].title == u"Random Access Memories (Édition Studio Masters)"
    assert albums[0].tracks_count == 13
    assert albums[0].released_at == 1368741600


def test_artist_album_artist(app, response_all_albums):
    artist = qobuz.Artist(artist_get_albums_json)

    albums = artist.get_all_albums()

    for a in albums:
        assert isinstance(a.artist, qobuz.Artist)

    assert albums[0].artist.name == "Daft Punk"
    assert albums[0].artist.id == 36819
    assert albums[0].artist.picture is None
    assert albums[0].artist.slug == "daft-punk"
    assert albums[0].artist.albums_count == 52
