if __name__ != "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from typing import AnyStr, Dict, SupportsInt

import requests
from loguru import logger

from gameyamlspiderandgenerator.util.setting import get_config

setting = get_config()


def get_json(url: AnyStr) -> SupportsInt | Dict:
    logger.info(setting)
    try:
        response = requests.get(url, proxies=setting["proxy"])
        return response.json() if response.status_code == 200 else response.status_code
    except Exception as e:
        logger.error(e)
        return -3


def get_text(url: AnyStr) -> SupportsInt | AnyStr:
    try:
        response = requests.get(url, proxies=setting["proxy"])
        return response.text if response.status_code == 200 else response.status_code
    except Exception as e:
        logger.error(e)
        return -3


def get_status(url: AnyStr) -> SupportsInt:
    try:
        return requests.get(url, proxies=setting["proxy"]).status_code
    except Exception as e:
        logger.error(e)
        return -3


def download_file(url: AnyStr, save: AnyStr) -> SupportsInt:
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            return response.status_code
        open(save, "wb").write(response.content)
        return 0
    except Exception as e:
        logger.error(e)
        return -3
