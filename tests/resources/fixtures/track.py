import pytest
import qobuz

from tests.resources.responses import track_search_json


@pytest.fixture
def track():
    track_item = track_search_json["tracks"]["items"][0]

    return qobuz.Track(track_item)
