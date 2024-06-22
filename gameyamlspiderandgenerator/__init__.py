import sys
from collections.abc import Callable
from inspect import signature

from loguru import logger


from .exception import InvalidUrlError, PluginNotLoadedError
from .plugin import BasePlugin
from .util.fgi_yaml import YamlData
from .util.plugin_manager import pkg

logger.remove()
logger.add(sys.stdout, level="WARNING")


def verify(url: str) -> Callable[..., BasePlugin] | None:
    if not pkg.plugin:
        _ = PluginNotLoadedError()
        _.add_note("Did you forget to use config.load()?")
        raise _
    verify_list = [
        [
            pkg.plugin[n].verify,
            pkg.plugin[n],
        ]
        for n in pkg.plugin
    ]
    return next((cls for func, cls in verify_list if func(url)), None)


def produce_yaml(url: str, lang: str = "en") -> YamlData | None:
    ret = verify(url)
    if ret is None:
        raise InvalidUrlError(url)
    if "lang" in [i.name for i in signature(ret).parameters.values()]:
        return ret(url, lang).to_yaml()
    else:
        return ret(url).to_yaml()
