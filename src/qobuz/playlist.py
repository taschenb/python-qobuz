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

    @classmethod
    def from_id(cls, playlist_id):
        playlist = api.request("playlist/get", playlist_id=playlist_id)

        return cls(playlist)

    @classmethod
    def search(cls, query, limit=50, offset=0):
        """Search for a playlist.

        Parameters
        ----------
        query: str
            Search query
        limit: int
            Number of elements returned per request
        offset: int
            Offset from which to obtain limit elements

        Returns
        -------
        list of Playlist
            Resulting playlists for the search query
        """
        playlists = api.request(
            "playlist/search", query=query, limit=limit, offset=offset
        )

        return [cls(p) for p in playlists["playlists"]["items"]]
