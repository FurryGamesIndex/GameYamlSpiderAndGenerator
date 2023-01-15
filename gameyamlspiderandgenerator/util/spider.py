from pathlib import Path

from requests import JSONDecodeError

from gameyamlspiderandgenerator.exception import (
    CommunicateWithServerFailed,
    InvalidResponse,
)

if __name__ != "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from typing import AnyStr, Dict, SupportsInt

import requests
from loguru import logger

from gameyamlspiderandgenerator.util.setting import get_config

setting = get_config()


class GetResponse:
    """对 requests.get 的简单封装"""

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
            "proxies": setting["proxy"],
            "allow_redirects": allow_redirects,
            **kwargs,
        }

    def __enter__(self):
        self.response = requests.get(self.url, **self.args)
        if self.response.status_code != 200:
            raise CommunicateWithServerFailed(self.response.status_code)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()

    @property
    def json(self) -> Dict:
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

    def to_disk(self, path: str | Path, allow_exist: bool = False, /):
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


def get_json(url: AnyStr) -> SupportsInt | Dict:
    logger.info(setting)
    try:
        response = requests.get(url, proxies=setting["proxy"])
        if response.status_code == 200:
            return response.json()
        raise CommunicateWithServerFailed(response.status_code)
    except Exception as e:
        logger.trace(e)
        raise CommunicateWithServerFailed() from e


def get_text(url: AnyStr) -> SupportsInt | AnyStr:
    try:
        response = requests.get(url, proxies=setting["proxy"])
        if response.status_code == 200:
            return response.text
        else:
            raise CommunicateWithServerFailed(response.status_code)
    except Exception as e:
        logger.trace(e)
        raise CommunicateWithServerFailed() from e


def get_status(url: AnyStr) -> SupportsInt:
    try:
        return requests.get(url, proxies=setting["proxy"]).status_code
    except Exception as e:
        logger.error(e)
        return -3


def download_file(url: AnyStr, save: AnyStr) -> SupportsInt:
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            return response.status_code
        open(save, "wb").write(response.content)
        # NEVER USE `open` THIS WAY, YOU WILL LEAK FDs
        return 0
    except Exception as e:
        logger.error(e)
        return -3
