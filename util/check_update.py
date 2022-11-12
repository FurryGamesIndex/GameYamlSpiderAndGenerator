import requests
import yaml
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn
import json
def get_update(proxy: AnyStr | None,repo:  AnyStr | None)->Dict | SupportsInt:
    note_str='current github repo' if repo is None else repo
    repo_link=r'https://raw.githubusercontent.com/FurryGamesIndex/GameYamlSpiderAndGenerator/master/version.json' if repo is None else repo
    logger.info(f'using {proxy} to get update form {note_str}')
    logger.info(repo_link)
    try:
        ver=requests.get(repo_link,proxies=proxy)
        if ver.status_code==200:
            return json.loads(ver.text)
        else:
            return ver.status_code
    except Exception as e:
        logger.error(e)
        return -3
        
if __name__=='__main__':
    get_update({"http": "http://127.0.0.1:7890", "https": "socks5://127.0.0.1:7891"},None)

