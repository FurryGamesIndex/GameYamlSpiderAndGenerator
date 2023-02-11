from typing import Optional, AnyStr

from loguru import logger

from gameyamlspiderandgenerator.plugin import BasePlugin
from gameyamlspiderandgenerator.util.plugin_manager import pkg


def verify(url: str) -> Optional[BasePlugin]:
    verify_list = [
        [
            pkg.plugin[n].verify,
            pkg.plugin[n],
        ]
        for n in pkg.plugin
    ]
    return next((cls for func, cls in verify_list if func(url)), None)


def produce_yaml(url: str) -> Optional[AnyStr]:
    ret = verify(url)
    if ret is None:
        logger.error("URL is invalid")
        return
    return ret(url).to_yaml()
