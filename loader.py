import importlib

obj=importlib.import_module('plugin.steam',None).__dir__()
print(obj)
#print(obj.make_yaml)
