import hashlib
import qobuz
import requests
import time
try:
    from urllib.parse import urljoin
except ImportError:
    # python2
    from urlparse import urljoin


API_URL = "https://www.qobuz.com/api.json/0.2/"
APP_ID = None
APP_SECRET = None


def register_app(app_id, app_secret=None):
    """Save the app's id and secret to be used when needed.

    Parameters
    ----------
    app_id: str
        The ID of the APP, issued by api@qobuz.com
    app_secret: str
        The secret to the app_id should anythin be used that requires a secret
    """
    qobuz.api.APP_ID = app_id
    qobuz.api.APP_SECRET = app_secret


def request(url, signed=False, comma_encoding=True, **params):
    """Call Qobuz API for URL and parameters.

    In order to be accepted, every call needs a valid APP_ID.
    Some calls also require the corresponding secret to be added as signature.
    Both the ID and secret can be requested from api@qobuz.com.

    >>> import qobuz
    >>> qobuz.api.register_app(app_id="your_app_id", app_secret="your secret")

    Parameters
    ----------
    url: str
        URL to be joined with the base URL API_URL
    signed: bool
        Sign the request with the APP secret
    comma_encoding: bool
        URL encode ',' as '%2C'
    **kwargs
        GET parameters to be added to the request
    """
    if signed is True:
        request_ts = int(time.time())
        params["request_sig"] = _get_request_sig(
            urljoin(API_URL, url), timestamp=request_ts, **params
        )
        params["request_ts"] = request_ts
    if comma_encoding is True:
        return _request(url, **params)
    else:
        return _request_comma_params(url, **params)


def _request(url, **params):
    """Call the API_URL with appended url and parameters.

    Parameters
    ----------
    url: str
        URL to be joined with the base URL API_URL
    **kwargs
        GET parameters to be added to the request
    """
    params["app_id"] = APP_ID

    # For server-side caching sort alphabetically
    params = dict(sorted(params.items()))

    r = requests.get(urljoin(API_URL, url), params=params)
    r.raise_for_status()

    return r.json()


def post(url, data, **params):
    """Send a POST request.

    Parameters
    ----------
    url: str
        URL to be joined with the base URL API_URL
    data: str
        Payload to be sent
    **params
        GET parameters to be added to the request
    """
    params["app_id"] = APP_ID

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    r = requests.post(
        urljoin(API_URL, url), params=params, headers=headers, data=data
    )
    r.raise_for_status()

    return r.json()


def _request_comma_params(url, **params):
    """Make a API request without encoding commas.

    The default for requests is to encode the complete URL, including the GET
    parameters. This is not always intended, as the API expects comma separated
    lists.

    Parameters
    ----------
    url: str
        URL to be joined with the base URL API_URL
    **kwargs
        GET parameters to be added to the request
    """
    params = requests.models.RequestEncodingMixin._encode_params(params)
    params = params.replace("%2C", ",")

    url = "{}?{}".format(urljoin(API_URL, url), params)

    return _request(url)


def _get_request_sig(url, timestamp, **params):
    """Return the signature for a request.

    Whenever an API-call requires the app-secret, the secret is not sent
    directly, but is hidden inside a checksum for that request, called
    signature.

    This signature needs to be added as 'request_sig' to the GET parameters.

    Parameters
    ----------
    url: str
        Url for the API call
    timestamp: int
        UNIX timestamp in seconds
    **kwargs
        GET parameters of the request

    Returns
    -------
    str
        request_sig to be added to the GET parameters
    """
    if qobuz.api.APP_SECRET is None:
        raise TypeError("No secret setup. See api.register_app()")

    request_sig = url.replace(API_URL, "")
    request_sig = request_sig.replace("/", "")

    # The signature does not include all parameters
    params.pop("app_id", None)
    params.pop("user_auth_token", None)
    params.pop("request_ts", None)

    params = dict(sorted(params.items()))

    for key, value in params.items():
        if value is not None:
            request_sig += str(key) + str(value)

    request_sig += str(timestamp)
    request_sig += APP_SECRET

    return hashlib.md5(request_sig.encode()).hexdigest()
