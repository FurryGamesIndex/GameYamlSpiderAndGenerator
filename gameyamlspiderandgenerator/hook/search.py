from re import sub
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from loguru import logger

from ..hook import BaseHook
from ..util.config import config
from ..util.spider import get_json, get_text

print(config, type(config))


class Search(BaseHook):
    @staticmethod
    def name_filter(s: str, rep: str = ""):
        return sub("[^A-z]", rep, s.lower())

    def __init__(self, name: str) -> None:
        logger.info(f"Hook: init {name}")
        self.pure = self.name_filter(name)
        self.encode = quote_plus(self.name_filter(name, " "))

    def search_play(self):
        data = get_json(
            "https://serpapi.com/search?engine=google_play&apikey="
            f'{config["api"]["google-play"]}&store=apps&q={self.encode}'
        )
        if "organic_results" in data and any(
                [self.name_filter(i["title"]) == self.pure for i in data["organic_results"][0]["items"]]):
            logger.info("FOUND: google_play")
            return "google-play", {'name': '.play-store',
                                   'uri': f'google-play-store:{data["organic_results"][0]["items"][0]["product_id"]}'}
        return [[], []]

    def search_apple(self):
        data = get_json(
            "https://serpapi.com/search.json?engine=apple_app_store&term="
            f'{self.encode}&apikey={config["api"]["apple"]}'
        )
        if "organic_results" in data and any(
                [self.name_filter(i["title"]) == self.pure for i in data["organic_results"]]):
            logger.info("FOUND: apple_app_store")
            return "apple-appstore", {'name': '.apple-appstore', 'uri': data["organic_results"][0]["link"]}
        return [[], []]

    def search_all(self) -> list:
        func_list = [
            self.__getattribute__(i)
            for i in (list(filter(lambda x: "__" not in x, self.__dir__())))
        ]
        func_list = filter(
            lambda x: callable(x) and x.__name__.startswith("search") and x.__name__ != "search_all",
            func_list,
        )
        return [ii() for ii in func_list]

    def setup(self, data: dict):
        temp = data.copy()
        try:
            result = self.search_all()
            publish = [i[0] for i in result] + temp["tags"]['publish']
            link = [i[1] for i in result] + temp["links"]

            def rm_empty(s: list):
                if [] in s:
                    s.remove([])
                    rm_empty(s)

            rm_empty(publish)
            rm_empty(link)
            temp["tags"]['publish'] = list(publish)
            temp["links"] = link
        except:
            return data
        return temp
