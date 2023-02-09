import sys

from gameyamlspiderandgenerator.plugin.steam import Steam as Steam
from gameyamlspiderandgenerator.util.config import config

config.load("config.yaml")
config.set("hook", ["search"])
config.set("plugin", ["steam", "itchio"])


sys.path.append("../gameyamlspiderandgenerator")
sys.path.append("../gameyamlspiderandgenerator/util")

print(Steam("https://store.steampowered.com/app/381210/Dead_by_Daylight/").to_yaml())
