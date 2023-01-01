from loguru import logger
from gameyamlspiderandgenerator.util.setting import config, set_config

config({"proxy": {"http": r'http://127.0.0.1:7890', "https": r'socks5://127.0.0.1:7891'},
        "api": {'google-play': 'a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90',
                'apple': 'a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90'}
        })
set_config('hook', ["search"])
set_config('plugin', ["steam", "itchio"])
from gameyamlspiderandgenerator.util.spider import get_status, get_text

logger.info(get_status('https://store.steampowered.com/'))
logger.info(get_text('https://www.so.com/'))
