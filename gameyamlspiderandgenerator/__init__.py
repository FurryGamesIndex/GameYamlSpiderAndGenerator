from typing import Optional

from loguru import logger

from .plugin import BasePlugin
from .util.fgi_yaml import YamlData
from .util.plugin_manager import pkg


def verify(url: str) -> Optional[BasePlugin]:
    verify_list = [
        [
            pkg.plugin[n].verify,
            pkg.plugin[n],
        ]
        for n in pkg.plugin
    ]
    return next((cls for func, cls in verify_list if func(url)), None)


def produce_yaml(url: str) -> Optional[YamlData]:
    ret: BasePlugin = verify(url)
    if ret is None:
        logger.error("URL is invalid")
        return
    return ret(url).to_yaml()
