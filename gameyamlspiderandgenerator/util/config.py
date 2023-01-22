from typing import List, Union


class Config:
    proxy = {}
    api = {}
    plugin = {}
    hook = {}

    def __getitem__(self, item):
        # Compatibility with the old version
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        # Compatibility with the old version
        self.__setattr__(key, value)

    def set(self, name: str, data: Union[dict, List[str]]):
        self.__setattr__(name, data)

    def update(self, data: dict):
        self.__dict__.update(data)

    def flush(self):
        self.__dict__.clear()


config = Config()
