import pytest
import qobuz
import responses

from tests.resources.fixtures import user, album


qobuz.api.APP_ID = "request_from_api@qobuz.com"


def get_favorite_add_albums_url(album_ids, user_auth_token):
    return (
        qobuz.api.API_URL
        + "favorite/create"
        + "?album_ids={}".format(album_ids)
        + "&user_auth_token={}".format(user_auth_token)
        + "&app_id={}".format(qobuz.api.APP_ID)
    )


def test_user_favorite_add_albums(user, album):
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
