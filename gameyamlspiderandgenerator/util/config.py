from typing import List, Union

from ruamel.yaml import round_trip_load, round_trip_dump

from gameyamlspiderandgenerator.exception import ReadOrWriteConfigFailed


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

    def load(self, file_name: str):
        try:
            with open(file_name, "r+") as fp:
                self.update(round_trip_load(fp, preserve_quotes=True))
        except Exception:
            raise ReadOrWriteConfigFailed from None

    def set(self, name: str, data: Union[dict, List[str]]):
        self.__setattr__(name, data)

    def update(self, data: dict):
        self.__dict__.update(data)

    def flush(self):
        self.__dict__.clear()

    def __str__(self):
        return round_trip_dump(self.__dict__, indent=1, explicit_start=True)


config = Config()
