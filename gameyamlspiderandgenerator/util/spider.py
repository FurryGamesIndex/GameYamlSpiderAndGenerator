
import requests
from requests import JSONDecodeError

from ..exception import (
    InvalidTargetResourceError,
    InvalidResponse,
)
from ..util.config import config


class GetResponse:
    """
    对 requests.get 的简单封装，使用上下文以保证资源被正确释放

    使用方法：

    with GetResponse("https://www.example.com/") as resp:
        print(resp.response)  # 响应内容
        response.to_disk("example.html")  # 将响应内容写入磁盘
    """

    def __init__(self, url: str, allow_redirects: bool = True, /, **kwargs):
        """
        获取响应

        Args:
            url: 请求的 URL
            allow_redirects: 是否允许重定向
            kwargs: 其他应传入 requests.get 的参数，proxies 会被自动添加
        """
        self.url = url
        self.args = {
            "proxies": config["proxy"],
            "allow_redirects": allow_redirects,
            **kwargs,
        }

    def __enter__(self):
        self.response = requests.get(self.url, **self.args)
        if self.response.status_code != 200:
            raise InvalidTargetResourceError(self.response.status_code)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()

    @property
    def json(self):
        """
        将响应内容解析为 JSON

        Proxied for self.response.json()

        Returns:
            JSON
        """
        try:
            return self.response.json()
        except JSONDecodeError as e:
            raise InvalidResponse(self.url) from e

    @property
    def text(self) -> str:
        """
        将响应内容解析为文本

        Proxied for self.response.text

        Returns:
            文本
        """
        return self.response.text.encode(self.response.encoding).decode(self.response.apparent_encoding)

    @property
    def status(self) -> int:
        """
        获取响应状态码

        Proxied for `self.response.status_code`

        Returns:
            状态码
        """
        return self.response.status_code

    @property
    def bytes(self):
        return self.response.content


def get_json(url: str) -> dict:
    with GetResponse(url) as resp:
        return resp.json


def get_text(url: str) -> str:
    with GetResponse(url) as resp:
        return resp.text


def get_status(url: str) -> int:
    with GetResponse(url) as resp:
        return resp.status


def get_bytes(url: str) -> bytes:
    with GetResponse(url) as resp:
        return resp.bytes
