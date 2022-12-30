import argparse
import importlib
import sys

from loguru import logger
from yaml import safe_load

pkg = {}


def load_plugins():
    global pkg
    for i in setting['plugin']:
        logger.info(f'Loading plugin {i}')
        pkg[i] = importlib.import_module(f'.{i}', 'gameyamlspiderandgenerator.plugin')


def verify(url: str):
    verify_list = []
    for n in pkg:
        if 'Search' in pkg[n].__dir__():
            verify_list.append(pkg[n].__getattribute__('Search').verify)
    return any([i(url) for i in verify_list])


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--config', type=str,
                    default={'plugin': ['steam', 'itchio']}, help="The location of config.yaml (default null)")
parser.add_argument('url', metavar='URL')
parser.add_argument('-push', action='store_true',
                    default=False, help='Whether push to github')
parser.add_argument('-pull', action='store_true',
                    default=False, help='Whether make a pull request to github')
args = parser.parse_args()

if isinstance(args.config, str):
    with open(args.config) as f:
        setting = safe_load(f)
else:
    setting = args.config
load_plugins()

print(verify('https://store.steampowered.com/app/1470120/Atopes/'))
print(verify('ht'))
print(verify('https://lunareffectdigital.itch.io/watches-you-'))
