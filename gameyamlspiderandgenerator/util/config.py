from gameyamlspiderandgenerator.exception import ReadOrWriteConfigFailed
from gameyamlspiderandgenerator.util.fgi_yaml import fgi


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
            with open(file_name, "r", encoding="utf-8") as fp:
                self.__dict__.update(fgi.load(fp))
        except Exception:
            raise ReadOrWriteConfigFailed from None

    def update(self, data: dict):
        self.__dict__.update(data)

    def __str__(self):
        fgi.preserve_quotes = True
        fgi.explicit_start = True
        fgi.indent = 1
        return fgi.dump_to_string(self.__dict__)


config = Config()
