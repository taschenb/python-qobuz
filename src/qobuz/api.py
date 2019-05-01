import qobuz
import requests
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


def request(url, comma_encoding=True, **params):
    """Call Qobuz API for URL and parameters.

    Call the API_URL, append the url and parameters.
    In order to be accepted, the call needs a valid APP_ID.
    An APP_ID can be requested from api@qobuz.com.

    >>> import qobuz
    >>> qobuz.api.register_app(app_id="your_app_id", app_secret="your secret")

    Parameters
    ----------
    url: str
        URL to be joined with the base URL API_URL
    comma_encoding: bool
        URL encode ',' as '%2C'
    **kwargs
        GET parameters to be added to the request
    """
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
