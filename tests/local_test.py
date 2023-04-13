from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg

config.load("/home/keiplyer/桌面/config.yaml")
pkg.__init__()
yml = produce_yaml("https://store.steampowered.com/app/1470120/Atopes/")
print(yml)
with open(yml.raw_dict['name'] + ".zip", 'wb') as f:
    f.write(bytes(yml))
yml = produce_yaml("https://sokpop.itch.io/springblades")
print(yml)
with open(yml.raw_dict['name'] + ".zip", 'wb') as f:
    f.write(bytes(yml))
