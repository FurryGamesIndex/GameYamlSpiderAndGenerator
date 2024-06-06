import zipfile
from dataclasses import dataclass
from io import BytesIO
from typing import Literal

from fgi_yaml_formattor import dump_to_yaml
from loguru import logger
from msgpack import dumps

from gameyamlspiderandgenerator.util.fgi_yaml import (
    process_thumbnail,
    get_valid_filename,
)

__all__ = ["DetailedMsg", "YamlData"]


@dataclass
class DetailedMsg:
    html: list[str] | str
    json: list[dict] | dict
    data: dict
    changed: dict
    program_name: str


@dataclass
class MetaData:
    logs: str
    plugin: DetailedMsg
    hooks: list[DetailedMsg]
    version: tuple[int]
    loaded_plugins: dict[Literal["plugins"] | Literal["hooks"], list[str]]


class YamlData:
    raw_dict: dict
    meta_data: MetaData = None

    def __init__(self, raw_data):
        self.raw_dict = raw_data

    def __str__(self):
        return dump_to_yaml({**self.raw_dict, "thumbnail": "thumbnail.png"})

    def __bytes__(self):
        from .util.spider import get_bytes

        _io = BytesIO()
        zip_data = zipfile.ZipFile(_io, "w", zipfile.ZIP_DEFLATED)
        if self.raw_dict["thumbnail"] is not None:
            img = get_bytes(self.raw_dict["thumbnail"])
            zip_data.writestr("thumbnail.png", process_thumbnail(img))
            logger.info("thumbnail exists")
        zip_data.writestr(
            get_valid_filename(self.raw_dict["name"]) + ".yaml",
            dump_to_yaml({**self.raw_dict, "thumbnail": "thumbnail.png"}),
        )
        if self.meta_data:
            zip_data.write("metadata.msgpack", dumps(self.meta_data, use_bin_type=True))
        zip_data.close()
        return _io.getvalue()
