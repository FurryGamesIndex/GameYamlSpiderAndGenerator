import argparse
import os
import sys
from importlib.metadata import version

from loguru import logger
from yaml import safe_load

from gameyamlspiderandgenerator import produce_yaml
from .util.config import config
from .util.fgi import default_config
from .util.fgi_yaml import get_valid_filename
from .util.plugin_manager import pkg

logger.remove()
logger.add(sys.stdout, level="WARNING")
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

# 添加 --silent 参数到互斥组中
group.add_argument(
    "--silent", action="store_true", default=False, help="Enable silent log mode"
)

# 添加 --debug 参数到互斥组中
group.add_argument(
    "--debug", action="store_true", default=False, help="Enable debug log mode"
)

parser.add_argument(
    "-f",
    "--config",
    type=str,
    default=default_config,
    help="The location of config.yaml (default null)",
)
parser.add_argument(
    "--proxy",
    type=str,
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
    default="en",
    help="The display language of the game. ISO 639-1 code(default: en)",
)
parser.add_argument(
    "--fast",
    action="store_true",
    default=False,
    help="Whether to disable all hooks (default: false)",
)
parser.add_argument("url", metavar="URL")
args = parser.parse_args()
if args.debug:
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")
if args.silent:
    logger.remove()
logger.debug(sys.version)
logger.debug("version: " + version("gameyamlspiderandgenerator"))
if isinstance(args.config, str):
    with open(args.config) as f:
        setting = safe_load(f)
else:
    setting = args.config
if args.fast:
    setting["hook"] = None
if args.proxy:
    setting["proxy"] = {"http": args.proxy, "https": args.proxy}


def getenv_case_insensitive(key):
    # 使用 next() 函数获取第一个找到的匹配环境变量的值，不区分大小写
    return next((v for k, v in os.environ.items() if k.lower() == key.lower()), None)


if getenv_case_insensitive("HTTP_PROXY"):
    setting["proxy"] = {
        "http": getenv_case_insensitive("HTTP_PROXY"),
        "https": getenv_case_insensitive("HTTPS_PROXY"),
    }
config.update(setting)
pkg.init()
yml = produce_yaml(args.url, args.lang)
if args.output is None:
    if yml is not None:
        print(yml)
    else:
        exit(2)
elif "." not in args.output:
    if args.output == "zip":
        with open(get_valid_filename(yml.raw_dict["name"]) + ".zip", "wb") as f:
            f.write(bytes(yml))
    elif args.output == "yaml":
        with open(get_valid_filename(yml.raw_dict["name"]) + ".yaml", "w") as f:
            f.write(str(yml))
elif "." in args.output:
    if "zip" in args.output:
        with open(args.output, "wb") as f:
            f.write(bytes(yml))
    elif "yaml" in args.output:
        with open(args.output, "w") as f:
            f.write(str(yml))
    else:
        logger.error(f"unsupported file format: {args.output[args.output.rfind('.'):]}")
        exit(1)

else:
    logger.error(f"unsupported file format: {args.output[args.output.rfind('.'):]}")
    exit(1)
