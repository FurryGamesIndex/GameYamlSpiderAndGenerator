import concurrent.futures
import re
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
from html2text import html2text
from langcodes import Language, find

from .. import BasePlugin, YamlData
from ..util.fgi import fgi_dict
from ..util.spider import get_json, get_text


class Steam(BasePlugin):
    _VERIFY_PATTERN = re.compile(r"https?://store\.steampowered\.com/app/\d+/.+/?.+")

    @staticmethod
    def get_steam_id(link: str) -> int:
        return int(urlparse(link).path.split("/")[2])

    def get_name(self):
        return (
            self.data[str(self.id)]["data"]["name"]
            if self.lang == "en"
            else self.lang[3]
        )

    def __init__(self, link: str, lang: str = "en") -> None:
        self.id = self.get_steam_id(link)
        self.json = get_json(
            f"https://store.steampowered.com/api/appdetails?appids="
            f"{self.id}&l={Language.get(lang).display_name('en').lower()}",
            headers={"Accept-Language": lang, "Content-Language": lang},
        )[str(self.id)]
        self.lang = (
            lang,
            self.json["data"]["detailed_description"],
            self.json["data"]["short_description"],
            self.json["data"]["name"],
        )
        result = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result.append(
                executor.submit(
                    get_json,
                    f"https://store.steampowered.com/api/appdetails?appids={self.id}&l=english",
                )
            )
            result.append(executor.submit(get_text, link))
        self.data, self.data_html = (result[0].result(), result[1].result())
        self._soup = BeautifulSoup(self.data_html, "lxml")
        self.name = self.get_name()
        _app_tag = self._soup.body.find_all("a", {"class": "app_tag"})
        self.tag = [re.sub(r"[\n\t\r]*", "", i.text) for i in _app_tag]

    def to_yaml(self):
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
            "screenshots": self.get_screenshots() + self.get_video(),
        }
        return YamlData(self._load_hook(ret))

    def get_langs(self):
        temp = self.data[str(self.id)]["data"]["supported_languages"].split(",")
        return list({find(i).language for i in temp})

    def get_desc(self):
        return (
            self._remove_query(
                html2text(
                    self.data[str(self.id)]["data"]["detailed_description"],
                    bodywidth=0,
                )
                if self.lang[0] == "en"
                else html2text(
                    self.lang[1],
                    bodywidth=0,
                )
            )
            .replace("\n" * 4, "\n")
            .strip()
        )

    def get_brief_desc(self):
        return html2text(
            self.data[str(self.id)]["data"]["short_description"]
            if self.lang[0] == "en"
            else self.lang[2],
            bodywidth=0,
        )

    def get_authors(self):
        temp = self.data[str(self.id)]["data"]
        developers = [
            {"name": i.strip(), "role": ["producer"]} for i in temp["developers"]
        ]
        publishers = [
            {"name": i.strip(), "role": ["publisher"]} for i in temp["publishers"]
        ]
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

    def get_tags(self):
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
        return bool(
            self._soup.body.find_all("div", {"id": "game_area_content_descriptors"})
        )

    def get_screenshots(self):
        return [
            self._remove_query(i["path_full"])
            for i in self.data[str(self.id)]["data"]["screenshots"]
        ]

    def get_video(self):
        is_nsfw = self.get_if_nsfw()
        video_webm = [
            self._remove_query(i["webm"]["max"]).replace("http", "https")
            for i in self.data[str(self.id)]["data"]["movies"]
        ]
        video_mp4 = [
            self._remove_query(i["mp4"]["max"]).replace("http", "https")
            for i in self.data[str(self.id)]["data"]["movies"]
        ]
        return [
            {
                "video": [
                    {
                        "mime": "video/webm",
                        "sensitive": is_nsfw,
                        "uri": video_webm[i],
                    },
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

    def get_links(self):
        def remove_query_string(url: str):
            return parse_qs(urlparse(url).query)["u"][0] if "linkfilter" in url else url

        description_div = self._soup.body.find("div", class_="game_area_description")
        padding_div = self._soup.body.find("div", style="padding-top: 14px;")
        anchor_tags = padding_div.find_all("a")

        # 提取链接并移除查询字符串
        tooltips = [
            remove_query_string(a["data-tooltip-text"])
            for a in anchor_tags
            if "data-tooltip-text" in a.attrs
        ]

        website_url: str | None = self.json["data"]["website"]
        if website_url:
            website_url = website_url.replace(r"\/", "\\")

        links = [
            remove_query_string(a.attrs["href"])
            for a in description_div.select("a[href]")
        ]
        unique_links = list(
            set(links + tooltips + [website_url] if website_url else [])
        )

        processed_data = []
        for url in unique_links:
            for pattern in fgi_dict:
                if re.match(pattern["match"], url):
                    processed_data.append(
                        {
                            "name": pattern["prefix"],
                            "uri": re.sub(pattern["match"], pattern["replace"], url),
                        }
                    )
                    break
            else:
                processed_data.append({"name": ".website", "uri": url})

        processed_data.append({"name": ".steam", "uri": f"steam:{self.id}"})
        return processed_data

    def get_thumbnail(self):
        return self._remove_query(
            self._soup.body.find("img", {"class": "game_header_image_full"}).attrs[
                "src"
            ]
        )
