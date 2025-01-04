import abc
import re
import traceback

from deepdiff import DeepDiff
from loguru import logger

from ..util.fgi_yaml import YamlData
from ..hook import HookLoadingSequence
from ..exception import GenerateError


class BasePlugin(abc.ABC):
    """Base class for plugins"""

    _VERIFY_PATTERN: re.Pattern

    @staticmethod
    def _remove_query(s: str):
        s = re.sub(r"\?t=\d{6,12}", "", s)
        return s.replace("![]", "![img]")

    @classmethod
    def verify(cls, url: str) -> bool:
        """
        Verify if the URL meets the plugin's requirements

        Args:
            url: The URL

        Returns:
            Whether it meets the requirements
        """
        return cls._VERIFY_PATTERN.match(url) is not None

    @staticmethod
    def _load_hook(data: dict):
        """
        Load hooks

        Args:
            data: Hook data
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
                        f"{i} changed: {DeepDiff(_old_data, data, ignore_order=True).to_json()}"
                    )
            except Exception as e:
                logger.warning(
                    f"An {type(e).__name__} error occurred while running the {i} hook. (Use --debug for more details)"
                )
                if not isinstance(e, GenerateError):
                    logger.debug(traceback.format_exc())
                else:
                    logger.error(traceback.format_exc())
        return data

    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Get the game name

        Returns:
            The game name
        """

    @abc.abstractmethod
    def get_desc(self) -> str:
        """
        Get the game description

        Returns:
            The game description
        """

    @abc.abstractmethod
    def get_brief_desc(self) -> str:
        """
        Get the game brief description

        Returns:
            The game brief description
        """

    @abc.abstractmethod
    def get_thumbnail(self) -> str:
        """
        Get the game cover

        Returns:
            The game cover
        """

    @abc.abstractmethod
    def get_authors(self) -> list[dict]:
        """
        Get the game authors

        Returns:
            The game authors
        """

    @abc.abstractmethod
    def get_tags(self) -> list[str]:
        """
        Get the game tags

        Returns:
            The game tags
        """

    @abc.abstractmethod
    def get_misc_tags(self) -> list[dict]:
        """
        Get other game tags

        Returns:
            Other game tags
        """

    @abc.abstractmethod
    def get_platforms(self) -> list[str]:
        """
        Get the game platforms

        Returns:
            The game platforms
        """

    @abc.abstractmethod
    def get_langs(self) -> list[str]:
        """
        Get the game languages

        Returns:
            The game languages
        """

    @abc.abstractmethod
    def get_links(self) -> list[dict]:
        """
        Get the game links

        Returns:
            The game links
        """

    @abc.abstractmethod
    def get_screenshots(self) -> list[str]:
        """
        Get the game screenshots

        Returns:
            The game screenshots
        """

    @abc.abstractmethod
    def to_yaml(self) -> YamlData:
        """
        Convert to YAML

        Returns:
            YAML
        """

    @abc.abstractmethod
    def get_type_tags(self) -> list[dict]:
        pass
