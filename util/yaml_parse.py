import yaml
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn


def init() -> Dict | SupportsInt:
    try:
        logger.info('Reading config.yaml...')
        with open('config.yaml', 'r') as f:
            return yaml.load(f.read())
    except Exception as e:
        logger.error(e)
        return -1


def read_config(name: AnyStr) -> Dict | SupportsInt:
    try:
        logger.info(f'Reading {name}...')
        with open(name, 'r') as f:
            return yaml.load(f.read())
    except Exception as e:
        logger.error(e)
        return -2


def save_config(name: AnyStr) -> NoReturn | SupportsInt:
    try:
        logger.info(f'Reading {name}...')
        with open(name, 'r') as f:
            return yaml.load(f.read())
    except Exception as e:
        logger.error(e)
        return -2
