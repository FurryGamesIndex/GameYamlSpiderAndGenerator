import argparse

from yaml import safe_load

from .util.config import config
from .util.fgi import default_config
from .util.fgi_yaml import get_valid_filename
from .util.plugin_manager import pkg
from loguru import logger
from gameyamlspiderandgenerator import produce_yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--config",
    type=str,
    default=default_config,
    help="The location of config.yaml (default null)",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default=None,
    help="The location of the output file (zip format or yaml format)",
)
parser.add_argument(
    "--lang",
    type=str,
    default='en',
    help="The display language of the game. ISO 639-1 code(default: en)",
)
parser.add_argument(
    "--fast",
    action='store_true',
    default=False,
    help="Whether to disable all hooks (default: false)",
)
parser.add_argument("url", metavar="URL")
args = parser.parse_args()
if isinstance(args.config, str):
    with open(args.config) as f:
        setting = safe_load(f)
else:
    setting = args.config
if args.fast:
    setting['hook'] = None
config.update(setting)
pkg.__init__()
yml = produce_yaml(args.url,args.lang)
if args.output is None:
    if yml is not None:
        print(yml)
    else:
        exit(2)
elif "." not in args.output:
    if args.output == "zip":
        with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
            f.write(bytes(yml))
    elif args.output == "yaml":
        with open(get_valid_filename(yml.raw_dict['name']) + ".yaml", 'w') as f:
            f.write(str(yml))
elif "." in args.output:
    if "zip" in args.output:
        with open(args.output, 'wb') as f:
            f.write(bytes(yml))
    elif "yaml" in args.output:
        with open(args.output, 'w') as f:
            f.write(str(yml))
    else:
        logger.error(f"unsupported file format: {args.output[args.output.rfind('.'):]}")
        exit(1)

else:
    logger.error(f"unsupported file format: {args.output[args.output.rfind('.'):]}")
    exit(1)
