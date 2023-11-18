import abc
import re
from typing import List

from ..util.fgi_yaml import YamlData


class BasePlugin(abc.ABC):
    """插件基类"""

    _VERIFY_PATTERN: re.Pattern

    @classmethod
    def verify(cls, url: str) -> bool:
        """
        验证 URL 是否符合插件的要求

        Args:
            url: URL

        Returns:
            是否符合要求
        """
        return bool(cls._VERIFY_PATTERN.match(url))

    @staticmethod
    def __load_hook__(data: dict):
        """
        加载钩子

        Args:
            data: 钩子数据
        """
        from gameyamlspiderandgenerator.util.plugin_manager import pkg

        for i in pkg.hook.values():
            data = i().setup(data)
        return data

    @abc.abstractmethod
    def get_name(self) -> str:
        """
        获取游戏名称

        Returns:
            游戏名称
        """

    @abc.abstractmethod
    def get_desc(self) -> str:
        """
        获取游戏描述

        Returns:
            游戏描述
        """

    @abc.abstractmethod
    def get_brief_desc(self) -> str:
        """
        获取游戏简介

        Returns:
            游戏简介
        """

    @abc.abstractmethod
    def get_thumbnail(self) -> str:
        """
        获取游戏封面

        Returns:
            游戏封面
        """

    @abc.abstractmethod
    def get_authors(self) -> List[dict]:
        """
        获取游戏作者

        Returns:
            游戏作者
        """

    @abc.abstractmethod
    def get_tags(self) -> List[dict]:
        """
        获取游戏标签

        Returns:
            游戏标签
        """

    @abc.abstractmethod
    def get_misc_tags(self) -> List[dict]:
        """
        获取游戏其他标签

        Returns:
            游戏其他标签
        """

    @abc.abstractmethod
    def get_platforms(self) -> List[str]:
        """
        获取游戏平台

        Returns:
            游戏平台
        """

    @abc.abstractmethod
    def get_langs(self) -> List[str]:
        """
        获取游戏语言

        Returns:
            游戏语言
        """

    @abc.abstractmethod
    def get_links(self) -> List[dict]:
        """
        获取游戏链接

        Returns:
            游戏链接
        """

    @abc.abstractmethod
    def get_screenshots(self) -> List[str]:
        """
        获取游戏截图

        Returns:
            游戏截图
        """

    @abc.abstractmethod
    def to_yaml(self) -> YamlData:
        """
        转换为 YAML

        Returns:
            YAML
        """
