import re
from jq import compile
from gameyamlspiderandgenerator import BasePlugin, YamlData


class Gcores(BasePlugin):
    _VERIFY_PATTERN = re.compile(r"https://www\.gcores\.com/games/(\d+)/?")
    jq = compile

    def __init__(self): ...
    def get_name(self) -> str:
        pass

    def get_desc(self) -> str:
        pass

    def get_brief_desc(self) -> str:
        pass

    def get_thumbnail(self) -> str:
        pass

    def get_authors(self) -> list[dict]:
        pass

    def get_tags(self) -> list[dict]:
        pass

    def get_misc_tags(self) -> list[dict]:
        pass

    def get_platforms(self) -> list[str]:
        pass

    def get_langs(self) -> list[str]:
        pass

    def get_links(self) -> list[dict]:
        pass

    def get_screenshots(self) -> list[str]:
        pass

    def to_yaml(self) -> YamlData:
        pass
