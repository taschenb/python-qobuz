from qobuz import api, Track


class Playlist(object):
    """This class represents a playlist from the Qobuz-API.

    Parameters
    ----------
    playlist_item: dict
        Dictionary as returned from the JSON-API to represent a playist

        Keys should include:
        'id', 'name', and 'description'
    """

    __slots__ = ["id", "name", "description"]

    def __init__(self, playlist_item):
        self.id = playlist_item.get("id")
        self.name = playlist_item.get("name")
        self.description = playlist_item.get("description")

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
        )
