if __name__=='__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn
import requests
from util.setting import setting

def get_json(url: AnyStr) -> SupportsInt | Dict:
    try:
        response = requests.get(url,proxies=setting['proxy'])
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
    except Exception as e:
        logger.error(e)
        return -3


def get_text(url: AnyStr) -> SupportsInt | AnyStr:
    try:
        response = requests.get(url,proxies=setting['proxy'])
        if response.status_code == 200:
            return response.text
        else:
            return response.status_code
    except Exception as e:
        logger.error(e)
        return -3
def get_status(url: AnyStr) -> SupportsInt:
    try:
        return requests.get(url,proxies=setting['proxy']).status_code
    except Exception as e:
        logger.error(e)
        return -3

if __name__ == '__main__':

    logger.info(get_json('https://raw.githubusercontent.com/FurryGamesIndex/GameYamlSpiderAndGenerator/master/version.json'))
    logger.info(get_text('https://www.so.com/'))

