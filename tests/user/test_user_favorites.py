import pytest
import qobuz
import responses

from tests.resources.fixtures import user, album
from tests.resources.responses import user_fav_get_albums_json


@pytest.fixture
def app():
    qobuz.api.register_app(app_id="request_from_api@qobuz.com")


def get_favorite_albums_url(user_auth_token, fav_type="albums",
                            limit=50, offset=0):
    return (
        qobuz.api.API_URL
        + "favorite/getUserFavorites"
        + "?type={}".format(fav_type)
        + "&limit={}".format(limit)
        + "&offset={}".format(offset)
        + "&user_auth_token={}".format(user_auth_token)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def get_favorite_add_albums_url(album_ids, user_auth_token):
    return (
        qobuz.api.API_URL
        + "favorite/create"
        + "?album_ids={}".format(album_ids)
        + "&user_auth_token={}".format(user_auth_token)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def get_favorite_del_albums_url(album_ids, user_auth_token):
    return (
        qobuz.api.API_URL
        + "favorite/delete"
        + "?album_ids={}".format(album_ids)
        + "&user_auth_token={}".format(user_auth_token)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


@pytest.fixture
def response_fav_get_albums(user):
    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=get_favorite_albums_url(user.auth_token),
            json=user_fav_get_albums_json,
            status=200,
            match_querystring=True,
        )

        yield response_mock


def test_user_favorite_get_albums_type(app, user, response_fav_get_albums):
    albums = user.favorites_get(fav_type="albums")

    for a in albums:
        assert isinstance(a, qobuz.Album)


def test_user_favorite_get_albums_len(app, user, response_fav_get_albums):
    albums = user.favorites_get(fav_type="albums")

    assert len(albums) == user_fav_get_albums_json["albums"]["limit"]


def test_user_favorite_get_albums_content(app, user, response_fav_get_albums):
    albums = user.favorites_get(fav_type="albums")

    for i in range(len(albums)):
        assert albums[i] == qobuz.Album(
            user_fav_get_albums_json["albums"]["items"][i]
        )


def test_user_favorite_add_albums(app, user, album):
    fav_add_album_url = get_favorite_add_albums_url(album.id, user.auth_token)

    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=fav_add_album_url,
            json={"status": "success"},
            status=200,
            match_querystring=True,
        )

        assert user.favorites_add(album) is True


def test_user_favorite_del_albums(app, user, album):
    fav_del_album_url = get_favorite_del_albums_url(album.id, user.auth_token)

    with responses.RequestsMock() as response_mock:
        response_mock.add(
            responses.GET,
            url=fav_del_album_url,
            json={"status": "success"},
            status=200,
            match_querystring=True,
        )

        assert user.favorites_del(album) is True
