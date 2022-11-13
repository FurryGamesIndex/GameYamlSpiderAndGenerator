if __name__=='__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn
from  util.setting import setting

def get_update(repo:  AnyStr | None)->Dict | SupportsInt:
    note_str='current github repo' if repo is None else repo
    repo_link=r'https://raw.githubusercontent.com/FurryGamesIndex/GameYamlSpiderAndGenerator/master/version.json' if repo is None else repo
    logger.info(f'using {setting["proxy"]} to get update form {note_str}')
    logger.info(repo_link)
    try:
        ver=requests.get(repo_link,proxies=setting['proxy'])
        if ver.status_code==200:
            return ver.json()
        else:
            return ver.status_code
    except Exception as e:
        logger.error(e)
        return -3
        
if __name__=='__main__':

    logger.info(get_update(None))

