import importlib
from types import ModuleType

from loguru import logger
from pathlib import Path
from ..exception import ApiKeyNotFoundError
from ..hook import BaseHook
from ..plugin import BasePlugin
from ..util.config import config


def get_subclasses(module: ModuleType, base_class: type) -> [BasePlugin, BaseHook]:
    """
    Get the subclasses of the specified base class from the given module.

    Args:
        module (ModuleType): The module to search for subclasses.
        base_class (Type): The base class to find subclasses for.

    Returns:
        Type: The subclass of the specified base class.

    Raises:
        NotImplementedError: If the specified base class is not found in the module.
    """

    class_dir = dir(module)
    if base_class.__name__ in class_dir:
        for i in class_dir:
            obj = getattr(module, i)
            if (
                isinstance(obj, type)
                and issubclass(obj, base_class)
                and obj is not base_class
            ):
                return getattr(module, i)
    raise NotImplementedError(base_class.__name__)


class Package:
    plugin: dict[str, BasePlugin] = {}
    hook: dict[str, BaseHook] = {}

    def init(self):
        config.plugin = (
            _.stem
            for _ in (
                (Path(__file__).resolve().parent.parent / "plugin").glob("[!_]*.py")
            )
        )
        self.load_plugins()
        self.load_hooks()

    def __getitem__(self, item):
        # Compatibility with the old version
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        # Compatibility with the old version
        self.__setattr__(key, value)

    def load_plugins(self):
        for plugin in config.plugin:
            try:
                logger.info(f"Loading plugin: {plugin}")
                temp = importlib.import_module(
                    f"gameyamlspiderandgenerator.plugin.{plugin}"
                )
                self.plugin[f"gameyamlspiderandgenerator.plugin.{plugin}"] = (
                    get_subclasses(temp, BasePlugin)
                )
            except ImportError as e:
                logger.debug(e)
                logger.error(f"Failed to import plugin: {plugin}")
            except NotImplementedError:
                logger.error(f"Imported plugin but no BasePlugin found: {plugin}")

    def load_hooks(self):
        if config.hook is None:
            logger.warning("All hooks are disabled")
            return
        for hook in config.hook:
            try:
                logger.info(f"Loading hook: {hook}")
                temp = importlib.import_module(f"yamlgenerator_hook_{hook}")
                self.hook[f"yamlgenerator_hook_{hook}"] = get_subclasses(temp, BaseHook)
                if (
                    self.hook[f"yamlgenerator_hook_{hook}"].REQUIRE_CONFIG
                    and hook not in config["hook_configs"]
                ):
                    raise ApiKeyNotFoundError(f"yamlgenerator_hook_{hook}")
            except ImportError as e:
                logger.debug(e)
                logger.error(f"Failed to import hook: {hook}")
            except NotImplementedError:
                logger.error(f"Imported hook but no BaseHook found: {hook}")


pkg = Package()
