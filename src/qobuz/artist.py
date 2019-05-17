import qobuz


class Artist(object):
    """This class represents an artist from the Qobuz-API.

    Parameters
    ----------
    artist_item: dict
        Dictionary as returned from the JSON-API to represent an artist

        Keys should include:
        'id', 'name', 'picture', 'slug', and 'album_count'
    """

    __slots__ = ["id", "name", "picture", "slug", "albums_count"]

    def __init__(self, artist_item):
        self.id = artist_item.get("id")
        self.name = artist_item.get("name")
        self.picture = artist_item.get("picture")
        self.slug = artist_item.get("slug")
        self.albums_count = artist_item.get("albums_count")

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.name == other.name
            and self.picture == other.picture
            and self.slug == other.slug
            and self.albums_count == other.albums_count
        )

    @property
    def type(self):
        return "artist"

    def get_all_tracks(self, offset=0, limit=50):
        res = qobuz.api.request(
            "artist/get",
            artist_id=self.id,
            extra="tracks",
            offset=offset,
            limit=limit,
        )

        return [qobuz.Track(t) for t in res["tracks"]["items"]]

    def get_all_albums(self, offset=0, limit=50):
        """Return albums of an artist.

        Parameters
        ----------
        limit: int
            Number of elements returned per request
        offset: int
            Offset from which to obtain limit elements

        Returns
        -------
        list of Album
            Albums from the artist
        """
        albums = qobuz.api.request(
            "artist/get",
            artist_id=self.id,
            extra="albums",
            offset=offset,
            limit=limit,
        )

        return [qobuz.Album(a) for a in albums["albums"]["items"]]

    @classmethod
    def from_id(cls, id):
        return cls(qobuz.api.request("artist/get", artist_id=id))

    @classmethod
    def search(cls, artist, limit=50, offset=0):
        """Search for an artist.

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
        list of Artist
            Resulting playlists for the search query
        """
        req = qobuz.api.request(
            "artist/search", query=artist, limit=limit, offset=offset
        )

        return [cls(a) for a in req["artists"]["items"]]
