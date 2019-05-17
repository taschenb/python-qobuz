import hashlib
import uuid

from qobuz import api, Artist, Album, Track, Playlist


class User(object):
    """Own user to be logged in.

    Some operations require an authenticated user.

    Parameters
    ----------
    username: str
        Username or e-mail of the user
    password: str
        Password for the username
    """

    def __init__(self, username, password, device_manufacturer_id=None):
        self.username = username
        if device_manufacturer_id is None:
            device_manufacturer_id = uuid.uuid4()

        login_resp = api.request(
            "user/login",
            username=username,
            password=self._hash_password(password),
            device_manufacturer_id=device_manufacturer_id,
        )

        self.auth_token = login_resp["user_auth_token"]
        self.id = login_resp["user"]["id"]
        self.credential_id = login_resp["user"]["credential"]["id"]
        self.device_id = login_resp["user"]["device"]["id"]

    @staticmethod
    def _hash_password(password):
        """Hash the password with MD5.

        Parameters
        ----------
        password: str
            Plain password

        Returns
        -------
        str
            Hashed password to be used for logging in
        """
        return hashlib.md5(password.encode()).hexdigest()

    @staticmethod
    def reset_password(username):
        """Request the resetting of the current password.

        Parameters
        ----------
        username: str
            Username to be sent a email with instructions.

        Returns
        -------
        bool
            Successfully requested
        """
        resp = api.request("user/resetPassword", username=username)

        return resp.get("status") == "success"

    def favorites_add(self, obj):
        """Add artist/album/track to user's favorites.

        Parameters
        ----------
        obj: Artist/Album/Track
            Object to be added to the favorites

        Returns
        -------
        bool
            Successfully added to favorites
        """
        if isinstance(obj, Artist):
            status = api.request(
                "favorite/create",
                artist_ids=obj.id,
                user_auth_token=self.auth_token,
            )
        elif isinstance(obj, Album):
            status = api.request(
                "favorite/create",
                album_ids=obj.id,
                user_auth_token=self.auth_token,
            )
        elif isinstance(obj, Track):
            status = api.request(
                "favorite/create",
                track_ids=obj.id,
                user_auth_token=self.auth_token,
            )
        else:
            raise TypeError("obj must be Artist, Album or Track")

        return status.get("status") == "success"

    def favorites_del(self, obj):
        """Delete artist/album/track from favorites.

        Parameters
        ----------
        obj: Artist/Album/Track
            Object to be added to the favorites

        Returns
        -------
        bool
            Successfully deleted from favorites
        """
        if isinstance(obj, Artist):
            status = api.request(
                "favorite/delete",
                artist_ids=obj.id,
                user_auth_token=self.auth_token,
            )
        elif isinstance(obj, Album):
            status = api.request(
                "favorite/delete",
                album_ids=obj.id,
                user_auth_token=self.auth_token,
            )
        elif isinstance(obj, Track):
            status = api.request(
                "favorite/delete",
                track_ids=obj.id,
                user_auth_token=self.auth_token,
            )
        else:
            raise TypeError("obj must be Artist, Album or Track")

        return status.get("status") == "success"

    def favorites_status(self, obj):
        """Get status whether obj is in the favorites.

        Parameters
        ----------
        obj: Artist/Album/Track
            Object to be added to the favorites

        Returns
        -------
        bool
            Successfully deleted from favorites
        """
        status = api.request(
            "favorite/status",
            item=obj.id,
            type=obj.type,
            user_auth_token=self.auth_token,
        )

        return status.get("status") == "true"

    def favorites_get(self, fav_type=None, limit=50, offset=0):
        """Get all favorites for the user.

        Parameters
        ----------
        fav_type: str
            Favorite type: 'artists', 'albums' or 'tracks'
        limit: int
            Number of elements returned per request
        offset: int
            Offset from which to obtain limit elements

        Returns
        -------
        list
            List containing Artist/Album/Track objects
        """
        favorites = api.request(
            "favorite/getUserFavorites",
            type=fav_type,
            limit=limit,
            offset=offset,
            user_auth_token=self.auth_token,
        )

        if fav_type == "artists":
            return [Artist(f) for f in favorites["artists"]["items"]]
        if fav_type == "albums":
            return [Album(f) for f in favorites["albums"]["items"]]
        if fav_type == "tracks":
            return [Track(f) for f in favorites["tracks"]["items"]]
        else:
            all_favorites = [Artist(f) for f in favorites["artists"]["items"]]
            all_favorites.append(
                Album(f) for f in favorites["albums"]["items"]
            )
            all_favorites.append(
                Track(f) for f in favorites["tracks"]["items"]
            )
            return all_favorites

    def playlists_get(self, filter="owner", limit=50, offset=0):
        result = api.request(
            "playlist/getUserPlaylists",
            filter=filter,
            limit=limit,
            offset=offset,
            user_auth_token=self.auth_token,
        )

        return [Playlist(p, user=self) for p in result["playlists"]["items"]]

    def playlist_create(
        self, name, description=None, is_public=0, is_collaborative=0
    ):
        """Create a new playlist.

        Parameters
        ----------
        name: str
            Name for the new playlist
        description: str
            Description for the playlist
        is_public: bool
            Flag to make the playlist public.
        is_collaborative: bool
            Flag to make the playlist collaborative.
        """
        playlist = api.request(
            "playlist/create",
            name=name,
            description=description,
            is_public=is_public,
            is_collaborative=is_collaborative,
            user_auth_token=self.auth_token,
        )

        return Playlist(playlist)

    def playlist_delete(self, playlist):
        """Delete a playlist.

        Parameters
        ----------
        playlist: Playlist
            Playlist to be deleted

        Returns
        -------
        bool
            Successfully deleted playlist
        """
        status = api.request(
            "playlist/delete",
            playlist_id=playlist.id,
            user_auth_token=self.auth_token,
        )

        return status.get("status") == "success"

    def get_file_url(self, track_id, format_id=None, intent=None):
        """Get the file url for a track.

        Parameters
        ----------
        track_id: int
            Track-ID to get the url for
        format_id: int
            Format ID following qobuz specifications:
             5: MP3 320
             6: FLAC Lossless
             7: FLAC Hi-Res 24 bit =< 96kHz,
            27: FLAC Hi-Res 24 bit >96 kHz & =< 192 kHz
        intent: str
            How the application will use the file URL
            Either 'stream', 'import', or 'download'.

        Returns
        -------
        str
            URL to the appropriate file
        """
        resp = api.request(
            "track/getFileUrl",
            signed=True,
            track_id=track_id,
            format_id=format_id,
            intent=intent,
            user_auth_token=self.auth_token,
        )

        return resp.get("url")
