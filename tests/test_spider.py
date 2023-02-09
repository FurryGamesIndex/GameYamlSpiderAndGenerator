from loguru import logger

from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.spider import get_status, get_text

config.load("config.yaml")

logger.info(get_status("https://store.steampowered.com/"))
logger.info(get_text("https://www.so.com/"))
