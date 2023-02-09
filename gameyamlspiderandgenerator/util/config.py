from ruamel.yaml import YAML

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
                yaml = YAML()
                yaml.preserve_quotes = True
                self.__dict__.update(yaml.load(fp))
        except Exception:
            raise ReadOrWriteConfigFailed from None

    def update(self, data: dict):
        self.__dict__.update(data)

    def __str__(self):
        yaml = YAML(typ=["rt", "string"])
        yaml.explicit_start = True
        yaml.indent = 1
        return yaml.dump_to_string(self.__dict__)


config = Config()
