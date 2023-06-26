from .fgi_yaml import fgi
from .fgi import default_config
from ..exception import ReadOrWriteConfigFailed


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

    def load(self, file_data: str | dict = None):
        """

        Args:
            file_data:
                When the type is str, it is text in yaml format.

                When the type is dict, it is the serialized dictionary data.

                When it is empty, the default is the default configuration(see util.fgi.default_config)

        Returns:

        """
        if type(file_data) is dict:
            self.__dict__.update(file_data)
            return
        if file_data is None:
            self.__dict__.update(default_config)
            return
        try:
            with open(file_data, "r", encoding="utf-8") as fp:
                self.__dict__.update(fgi.load(fp))
        except Exception as e:
            raise ReadOrWriteConfigFailed from e

    def update(self, data: dict):
        self.__dict__.update(data)

    def __str__(self):
        fgi.preserve_quotes = True
        fgi.explicit_start = True
        fgi.indent = 1
        return fgi.dump_to_string(self.__dict__)


config = Config()
