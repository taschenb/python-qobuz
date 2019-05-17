import json
import time

from qobuz import api


class Event(object):
    """Class for reporting start/end events.

    Whenever a audio stream starts, it is required to report its start.
    Whenever a audio stream stops, it is required to report the time it was
    effectively played.

    Events may be sent delayed.

    Parameters
    ----------
    user: qobuz.User
        Logged in user
    track_id: int
        Track whose start/end will be reported
    format_id: int
        The format ID of the file:
        5: MP3 320
        6: FLAC Lossless
        7: FLAC Hi-Res 24 bit =< 96kHz
        27: FLAC Hi-Res 24 bit >96 kHz & =< 192 kHz
    online: bool
        Stream played online or offline
    sample: bool
        Stream was a sample
    intent: str
        Stream or an import of the file.
        Allowed values:
        "streaming", "import", "download"
    purchase: bool
        Stream has been purchased
    local: bool
        Stream is not from Qobuz server, but local user's storage
    """
    def __init__(
        self,
        user,
        track_id,
        format_id,
        online=True,
        sample=False,
        intent="stream",
        purchase=False,
        local=False,
    ):
        self.user_id = user.id
        self.credential_id = user.credential_id
        self.device_id = user.device_id
        self.track_id = track_id
        self.format_id = format_id
        self.online = online
        self.sample = sample
        self.intent = intent
        self.purchase = purchase
        self.local = local
        self.timestamp_start = None
        self.duration = 0

    def report_start(self):
        """Report the beginning of any track streaming."""
        self.timestamp_start = time.time()
        self.duration = 0

        resp = api.post(
            "track/reportStreamingStart",
            data="events=[{}]".format(json.dumps(self.__dict__)),
        )

        return resp.get("status") == "success"

    def report_end(self, duration):
        """Report the end of the streaming of a track.

        Can be called 10 seconds before the end of the track.

        Parameters
        ----------
        duration: int
            Seconds the audio stream was played, excluding all pauses.
        """
        if self.timestamp_start is None:
            raise TypeError("Report the start beforehand")

        self.duration = duration

        resp = api.post(
            "track/reportStreamingEnd",
            data="events=[{}]".format(json.dumps(self.__dict__)),
        )

        return resp.get("status") == "success"
