import requests
from loguru import logger
from requests import JSONDecodeError

from ..exception import (
    InvalidResponse,
    InvalidTargetResourceError,
)


class GetResponse:
    """
    Simple wrapper around `requests.get`, using context to ensure resources are released properly

    Instructions:
     with GetResponse("https://www.example.com/") as resp:
         print(resp.response) # response content
         response.to_disk("example.html") # write the response content to disk
    """

    def __init__(self, url: str, allow_redirects: bool = True, /, **kwargs):
        """
        get response

        Args:
             url: URL of the request
             allow_redirects: whether to allow redirection
             kwargs: Other parameters that should be passed to `requests.get`, proxies will be added automatically
        """
        from ..util.config import config

        if config["git_proxy"] and "raw.githubusercontent.com" in url:
            self.url = config.api["git_proxy"] + url
        else:
            self.url = url
        self.args = {
            "proxies": config.proxy,
            "allow_redirects": allow_redirects,
            **kwargs,
        }
        if len(self.args) != 2:
            logger.debug(self.args)

    def __enter__(self):
        self.response = requests.get(self.url, **self.args)
        if self.response.status_code != 200:
            raise InvalidTargetResourceError(self.response.status_code)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()

    @property
    def json(self) -> dict:
        """
        Parse the response content as dict

        Proxied for self.response.json()

        Returns:
             dict
        """
        try:
            return self.response.json()
        except JSONDecodeError as e:
            raise InvalidResponse(self.url) from e

    @property
    def text(self) -> str:
        """
        Parse the response content as text

        Proxied for self.response.text

        Returns:
             str
        """
        return self.response.text.encode(self.response.encoding).decode(
            self.response.apparent_encoding
        )

    @property
    def bytes(self):
        return self.response.content


def get_json(url: str, **kwargs) -> dict:
    with GetResponse(url, **kwargs) as resp:
        return resp.json


def get_text(url: str, **kwargs) -> str:
    with GetResponse(url, **kwargs) as resp:
        return resp.text


def get_bytes(url: str, **kwargs) -> bytes:
    with GetResponse(url, **kwargs) as resp:
        return resp.bytes
