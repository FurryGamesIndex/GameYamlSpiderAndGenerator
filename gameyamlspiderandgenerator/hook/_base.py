import abc
from enum import Enum


class HookLoadingSequence(Enum):
    FIRST = 1
    NORMAL = 2
    LAST = 3


class BaseHook(abc.ABC):
    """钩子基类"""

    CHANGED: list | None = None
    REQUIRE_CONFIG: bool = False
    ORDER: HookLoadingSequence = HookLoadingSequence.NORMAL

    @abc.abstractmethod
    def setup(self, data: dict):
        """
        运行钩子函数

        Args:
            data: 数据
        """
