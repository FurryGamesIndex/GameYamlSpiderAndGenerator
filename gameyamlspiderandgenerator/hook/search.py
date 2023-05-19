from re import sub
from urllib.parse import quote_plus

from loguru import logger

from ..hook import BaseHook
from ..util.config import config
from ..util.spider import get_json
from ..util.thread import ThreadWithReturnValue


# print(config, type(config))

class Search(BaseHook):
    CHANGED = ["tags", "links"]

    def __init__(self):
        self.pure = None
        self.encode = None

    @staticmethod
    def name_filter(string: str, pattern: str = r"[^A-z]", repl: str = ""):
        """
        
        Args:
            string: The string to be replaced
            pattern: Regular expression, replace non-English letters by default
            repl: The string to replace with

        Returns:

        """
        return sub(pattern, repl, string)
    def search_play(self) -> tuple:
        data = get_json(
            "https://serpapi.com/search?engine=google_play&apikey="
            f'{config["api"]["google-play"]}&store=apps&q={self.encode}'
        )
        if "organic_results" in data and any(
                [self.name_filter(i["title"]) == self.pure for i in data["organic_results"][0]["items"]]):
            logger.info("FOUND: google_play")
            return "google-play", {'name': '.play-store',
                                   'uri': f'google-play-store:{data["organic_results"][0]["items"][0]["product_id"]}'}
        return [], []

    def search_apple(self) -> tuple:
        data = get_json(
            "https://serpapi.com/search.json?engine=apple_app_store&term="
            f'{self.encode}&apikey={config["api"]["apple"]}'
        )
        if "organic_results" in data and any(
                [self.name_filter(i["title"]) == self.pure for i in data["organic_results"]]):
            logger.info("FOUND: apple_app_store")
            return "apple-appstore", {'name': '.apple-appstore', 'uri': data["organic_results"][0]["link"]}
        return [], []

    def search_all(self) -> list:
        func_list = [
            self.__getattribute__(i)
            for i in (list(filter(lambda x: "__" not in x, self.__dir__())))
        ]
        func_list = list(filter(
            lambda x: callable(x) and x.__name__.startswith("search") and x.__name__ != "search_all",
            func_list,
        ))

        fn_list = [ThreadWithReturnValue(target=i) for i in func_list]
        for i in fn_list:
            i.start()
        return [ii.join() for ii in fn_list]

    def search_epic(self):
        from epicstore_api import EpicGamesStoreAPI

        api = EpicGamesStoreAPI().fetch_store_games(keywords="TUNIC", sort_dir="DESC")
        game_list = api['data']['Catalog']['searchStore']['elements']
        reg = r"[^A-z\d]"
        if game_list and any(
                [self.name_filter(i["title"]) == self.pure for i in game_list]):
            logger.info("FOUND: epic")
            return "epic", {'name': '.epic',
                            'uri': f'https://store.epicgames.com/p/{self.name_filter(game_list[0]["title"], pattern=reg, repl="-")}'}
        return [], []

    def setup(self, data: dict):
        """
        hook handler
        Args:
            data: yaml daya

        Returns:
            The processed dict data

        """
        self.pure = self.name_filter(data['name'])
        self.encode = quote_plus(self.name_filter(data['name'], repl=" "))
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
