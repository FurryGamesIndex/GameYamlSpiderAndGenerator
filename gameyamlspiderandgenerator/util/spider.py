from curl_cffi.requests import Session
from curl_cffi.requests.exceptions import RequestException, JSONDecodeError
from loguru import logger
from ..exception import InvalidResponse, InvalidTargetResourceError
from ..util.config import config


class MultiDomainSessionManager:
    """
    Manages multiple sessions for different domains to allow session reuse.
    """

    def __init__(self):
        self.sessions = {}

    def get_session(self, domain: str) -> Session:
        """
        Get or create a session for a given domain.

        Args:
            domain (str): The domain for which to get a session.

        Returns:
            Session: A session object.
        """
        if domain not in self.sessions:
            self.sessions[domain] = Session()
        return self.sessions[domain]

    def close_all(self):
        """
        Close all sessions.
        """
        for session in self.sessions.values():
            session.close()
        self.sessions.clear()


session_manager = MultiDomainSessionManager()


def _get_domain_from_url(url: str) -> str:
    """
    Extract the domain from a given URL.

    Args:
        url (str): The URL to extract the domain from.

    Returns:
        str: The domain of the URL.
    """
    from urllib.parse import urlparse

    return urlparse(url).netloc


def _request(url: str, method: str = "GET", **kwargs):
    """
    Helper function to send an HTTP request using the appropriate session.

    Args:
        url (str): The URL to request.
        method (str): HTTP method to use (default: "GET").
        **kwargs: Additional arguments passed to the request.

    Returns:
        Response: The HTTP response.

    Raises:
        InvalidTargetResourceError: If the response status code is not 200.
        InvalidResponse: If there is an error parsing the response.
    """
    domain = _get_domain_from_url(url)
    session = session_manager.get_session(domain)

    if config["git_proxy"] and "raw.githubusercontent.com" in url:
        url = config.api["git_proxy"] + url

    args = {
        "proxies": config.proxy,
        "allow_redirects": kwargs.pop("allow_redirects", True),
        **kwargs,
    }

    try:
        if len(args) != 2:
            logger.debug(args)
        else:
            logger.debug(url)

        response = session.request(method, url, impersonate="chrome", **args)  # noqa
        if response.status_code != 200:
            raise InvalidTargetResourceError(response.status_code)
        return response
    except RequestException as e:
        logger.error(f"Error during request to {url}: {e}")
        raise InvalidResponse(url) from e


def get_json(url: str, **kwargs) -> dict:
    """
    Fetch JSON data from a URL.

    Args:
        url (str): The URL to fetch.
        **kwargs: Additional arguments passed to the request.

    Returns:
        dict: The parsed JSON data.

    Raises:
        InvalidResponse: If the response is not valid JSON.
    """
    response = _request(url, **kwargs)
    try:
        return response.json()
    except JSONDecodeError as e:
        raise InvalidResponse(url) from e


def get_text(url: str, **kwargs) -> str:
    """
    Fetch text content from a URL.

    Args:
        url (str): The URL to fetch.
        **kwargs: Additional arguments passed to the request.

    Returns:
        str: The response content as text.
    """
    response = _request(url, **kwargs)
    return response.text


def get_bytes(url: str, **kwargs) -> bytes:
    """
    Fetch binary content from a URL.

    Args:
        url (str): The URL to fetch.
        **kwargs: Additional arguments passed to the request.

    Returns:
        bytes: The response content as bytes.
    """
    response = _request(url, **kwargs)
    return response.content
