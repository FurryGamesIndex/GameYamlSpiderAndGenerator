import re
from io import BytesIO
import zipfile

from fgi_yaml_formattor import dump_to_yaml
from PIL import Image
from loguru import logger


def process_thumbnail(img_byte: bytes):
    img = Image.open(BytesIO(img_byte))
    if img.size == (460, 215):
        img_resize = img.resize((360, 168))
        ret_byte = BytesIO()
        img_resize.save(ret_byte, format="PNG", optimize=True, quality=85)
        return ret_byte.getvalue()
    logger.warning("Thumbnails cannot be scaled down.")
    return img_byte


def get_valid_filename(s: str):
    s = s.strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "_", s)


class YamlData:
    raw_dict: dict

    def __init__(self, raw_data):
        self.raw_dict = raw_data

    def __str__(self):
        return dump_to_yaml({**self.raw_dict, "thumbnail": "thumbnail.png"})

    def __bytes__(self):
        from ..util.spider import get_bytes

        _io = BytesIO()
        zip_data = zipfile.ZipFile(_io, "w", zipfile.ZIP_DEFLATED)
        if self.raw_dict["thumbnail"] is not None:
            img = get_bytes(self.raw_dict["thumbnail"])
            zip_data.writestr("thumbnail.png", process_thumbnail(img))
            logger.warning("thumbnail exists")
        zip_data.writestr(
            get_valid_filename(self.raw_dict["name"]) + ".yaml",
            dump_to_yaml({**self.raw_dict, "thumbnail": "thumbnail.png"}),
        )
        zip_data.close()
        return _io.getvalue()
