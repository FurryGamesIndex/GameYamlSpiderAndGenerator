import importlib
from types import ModuleType

from loguru import logger

from gameyamlspiderandgenerator.util.setting import get_config


class Package:
    plugin: dict[str, ModuleType] = {}
    hook: dict[str, ModuleType] = {}


pkg = Package()


# TODO Rewrite this using __dict__
def load_plugins():
    global pkg
    if not pkg.plugin:
        try:
            print("Loading plugins...")
            for i in get_config()["plugin"]:
                logger.info(f"Loading plugin {i}")
                pkg.plugin[i] = importlib.import_module(
                    f"gameyamlspiderandgenerator.plugin.{i}"
                )
            for i in get_config()["hook"]:
                logger.info(f"Loading hook {i}")
                pkg.plugin[i] = importlib.import_module(
                    f"gameyamlspiderandgenerator.hook.{i}"
                )
        except Exception as e:
            logger.error(e)
    return pkg
