import pytest
import qobuz

from tests.resources.responses import artist_search_json


@pytest.fixture
def artist():
    artist_item = artist_search_json["artists"]["items"][0]

    return qobuz.Artist(artist_item)
