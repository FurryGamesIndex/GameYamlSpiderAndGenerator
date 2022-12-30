import importlib
from util.setting import setting
from loguru import logger

pkg = {}


def load_plugins():
    global pkg
    for i in setting['plugin']:
        logger.info(f'Loading plugin {i}')
        pkg[i] = importlib.import_module(f'.{i}', 'plugin')


if __name__ == '__main__':
    load_plugins()
    print(pkg)
