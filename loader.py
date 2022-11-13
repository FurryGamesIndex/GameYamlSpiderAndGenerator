import importlib
import os
from util.setting import setting

pkg={}
def load_plugins():
    global pkg
    for i in setting['plugin']:
        pkg[i]=importlib.import_module(f'.{i}','plugin')
if __name__=='__main__':
    load_plugins()
    print(pkg)
