import argparse
import importlib
import sys

from gameyamlspiderandgenerator.util.setting import get_config
from loguru import logger
from yaml import safe_load

pkg = {'plugin': {}, 'hook': {}}


def load_plugins():
    global pkg
    if not pkg['plugin']:
        for i in get_config()['plugin']:
            logger.info(f'Loading plugin {i}')
            pkg['plugin'][i] = importlib.import_module(f'.{i}', 'gameyamlspiderandgenerator.plugin')
        for i in get_config()['hook']:
            logger.info(f'Loading hook {i}')
            pkg['hook'][i] = importlib.import_module(f'.{i}', 'gameyamlspiderandgenerator.hook')
    return pkg
