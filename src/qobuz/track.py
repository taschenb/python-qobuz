from qobuz import api, Artist, Album


class Track(object):
    """This class represents a Track from the Qobuz-API.

    Parameters
    ----------
    track_item: dict
        Dictionary as returned from the JSON-API to represent a track

        Keys should include:
        'id', 'title', 'album', and 'performer'
    """

    __slots__ = ["id", "title", "album", "_artist", "_performer_id"]

    def __init__(self, track_item):
        self.id = track_item.get("id")
        self.title = track_item.get("title")
        self.album = Album(track_item.get("album"))
        self._performer_id = track_item.get("performer", {}).get("id")
        self._artist = None

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.title == other.title
            and self.album == other.album
            and self._performer_id == other._performer_id
            and self._artist == other._artist
        )

    @property
    def artist(self):
        if self._artist is None:
            self._artist = Artist.from_id(self._performer_id)
        return self._artist

    @property
    def type(self):
        return "track"

    @classmethod
    def search(cls, query, limit=50, offset=0):
        """Search for a track.

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
        list of Track
            Resulting tracks for the search query
        """
        tracks = api.request(
            "track/search", query=query, offset=offset, limit=limit
        )

        return [cls(t) for t in tracks["tracks"]["items"]]
