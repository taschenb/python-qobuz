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
