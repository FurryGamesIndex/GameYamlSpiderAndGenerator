import argparse

from yaml import safe_load

from gameyamlspiderandgenerator.plugin import BasePlugin
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--config",
    type=str,
    default={"plugin": ["steam", "itchio"], "hook": ["search"]},
    help="The location of config.yaml (default null)",
)
parser.add_argument("url", metavar="URL")
parser.add_argument(
    "--push", action="store_true", default=False, help="Whether push to github"
)
parser.add_argument(
    "--pull",
    action="store_true",
    default=False,
    help="Whether make a pull request to github",
)
args = parser.parse_args()

if isinstance(args.config, str):
    with open(args.config) as f:
        setting = safe_load(f)
else:
    setting = args.config
config.update(setting)


def verify(url: str) -> BasePlugin | None:
    verify_list = [
        [
            pkg.plugin[n].verify,
            pkg.plugin[n],
        ]
        for n in pkg.plugin
    ]
    return next((cls for func, cls in verify_list if func(url)), None)


print(verify("https://store.steampowered.com/app/1470120/Atopes/"))
print(verify("ht"))
print(verify("https://lunareffectdigital.itch.io/watches-you-"))
