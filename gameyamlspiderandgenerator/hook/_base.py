import abc
from enum import Enum, auto


class HookLoadingSequence(Enum):
    FIRST = auto()
    NORMAL = auto()
    LAST = auto()


class BaseHook(abc.ABC):
    """Base class for hooks"""

    CHANGED: list | None = None
    REQUIRE_CONFIG: bool = False
    ORDER: HookLoadingSequence = HookLoadingSequence.NORMAL

    @abc.abstractmethod
    def setup(self, data: dict):
        """
        Run the hook function

        Args:
            data: The data
        """
