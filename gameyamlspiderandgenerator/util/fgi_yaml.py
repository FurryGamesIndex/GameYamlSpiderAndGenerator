import re
from io import BytesIO

from loguru import logger
from PIL import Image


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
