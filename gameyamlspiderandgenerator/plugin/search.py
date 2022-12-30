if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
from gameyamlspiderandgenerator.util.spider import get_json
from gameyamlspiderandgenerator.util.spider import get_text
from urllib.parse import quote_plus
from re import sub
from typing import AnyStr
from bs4 import BeautifulSoup
from gameyamlspiderandgenerator.util.setting import setting
from loguru import logger


class Search:
    @staticmethod
    def name_filter(s: AnyStr, rep: AnyStr = ''):
        return sub('[^A-z]', rep, s.lower())

    def __init__(self, name: str) -> None:
        logger.info(f'init {name}')
        self.pure = self.name_filter(name)
        self.encode = quote_plus(self.name_filter(name, ' '))

    def search_steam(self):
        data = get_json(
            f'https://store.steampowered.com/api/storesearch/?term={self.encode}&l=english&cc=US')['items']
        for i in data:
            if self.name_filter(i['name']) == self.pure:
                return True
        return False

    def search_epic(self):
        data = get_text(f'https://en.softonic.com/s/{self.encode}')
        soup = BeautifulSoup(data, "html.parser")
        bf = soup.body.find_all("a", {"class": "track-search-results"})
        for i in range(len(bf)):
            if self.name_filter(bf[i].div['data-meta-data']) == self.pure:
                return True
        return False

    def search_play(self):
        data = get_json(
            f'https://serpapi.com/search?engine=google_play&apikey={setting["api"]["google-play"]}&store=apps&q={self.encode}')
        for i in data["organic_results"][0]["items"]:
            if self.name_filter(i['title']) == self.pure:
                return True
        return False

    def search_apple(self):
        data = get_json(
            f'https://serpapi.com/search.json?engine=apple_app_store&term={self.encode}&apikey={setting["api"]["apple"]}')
        for i in data["organic_results"]:
            if self.name_filter(i['title']) == self.pure:
                return True
        return False

    def search_all(self):
        func_list = [self.__getattribute__(i) for i in (
            list(filter(lambda x:'__' not in x, self.__dir__())))]
        func_list = filter(lambda x: callable(x) and x.__name__.startswith(
            'search') and x.__name__ != 'search_all', func_list)
        for ii in func_list:
            print(ii.__name__, ii())


if __name__ == '__main__':
    s = Search('dead-space').search_all()
