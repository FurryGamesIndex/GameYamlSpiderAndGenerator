import importlib
from typing import Literal

from loguru import logger

from gameyamlspiderandgenerator.hook import BaseHook
from gameyamlspiderandgenerator.plugin import BasePlugin
from gameyamlspiderandgenerator.util.config import config


class Package:
    plugin: dict[str, BasePlugin] = {}
    hook: dict[str, BaseHook] = {}

    def __init__(self):
        self.load_plugins()
        self.load_hooks()

    def __getitem__(self, item):
        # Compatibility with the old version
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        # Compatibility with the old version
        self.__setattr__(key, value)

    def _load(
        self, _dir: Literal["plugin", "hook"], _type: type[BasePlugin] | type[BaseHook]
    ):
        base = __package__.split(".")[0] + "." + _dir
        for plugin in getattr(config, _dir, []):
            if plugin.startswith("_"):
                logger.warning(f"Skip loading protected {_dir} {plugin}")
                continue
            try:
                package = f"{base}.{plugin}"
                logger.info(f"Loading {_dir}: {plugin}")
                module = importlib.import_module(package)
                target = [
                    o
                    for o in module.__dict__.values()
                    if isinstance(o, type) and issubclass(o, _type) and o is not _type
                ][-1]
                if target in self[_dir].values():
                    logger.warning(f"Skip loading duplicate {_dir} {plugin}")
                    continue
                self[_dir][plugin] = target
            except ImportError as e:
                logger.trace(e)
                logger.error(f"Failed to import {_dir}: {plugin}")
            except IndexError:
                logger.error(f"Imported {_dir} but no {_type.__name__} found: {plugin}")

    def load_plugins(self):
        self._load("plugin", BasePlugin)

    def load_hooks(self):
        self._load("hook", BaseHook)


pkg = Package()
