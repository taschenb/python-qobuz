import pytest
import qobuz

from tests.resources.responses import playlist_create_json


@pytest.fixture
def playlist():
    return qobuz.Playlist(playlist_create_json)
