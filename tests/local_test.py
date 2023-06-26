from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg
from gameyamlspiderandgenerator.util.fgi_yaml import get_valid_filename
import time


def get_time(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print('耗时：{:.2f}秒'.format(e_time - s_time))
        return res

    return inner


config.load("C:\\Users\\Administrator\\Desktop\\config.yaml")
pkg.__init__()


@get_time
def test1():
    yml = produce_yaml("https://finji.itch.io/longest-night")
    print(yml)
    with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
        f.write(bytes(yml))


@get_time
def test2():
    yml = produce_yaml("https://store.steampowered.com/app/1470120/Atopes/")
    print(yml)
    with open(get_valid_filename(yml.raw_dict['name']) + ".zip", 'wb') as f:
        f.write(bytes(yml))


test1()
test2()
