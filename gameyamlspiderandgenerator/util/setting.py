from typing import Dict


class Setting:
    proxy: Dict[str, str] = {}
    api: Dict[str, str] = {}


setting = Setting()


def config(data: dict):
    setting.__dict__.update(data)


def get_config():
    return setting.__dict__


def set_config(name: str, data: dict | list[str]):
    setting.__dict__[name] = data
