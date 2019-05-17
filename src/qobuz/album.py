import qobuz


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
        "_tracks",
    ]

    def __init__(self, album_item):
        self.id = album_item.get("id")
        self.title = album_item.get("title")
        self.tracks_count = album_item.get("tracks_count")
        self.released_at = album_item.get("released_at")
        self.artist = qobuz.Artist(album_item["artist"])
        self._tracks = None

    @property
    def type(self):
        return "album"

    @property
    def tracks(self):
        if self._tracks is None:
            self._update_tracks()

        return self._tracks

    def _update_tracks(self):
        resp = qobuz.api.request("album/get", album_id=self.id)

        self._tracks = [
            qobuz.Track(t, album=self) for t in resp["tracks"]["items"]
        ]

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
        return cls(qobuz.api.request("album/get", album_id=id))

    @classmethod
    def get_featured(cls, type="new-releases", limit=50, offset=0):
        """Get featured albums.

        Parameters
        ----------
        type: str
            Accepted values are:
            most-streamed, best-sellers, new-releases, press-awards,
            editor-picks, most-featured, new-releases-full, recent-releases,
            ideal-discography, qobuzissims, album-of-the-week,
            re-release-of-the-week
        """
        albums = qobuz.api.request(
            "album/getFeatured", type=type, offset=offset, limit=limit
        )

        return [cls(a) for a in albums["albums"]["items"]]

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
        albums = qobuz.api.request(
            "album/search", query=query, offset=offset, limit=limit
        )

        return [cls(a) for a in albums["albums"]["items"]]
