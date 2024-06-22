import abc


class BaseHook(abc.ABC):
    """钩子基类"""

    CHANGED: list | None = None
    REQUIRE_CONFIG: bool = False

    @abc.abstractmethod
    def setup(self, data: dict):
        """
        运行钩子函数

        Args:
            data: 数据
        """
