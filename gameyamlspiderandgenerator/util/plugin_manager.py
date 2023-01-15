import importlib
from typing import Literal

from loguru import logger

from gameyamlspiderandgenerator.hook import BaseHook
from gameyamlspiderandgenerator.plugin import BasePlugin
from gameyamlspiderandgenerator.util.setting import get_config, setting


class Package:
    plugin: dict[str, BasePlugin] = {}
    hook: dict[str, BaseHook] = {}

    def __getitem__(self, item):
        # Compatibility with the old version
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        # Compatibility with the old version
        self.__setattr__(key, value)

    @staticmethod
    def _run_hook(cls: BasePlugin | BaseHook, data: dict):
        cls.__load_hook__(data)

    def _load(
        self, _dir: Literal["plugin", "hook"], _type: type[BasePlugin] | type[BaseHook]
    ):
        base = __package__.split(".")[0] + "." + _dir
        for plugin in getattr(setting, _dir, []):
            try:
                logger.info(f"Loading {_dir}: {plugin}")
                module = importlib.import_module(f"{base}.{plugin}")
                target = [o for o in module.__dict__.values() if isinstance(o, _type)][
                    0
                ]
                self[_dir][plugin] = target
            except ImportError as e:
                logger.trace(e)
                logger.error(f"Failed to import {_dir}: {plugin}")
            except IndexError:
                logger.error(f"Import {_dir} but no {_type} found: {plugin}")

    def load_plugins(self):
        self._load("plugin", BasePlugin)

    def load_hooks(self):
        self._load("hook", BaseHook)


pkg = Package()


def load_plugins():
    if not pkg.plugin:
        try:
            logger.info("Loading plugins...")
            for i in get_config()["plugin"]:
                logger.info(f"Loading plugin {i}")
                pkg.plugin[i] = importlib.import_module(  # type: ignore
                    f"gameyamlspiderandgenerator.plugin.{i}"
                )
            for i in get_config()["hook"]:
                logger.info(f"Loading hook {i}")
                pkg.hook[i] = importlib.import_module(  # type: ignore
                    f"gameyamlspiderandgenerator.hook.{i}"
                )
        except Exception as e:
            logger.trace(e)
    return pkg
