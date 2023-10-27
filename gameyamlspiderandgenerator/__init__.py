from inspect import signature
from typing import Optional, Callable

from loguru import logger

from .util.fgi_yaml import YamlData
from .util.plugin_manager import pkg


def verify(url: str) -> Callable:
    if not pkg.plugin:
        raise Exception("Plugin not yet loaded")
    verify_list = [
        [
            pkg.plugin[n].verify,
            pkg.plugin[n],
        ]
        for n in pkg.plugin
    ]
    return next((cls for func, cls in verify_list if func(url)), None)


def produce_yaml(url: str, lang: str = "en") -> Optional[YamlData]:
    ret = verify(url)
    if ret is None:
        logger.error("URL is invalid")
        return
    if 'lang' in [i.name for i in signature(ret).parameters.values()]:
        return ret(url, lang).to_yaml()
    else:
        return ret(url).to_yaml()
