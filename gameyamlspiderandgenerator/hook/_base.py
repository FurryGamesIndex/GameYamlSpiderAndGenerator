import abc


class BaseHook(abc.ABC):
    """钩子基类"""

    def __load_hook__(self, data: dict):
        """
        加载钩子

        Args:
            data: 钩子数据
        """
