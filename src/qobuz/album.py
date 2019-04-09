from qobuz import api, Artist


class Album(object):
    """This class represents a Album from the Qobuz-API.

    Parameters
    ----------
    album_item: dict
        Dictionary as returned from the JSON-API to represent a album

        Keys should include:
        'id', 'title', 'tracks_count', 'released_at', and 'artist'
    """

    __slots__ = [
        "id",
        "title",
        "tracks_count",
        "released_at",
        "artist",
        "tracks",
    ]

    def __init__(self, album_item):
        self.id = album_item.get("id")
        self.title = album_item.get("title")
        self.tracks_count = album_item.get("tracks_count")
        self.released_at = album_item.get("released_at")
        self.artist = Artist(album_item["artist"])

    @property
    def type(self):
        return "album"

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.title == other.title
            and self.tracks_count == other.tracks_count
            and self.released_at == other.released_at
            and self.artist == other.artist
        )

    @classmethod
    def from_id(cls, id):
        return cls(api.request("album/get", album_id=id))

    @classmethod
    def search(cls, query, limit=50, offset=0):
        """Search for a album.

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
        list of Album
            Resulting albums for the search query
        """
        albums = api.request(
            "album/search", query=query, offset=offset, limit=limit
        )

        return [cls(a) for a in albums["albums"]["items"]]
