import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import yaml
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn


def init() -> Dict | SupportsInt:
    try:
        logger.info('Reading config.yaml...')
        with open('../config.yaml', 'r') as f:
            return yaml.safe_load(f.read())
    except Exception as e:
        logger.critical(e)
        return -1


def read_config(name: AnyStr) -> Dict | SupportsInt:
    try:
        logger.info(f'Reading {name}...')
        with open(name, 'r') as f:
            return yaml.safe_load(f.read())
    except Exception as e:
        logger.error(e)
        return -2


def save_config(name: AnyStr, data: Dict) -> NoReturn | SupportsInt:
    try:
        logger.info(f'Saving {name}...')
        with open(name, 'w') as f:
            yaml.safe_dump(data, f, indent=3)
    except Exception as e:
        logger.error(e)
        return -2


if __name__ == '__main__':
    save_config('s.yaml', {"test": {'2': None, '3': ['ghjgh', 'dsfghdfh']}})
    logger.info(read_config('s.yaml'))
    logger.info(read_config('.yaml'))
    os.remove('s.yaml')
