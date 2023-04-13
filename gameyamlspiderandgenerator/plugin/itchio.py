import itertools
import re
from contextlib import suppress
from json import loads
from re import match, sub
from typing import AnyStr, List

from bs4 import BeautifulSoup
from html2text import html2text
from langcodes import find

from ._base import BasePlugin
from ..util.fgi import fgi_dict
from ..util.fgi_yaml import YamlData, pss_dedent
from ..util.spider import get_text


class ItchIO(BasePlugin):
    _VERIFY_PATTERN = re.compile(r"https?://.+\.itch\.io/.+")

    @staticmethod
    def remove_query(s: str):
        s = re.sub(r"\?t=\d{6,12}", "", s)
        return s.replace("![]", "![img]")

    def __init__(self, link: AnyStr) -> None:
        self.data_html = get_text(link)
        self.soup = BeautifulSoup(self.data_html, "html.parser")
        self.data = [
            ii
            for ii in [
                loads(i.text)
                for i in self.soup.find_all(
                    "script", attrs={"type": "application/ld+json"}
                )
            ]
            if "name" in ii
        ][0]
        self.more_info = self.get_more_info()
        self.tag = self.get_tags()

    def get_thumbnail(self):
        return self.soup.select_one("#header > img").attrs["src"]

    def get_brief_desc(self):
        return (
            pss_dedent(self.data["aggregateRating"]["description"])
            if "description" in self.data["aggregateRating"]
            else None
        )

    def get_name(self):
        return self.data["name"]

    def get_screenshots(self):
        return [
            i.attrs["src"]
            for i in self.soup.find_all("img", attrs={"class": "screenshot"})
        ]

    def get_desc(self):
        return pss_dedent(self.remove_query(html2text(
            str(self.soup.select_one("div.formatted_description.user_formatted")),
            bodywidth=0,
        )).strip())

    def get_platforms(self):
        repl = {
            "Windows": "windows",
            "macOS": "macos",
            "Linux": "linux",
            "Android": "android",
            "HTML5": "web",
            "iOS": "ios",
        }
        platforms = self.more_info["Platforms"][0].split(",")
        return [repl[i.strip()] for i in platforms]

    def get_authors(self) -> List[dict]:
        temp = self.more_info["Author"]
        return [{"name": i, "role": "developer"} for i in temp]

    def get_tags(self) -> List[str]:
        temp = self.more_info["Genre"] if "Genre" in self.more_info else []
        temp1 = self.more_info["Made with"] if "Made with" in self.more_info else []
        temp2 = self.more_info["Tags"]
        return [i.strip() for i in (temp2 + temp1 + temp)]

    def get_misc_tags(self):
        repl = {
            "3D": "3d",
            "Pixel Art": "pixel-art",
            "free": "freeware",
            "Multiplayer": "multiplayer",
            "Co-op": "co-op",
            "PvP": "pvp",
            "Ren'Py": "engine-renpy",
            "Unity": "engine-unity",
            "RPG Maker": "engine-rpg-maker",
            "Godot": "engine-godot",
            "ue4": "engine-ue4",
            "unreal - engine - 4": "engine-ue4",
            "TyranoBuilder": "engine-tyranobuilder",
            "Flash": "adobe-flash",
            "t-series": "multiple-series",
            "Multiple Endings": "multiple-endings",
        }

        ret = []
        for i, value in repl.items():
            ret.extend(value for ii in self.tag if i in ii)
        return list(set(ret))

    def get_langs(self) -> List[str]:
        temp = self.more_info["Languages"] if "Languages" in self.more_info else ["English"]
        return list(set(find(i).language for i in temp))

    def get_links(self) -> List[dict]:
        link = [i.attrs["href"] for i in self.soup.select("a[href]")]
        data = list(list(set(link)))
        return [
            {"name": p["prefix"], "uri": sub(p["match"], p["replace"], i)}
            for i, p in itertools.product(data, fgi_dict)
            if match(p["match"], i)
        ]

    def get_more_info(self):
        d = {}
        for i in range(1, 18):
            with suppress(Exception):
                cache = self.soup.select_one(
                    f"div.info_panel_wrapper > div > table > tbody > tr:nth-child({str(i)})"
                )
                temp = [i.get_text() for i in list(cache.children)]
                d[temp[0]] = temp[1:][0].split(",")
        return d

    def __load_hook__(self, data: dict):
        from gameyamlspiderandgenerator.util.plugin_manager import pkg

        temp = data.copy()
        for _ in pkg["hook"].values():
            temp = pkg["hook"].Search(self.get_name()).setup(temp)
        return temp

    def to_yaml(self) -> YamlData:
        if type(self.data) == int:
            return self.data
        ret = {
            "name": self.get_name(),
            "brief-description": self.get_brief_desc(),
            "description": self.get_desc(),
            "description-format": "markdown",
            "authors": self.get_authors(),
            "tags": {
                "type": self.get_type_tag(),
                "lang": self.get_langs(),
                "platform": self.get_platforms(),
                "misc": self.get_misc_tags(),
            },
            "links": self.get_links(),
            "thumbnail": self.get_thumbnail(),
            "screenshots": self.get_screenshots()  # + self.get_video(),
        }
        return YamlData(ret)

    def get_type_tag(self):
        pass
