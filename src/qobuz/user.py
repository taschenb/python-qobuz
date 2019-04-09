import hashlib

from qobuz import api, Artist, Album, Track


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

    def __init__(self, username, password):
        self.username = username
        self.auth_token = self.login(self.username, password)

    def login(self, username, password):
        """Login and return a authentication token.

        Parameters
        ----------
        username: str
            Username or e-mail of the user
        password: str
            Password for the username

        Returns
        -------
        str
            User's authentication token
        """
        user = api.request(
            "user/login",
            username=username,
            password=self._hash_password(password),
        )

        return user["user_auth_token"]

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
