from qobuz import api, Artist, Album


audio_format = {
    "mp3": 5,  # 'MP3 320'),
    "flac": 6,  # 'FLAC Lossless'),
    "hires": 7,  # 'FLAC Hi-Res 24 bit =< 96kHz'),
    "hires_hsr": 27,  # 'FLAC Hi-Res 24 bit >96 kHz & =< 192 kHz')
}


class Track(object):
    """This class represents a Track from the Qobuz-API.

    Parameters
    ----------
    track_item: dict
        Dictionary as returned from the JSON-API to represent a track

        Keys should include:
        'id', 'title', 'album', and 'performer'
    """

    __slots__ = [
        "id",
        "title",
        "album",
        "duration",
        "media_number",
        "track_number",
        "_artist",
        "_performer_id",
        "maximum_format_id",
    ]

    def __init__(self, track_item, album=None):
        self.id = track_item.get("id")
        self.title = track_item.get("title")
        if album is not None:
            self.album = album
        else:
            self.album = Album(track_item.get("album"))
        self.duration = track_item.get("duration")
        self.media_number = track_item.get("media_number")
        self.track_number = track_item.get("track_number")
        self._performer_id = track_item.get("performer", {}).get("id")
        self._artist = None

        maximum_bit_depth = track_item.get("album", {}).get(
            "maximum_bit_depth"
        )
        maximum_sampling_rate = track_item.get("album", {}).get(
            "maximum_sampling_rate"
        )
        if maximum_bit_depth < 24:
            self.maximum_format_id = audio_format["flac"]
        elif maximum_sampling_rate <= 96:
            self.maximum_format_id = audio_format["hires"]
        else:
            self.maximum_format_id = audio_format["hires_hsr"]

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
        # Not all tracks have a valid performer
        if self._performer_id is None:
            return

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

    @classmethod
    def from_id(cls, id):
        return cls(api.request("track/get", track_id=id))
