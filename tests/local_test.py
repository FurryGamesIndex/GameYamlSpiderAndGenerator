from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg
from gameyamlspiderandgenerator.util.fgi_yaml import get_valid_filename
config.load("/home/keiplyer/桌面/config.yaml")
pkg.__init__()
yml = produce_yaml("https://store.steampowered.com/app/553420/TUNIC/")
print(yml)
with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
    f.write(bytes(yml))
yml = produce_yaml("https://store.steampowered.com/app/2121450/Bangkok_Story_A_Stray_Dog/")
print(yml)
with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
    f.write(bytes(yml))
