from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg
from gameyamlspiderandgenerator.util.fgi_yaml import get_valid_filename
config.load("/home/keiplyer/桌面/config.yaml")
pkg.__init__()
yml = produce_yaml("https://finji.itch.io/tunic")
print(yml)
with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
    f.write(bytes(yml))
yml = produce_yaml("https://store.steampowered.com/app/290340/Armello/")
print(yml)
with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
    f.write(bytes(yml))
