import abc
import re
import traceback

from deepdiff import DeepDiff as diff
from loguru import logger

from ..util.fgi_yaml import YamlData
from ..hook import HookLoadingSequence


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
        return cls._VERIFY_PATTERN.match(url) is not None

    @staticmethod
    def _load_hook(data: dict):
        """
        加载钩子

        Args:
            data: 钩子数据
        """
        from ..util.plugin_manager import pkg

        load_order = (
            [_ for _ in pkg.hook if pkg.hook[_].ORDER == HookLoadingSequence.FIRST]
            + [_ for _ in pkg.hook if pkg.hook[_].ORDER == HookLoadingSequence.NORMAL]
            + [_ for _ in pkg.hook if pkg.hook[_].ORDER == HookLoadingSequence.LAST]
        )
        for i in load_order:
            try:
                _old_data = data
                data = pkg.hook[i]().setup(data)
                if pkg.hook[i].CHANGED is not None:
                    logger.debug(
                        f"{i} changed: {diff(_old_data, data, ignore_order=True).to_json()}"
                    )
            except Exception as e:
                logger.warning(
                    f"An {type(e).__name__} error occurred while running the {i} hook. (Use --debug for more details)"
                )
                logger.debug(traceback.format_exc())
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
    def get_authors(self) -> list[dict]:
        """
        获取游戏作者

        Returns:
            游戏作者
        """

    @abc.abstractmethod
    def get_tags(self) -> list[dict]:
        """
        获取游戏标签

        Returns:
            游戏标签
        """

    @abc.abstractmethod
    def get_misc_tags(self) -> list[dict]:
        """
        获取游戏其他标签

        Returns:
            游戏其他标签
        """

    @abc.abstractmethod
    def get_platforms(self) -> list[str]:
        """
        获取游戏平台

        Returns:
            游戏平台
        """

    @abc.abstractmethod
    def get_langs(self) -> list[str]:
        """
        获取游戏语言

        Returns:
            游戏语言
        """

    @abc.abstractmethod
    def get_links(self) -> list[dict]:
        """
        获取游戏链接

        Returns:
            游戏链接
        """

    @abc.abstractmethod
    def get_screenshots(self) -> list[str]:
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
