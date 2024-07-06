from fgi_yaml_formattor import fgi
from .fgi import default_config
from ..exception import ReadOrWriteConfigFailed
from dataclasses import dataclass, field
from deprecated import deprecated


@dataclass
class Config:
    proxy: field(default_factory=dict)
    hook: field(default_factory=dict)
    hook_configs: field(default_factory=dict)
    git_proxy: str

    def __getitem__(self, item):
        return self.__dict__[item]

    def load(self, file_data: str | dict = None):
        """

        Args:
            file_data:
                When the type is str, it is text in yaml format.

                When the type is dict, it is the serialized dictionary data.

                When it is empty, the default is the default configuration(see util.fgi.default_config)

        Returns:

        """
        if isinstance(file_data, dict):
            self.__dict__.update(file_data)
            return
        try:
            with open(file_data, encoding="utf-8") as fp:
                self.__dict__.update(fgi.load(fp))
        except Exception as e:
            raise ReadOrWriteConfigFailed from e

    @deprecated(version="2.0.2b")
    def update(self, data: dict):
        self.load(data)


config = Config(**default_config)
