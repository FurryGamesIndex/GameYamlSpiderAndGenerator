import re
from contextlib import suppress
from json import loads
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

    def __init__(self, link: str) -> None:
        self.link = link
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
        th = self.soup.select_one("#header > img")
        if th is None:
            return None
        return th.attrs["src"]

    def get_brief_desc(self):
        return (
            pss_dedent(self.data["aggregateRating"]["description"])
            if "description" in self.data["aggregateRating"]
            else ""
        )

    def get_name(self):
        return self.data["name"]

    def get_screenshots(self):
        temp = self.soup.select_one("div.columns > div.right_col.column > div.screenshot_list").select('a')
        return [i.attrs['href'] for i in temp]

    def get_desc(self):
        return pss_dedent(self.remove_query(html2text(
            str(self.soup.select_one("div.formatted_description.user_formatted")),
            bodywidth=0,
        )).replace("\n" * 4, "\n").strip())

    def get_platforms(self):
        repl = {
            "Windows": "windows",
            "macOS": "macos",
            "Linux": "linux",
            "Android": "android",
            "HTML5": "web",
            "iOS": "ios",
        }
        platforms = self.more_info["Platforms"][0].split(",") if "Platforms" in self.more_info else ["Windows"]
        return [repl[i.strip()] for i in platforms]

    def get_authors(self) -> list[dict]:
        temp = []
        if "Authors" in self.more_info:
            temp = self.more_info["Authors"]
        elif "Author" in self.more_info:
            temp = self.more_info["Author"]
        return [{"name": i.strip(), "role": ["producer"]} for i in temp]

    def get_tags(self) -> list[str]:
        temp = self.more_info["Genre"] if "Genre" in self.more_info else []
        temp1 = self.more_info["Made with"] if "Made with" in self.more_info else []
        temp2 = self.more_info["Tags"] if "Tags" in self.more_info else []
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

    def get_langs(self) -> list[str]:
        temp = self.more_info["Languages"] if "Languages" in self.more_info else ["English"]
        return list(set(find(i).language for i in temp))

    def get_links(self) -> list[dict]:
        link = [i.attrs["href"] for i in self.soup.select_one("div.left_col.column > "
                                                              "div.formatted_description.user_formatted").select("a["
                                                                                                                 "href]")]
        data = [{"url": i, "processed": False} for i in list(set(link))]
        processed_data = []
        for i in data:
            for p in fgi_dict:
                if re.match(p["match"], i["url"]):
                    processed_data.append(
                        {
                            "name": p["prefix"],
                            "uri": re.sub(p["match"], p["replace"], i["url"]),
                        }
                    )
                    i["processed"] = True
        for i in data:
            if not i["processed"]:
                processed_data.append({"name": ".website", "uri": i["url"]})
        processed_data.append({"name": ".itchio", "uri": self.link})
        return processed_data

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

    def to_yaml(self) -> YamlData:
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
                "publish": [".itchio"],
                "misc": self.get_misc_tags(),
            },
            "links": self.get_links(),
            "thumbnail": self.get_thumbnail(),
            "screenshots": self.get_screenshots()  # + self.get_video(),
        }
        return YamlData(self.__load_hook__(ret))

    def get_type_tag(self):
        repl = {
            "Visual Novel": "visual-nove",
            "Real time strategy": "real-time-strategy",
            "Strategy": "strategy",
            "Casual": "casual",
            "Adventure": "adventure",
            "Board Game": "board",
            "Action": "action",
            "Fantasy": "fantasy",
            "Fighting": "fighting",
            "Music": "music",
            "Shooter": "shooter",
            "Puzzle": "puzzle",
            "RPG": "role-playing",
            "MMORPG": "mmorpg",
            "Dating Sim": "dating-sim",
            "Roguelike": "roguelike",
            "Sports": "Sports",
            "Bara": "bara",
            "Yuri": "yuri",
            "Gore": "gore",
            "Comedy": "comedy",
            "tragedy": "tragedy",
            "Horror": "horror"
        }

        ret = []
        for i, value in repl.items():
            ret.extend(value for ii in self.tag if i in ii)
        return list(set(ret))
