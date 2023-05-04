import argparse

from yaml import safe_load

from . import verify
from .util.config import config
from .util.plugin_manager import pkg
import sys
from loguru import logger
from gameyamlspiderandgenerator import produce_yaml

parser = argparse.ArgumentParser()
logger.remove()
logger.add(sys.stderr, level="ERROR")
parser.add_argument(
    "-f",
    "--config",
    type=str,
    default={"plugin": ["steam", "itchio"], "hook": ["search"]},
    help="The location of config.yaml (default null)",
)
parser.add_argument("url", metavar="URL")
args = parser.parse_args()

if isinstance(args.config, str):
    with open(args.config) as f:
        setting = safe_load(f)
else:
    setting = args.config
config.update(setting)
pkg.__init__()


print(produce_yaml(args.url))