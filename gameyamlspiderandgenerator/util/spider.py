from pathlib import Path
from typing import Dict, Union

import requests
from requests import JSONDecodeError

from ..exception import (
    CommunicateWithServerFailed,
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
        try:
            self.response = requests.get(self.url, **self.args)
            if self.response.status_code != 200:
                raise CommunicateWithServerFailed(self.response.status_code)
            return self
        except Exception as e:
            raise CommunicateWithServerFailed(str(e)[:100]) from None

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
        return self.response.text

    @property
    def status(self) -> int:
        """
        获取响应状态码

        Proxied for `self.response.status_code`

        Returns:
            状态码
        """
        return self.response.status_code

    def to_disk(self, path: Union[str, Path], allow_exist: bool = False, /):
        """
        将响应内容写入磁盘

        Args:
            path: 路径
            allow_exist: 是否允许覆盖已存在的文件
        """
        path = Path(path)
        if path.is_file():
            if allow_exist:
                path.unlink()
            else:
                raise FileExistsError(f"File {path} already exists")
        elif path.is_dir():
            raise IsADirectoryError(f"{path} is a directory")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.response.content)


def get_json(url: str) -> Dict:
    with GetResponse(url) as resp:
        return resp.json


def get_text(url: str) -> str:
    with GetResponse(url) as resp:
        return resp.text


def get_status(url: str) -> int:
    with GetResponse(url) as resp:
        return resp.status


def download_file(url: str, save: Union[str, Path]):
    with GetResponse(url) as resp:
        resp.to_disk(save)
