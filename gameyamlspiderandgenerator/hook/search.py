if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from re import sub
from typing import AnyStr
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from loguru import logger

from gameyamlspiderandgenerator.util.setting import setting
from gameyamlspiderandgenerator.util.spider import get_json, get_text


class Search:
    @staticmethod
    def name_filter(s: AnyStr, rep: AnyStr = ""):
        return sub("[^A-z]", rep, s.lower())

    def __init__(self, name: str) -> None:
        logger.info(f"init {name}")
        self.pure = self.name_filter(name)
        self.encode = quote_plus(self.name_filter(name, " "))

    def search_steam(self):
        data = get_json(
            f"https://store.steampowered.com/api/storesearch/"
            f"?term={self.encode}&l=english&cc=US"
        )["items"]
        return any(self.name_filter(i["name"]) == self.pure for i in data)

    def search_epic(self):
        data = get_text(f"https://en.softonic.com/s/{self.encode}")
        soup = BeautifulSoup(data, "html.parser")
        bf = soup.body.find_all("a", {"class": "track-search-results"})
        return any(
            self.name_filter(bf[i].div["data-meta-data"]) == self.pure
            for i in range(len(bf))
        )

    def search_play(self):
        data = get_json(
            "https://serpapi.com/search?engine=google_play&apikey="
            f'{setting["api"]["google-play"]}&store=apps&q={self.encode}'
        )
        return any(
            self.name_filter(i["title"]) == self.pure
            for i in data["organic_results"][0]["items"]
        )

    def search_apple(self):
        data = get_json(
            "https://serpapi.com/search.json?engine=apple_app_store&term="
            f'{self.encode}&apikey={setting["api"]["apple"]}'
        )
        return any(
            self.name_filter(i["title"]) == self.pure for i in data["organic_results"]
        )

    def search_all(self):
        func_list = [
            self.__getattribute__(i)
            for i in (list(filter(lambda x: "__" not in x, self.__dir__())))
        ]
        func_list = filter(
            lambda x: callable(x)
            and x.__name__.startswith("search")
            and x.__name__ != "search_all",
            func_list,
        )
        for ii in func_list:
            print(ii.__name__, ii())

    def setup(self, data: dict):
        pass


if __name__ == "__main__":
    Search("dead-space").search_all()
