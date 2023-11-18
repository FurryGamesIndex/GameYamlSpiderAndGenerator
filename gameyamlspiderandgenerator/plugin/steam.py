import concurrent.futures
import re
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
from html2text import html2text
from langcodes import find, Language
from yaml import dump

from ._base import BasePlugin
from ..util.fgi import fgi_dict
from ..util.fgi_yaml import YamlData
from ..util.spider import get_json, get_text


class Steam(BasePlugin):
    _VERIFY_PATTERN = re.compile(r"https?://store\.steampowered\.com/app/\d+/.+/?.+")

    @staticmethod
    def get_steam_id(link: str) -> int:
        return int(urlparse(link).path.split("/")[2])

    def get_name(self):
        return self.data[str(self.id)]["data"]["name"]

    @staticmethod
    def remove_query(s: str):
        s = re.sub(r"\?t=\d{6,12}", "", s)
        return s.replace("![]", "![img]")

    def __init__(self, link: str, lang: str = 'en') -> None:
        self.id = self.get_steam_id(link)
        if lang != 'en':
            print(dump(get_json(
                f'https://store.steampowered.com/api/appdetails?appids={self.id}&l={Language.get(lang).display_name("en").lower()}'),
                allow_unicode=True))
        result = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result.append(
                executor.submit(get_json, f"https://store.steampowered.com/api/appdetails?appids={self.id}&l=english"))
            result.append(executor.submit(get_text, link))
        self.data, self.data_html = (result[0].result(), result[1].result())
        self.soup = BeautifulSoup(self.data_html, "lxml")
        self.name = self.get_name()
        temp1 = self.soup.body.find_all("a", {"class": "app_tag"})
        self.tag = [re.sub(r"[\n\t\r]*", "", temp1[i].text) for i in range(len(temp1))]

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
                "publish": ["steam"],
                "misc": self.get_misc_tags(),
            },
            "links": self.get_links(),
            "thumbnail": self.get_thumbnail(),
            "screenshots": self.get_screenshots() + self.get_video(),  # type: ignore
        }
        return YamlData(self.__load_hook__(ret))

    def get_langs(self) -> list[str]:
        temp = self.data[str(self.id)]["data"]["supported_languages"].split(",")
        return list({find(i).language for i in temp})

    def get_desc(self):
        return self.remove_query(
            (
                html2text(
                    self.data[str(self.id)]["data"]["detailed_description"],
                    bodywidth=0,
                )
            )
        ).replace("\n" * 4, "\n").strip()

    def get_brief_desc(self):
        return html2text(self.data[str(self.id)]["data"]["short_description"], bodywidth=0)

    def get_authors(self) -> list[dict]:
        temp = self.data[str(self.id)]["data"]
        developers = [{"name": i.strip(), "role": ["producer"]} for i in temp["developers"]]
        publishers = [{"name": i.strip(), "role": ["publisher"]} for i in temp["publishers"]]
        return developers + publishers

    def get_platforms(self):
        temp = self.data[str(self.id)]["data"]["platforms"]
        repl = {"windows": "windows", "mac": "macos", "linux": "linux"}
        return [repl[i] for i in temp if temp[i]]

    def get_type_tag(self):
        repl = {
            "Adventure": "adventure",
            "Action": "action",
            "Visual Novel": "visual-novel",
            "Strategy": "strategy",
            "RTS": "real-time-strategy",
            "Casual": "casual",
            "Management": "business-sim",
            "Card Game": "board",
            "Fighting": "fighting",
            "Music": "music",
            "Shooter": "shooter",
            "Puzzle": "puzzle",
            "RPG": "role-playing",
            "MMORPG": "mmorpg",
            "Dating Sim": "dating-sim",
            "Roguel": "roguelike",
            "Sports": "sports",
            "Comedy": "comedy",
            "Horror": "horror",
        }

        ret = []
        for i, value in repl.items():
            ret.extend(value for ii in self.tag if i in ii)
        return list(set(ret))

    def get_tags(self) -> list[str]:
        return self.tag

    def get_misc_tags(self):
        repl = {
            "3D": "3d",
            "Pixel": "pixel-art",
            "Multiplayer": "multiplayer",
            "PvP": "pvp",
            "Sexual": "uncensored",
            "Nudity": "uncensored",
            "Free to Play": "freeware",
            "Story Rich": "multiple-endings",
            "JRPG": "multiple-endings",
            "Co-Op": "co-op",
            "Online": "online",
        }
        ret = []
        for i, value in repl.items():
            ret.extend(value for ii in self.tag if i in ii)
        return list(set(ret))

    def get_if_nsfw(self):
        return (
                self.soup.body.find_all("div", {"id": "game_area_content_descriptors"})
                != []
        )

    def get_screenshots(self):
        return [
            self.remove_query(i["path_full"])
            for i in self.data[str(self.id)]["data"]["screenshots"]
        ]

    def get_video(self):
        is_nsfw = self.get_if_nsfw()
        video_webm = [
            self.remove_query(i["webm"]["max"]).replace("http", "https")
            for i in self.data[str(self.id)]["data"]["movies"]
        ]
        video_mp4 = [
            self.remove_query(i["mp4"]["max"]).replace("http", "https")
            for i in self.data[str(self.id)]["data"]["movies"]
        ]
        return [
            {
                "video": [{"mime": "video/webm", "sensitive": is_nsfw, "uri": video_webm[i], },
                          {"mime": "video/mp4", "sensitive": is_nsfw, "uri": video_mp4[i]},
                          ]
                if is_nsfw
                else [
                    {"mime": "video/webm", "uri": video_webm[i]},
                    {"mime": "video/mp4", "uri": video_mp4[i]},
                ],
            }
            for i in range(len(video_webm))
        ]

    def get_links(self) -> list[dict]:
        def remove_query_string(x: str):
            return parse_qs(urlparse(x).query)["u"][0] if "linkfilter" in x else x

        temp1 = self.soup.body.find(
            "div",
            attrs={"class": "game_area_description"},
        )
        temp3 = self.soup.body.find("div", attrs={"style": "padding-top: 14px;"})
        temp2 = temp3.find_all("a")
        temp4 = [
            remove_query_string(i["data-tooltip-text"])
            for i in temp2
            if "data-tooltip-text" in i.attrs
        ]
        temp = temp1.select("a[href]")
        ret = []
        for i in temp:
            ret.append(remove_query_string(i.attrs["href"]))
        data = [{"url": i, "processed": False} for i in list(set(ret + temp4))]
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
        processed_data.append({"name": ".steam", "uri": f'steam:{self.id}'})
        return processed_data

    def get_thumbnail(self):
        return self.remove_query(
            self.soup.body.find("img", {"class": "game_header_image_full"}).attrs["src"]
        )
