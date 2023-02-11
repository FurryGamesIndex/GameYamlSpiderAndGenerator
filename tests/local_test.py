from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg

config.load("/home/keiplyer/桌面/config.yaml")
pkg.__init__()
print(produce_yaml("https://store.steampowered.com/app/1470120/Atopes/"))
