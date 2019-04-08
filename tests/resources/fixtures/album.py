import pytest
import qobuz

from tests.resources.responses import album_get_json


@pytest.fixture
def album():
    return qobuz.Album(album_get_json)
