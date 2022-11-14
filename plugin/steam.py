if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
from util.spider import get_json
from util.spider import get_text
from util.spider import get_status
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn, List
from bs4 import BeautifulSoup
from langcodes import find
from urllib.parse import urlparse
from html2text import html2text
from ruamel.yaml.scalarstring import PreservedScalarString as PS
from textwrap import dedent
import re
def LS(x: AnyStr): return PS(dedent(x))


class search:
    def __init__(self, link: AnyStr) -> None:
        self.data = get_json(
            f'https://store.steampowered.com/api/appdetails?appids={self.get_steam_id(link)}&cc=us&l=english')
        self.data_html = get_text(link)
        self.soup = BeautifulSoup(self.data_html, "html.parser")
        self.id = self.get_steam_id(link)
        self.name = self.get_steam_name(link)

    def make_yaml(self, id: SupportsInt) -> Dict | SupportsInt:
        if type(self.data) == int:
            return self.data

    def get_lang(self) -> List[str]:
        temp = self.data[str(
            self.id)]['data']['supported_languages'].split(',')
        return [find(i).language for i in temp]

    def get_desc(self):
        return LS(self.remove_query((html2text(self.data[str(self.id)]['data']['detailed_description'], bodywidth=0))))

    def get_brief_desc(self):
        return LS(html2text(self.data[str(self.id)]['data']['short_description'], bodywidth=0))

    def get_authors(self) -> List[dict]:
        temp = self.data[str(self.id)]['data']
        developers = [{'name': i, 'role': 'developer'}
                      for i in temp['developers']]
        publishers = [{'name': i, 'role': 'publisher'}
                      for i in temp['publishers']]
        return developers+publishers

    def get_platforms(self):
        temp = self.data[str(self.id)]['data']['platforms']
        repl = {'windows': 'windows', 'mac': 'macos', 'linux': 'linux'}
        return [repl[i] for i in temp if i]

    @staticmethod
    def get_steam_id(link: AnyStr) -> SupportsInt:
        return int(urlparse(link).path.split('/')[2])

    @staticmethod
    def get_steam_name(link: AnyStr) -> SupportsInt:
        name = urlparse(link).path.split('/')[3]
        return name if name != '_' else '[NAME NEED TRANSLATE]'

    @staticmethod
    def remove_query(s: str):
        s = re.sub(r"\?t=\d{6,12}", "", s)
        return s.replace('![]', '![img]')


if __name__ == '__main__':
    obj = search('https://store.steampowered.com/app/848450/_/')
    print(obj.get_lang())
    print(obj.get_brief_desc())
    print(obj.get_desc())
    print(obj.get_authors())
    print(obj.get_platforms())
    print(obj.name)
