if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
from util.spider import get_json
from util.spider import get_text
from util.yaml_parse import read_config
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn, List
from bs4 import BeautifulSoup
from langcodes import find
from urllib.parse import urlparse,parse_qs
from html2text import html2text
from ruamel.yaml.scalarstring import PreservedScalarString as PS
from textwrap import dedent
import re
def LS(x: AnyStr): return PS(dedent(x))
'''
^https://www\.youtube\.com/(@[A-z]{3,})
^https://www\.youtube\.com/channel/(.{3,})

^https://twitter\.com/(.{1,})
'''

class search:

    def __init__(self, link: AnyStr) -> None:
        self.id = self.get_steam_id(link)
        self.data = get_json(
            f'https://store.steampowered.com/api/appdetails?appids={self.id}&cc=us&l=english')
        self.data_html = get_text(link)
        self.soup = BeautifulSoup(self.data_html, "html.parser")
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

    def get_tag(self) -> List[str]:
        repl = {
            "Adventure": "adventure",
            "Action": "action",
            "Visual Novel": "visual-novel",
            "Strategy": "strategy",
            "RTS": "real-time-strategy",
            'Casual': 'casual',
            'Management': 'business-sim',
            'Card Game': 'board',
            'Fighting': 'fighting',
            'Music': 'music',
            'Shooter': 'shooter',
            'Puzzle': 'puzzle',
            'RPG': 'role-playing',
            'MMORPG': 'mmorpg',
            'Dating Sim': 'dating-sim',
            'Roguel': 'roguelike',
            'Sports': 'sports'
        }
        temp1 = self.soup.body.find_all("a", {"class": "app_tag"})
        temp = [re.sub(r"[\n\t\r]*", "", temp1[i].text)
                for i in range(len(temp1))]
        ret = []
        for i in repl:
            for ii in temp:
                if i in ii:
                    ret.append(repl[i])
        return list(set(ret))

    def get_if_nsfw(self):
        return self.soup.body.find_all("div", {"id": "game_area_content_descriptors"}) != []

    def get_screenshots(self):
        return [self.remove_query(i['path_full']) for i in self.data[str(self.id)]['data']['screenshots']]

    def get_video(self):
        return [[self.remove_query(i['webm']['max']), self.remove_query(i['mp4']['max'])] for i in self.data[str(self.id)]['data']['movies']]

    def get_link(self) -> List[dict]:
        def remove_query_string(x: AnyStr):
            if 'linkfilter' in x:
                return parse_qs(urlparse(x).query)['url'][0]
            else:
                return x
        temp1 = self.soup.body.find("div", attrs={
            'id': 'game_area_description', "class": "game_area_description"})
        temp3=self.soup.body.find("div", attrs={"style": "padding-top: 14px;"})
        temp2=temp3.find_all('a')
        temp4=[remove_query_string(i["data-tooltip-text"]) for i in temp2 if "data-tooltip-text" in i.attrs]
        temp = temp1.select("a[href]")
        ret = []
        for i in temp:
            ret.append(remove_query_string(i.attrs['href']))
        return list(set(ret+temp4))

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
    obj = search('https://store.steampowered.com/app/1313140/_/')
    print(obj.get_lang())
    print(obj.get_brief_desc())
    print(obj.get_desc())
    print(obj.get_authors())
    print(obj.get_platforms())
    print(obj.get_tag())
    print(obj.get_if_nsfw())
    print(obj.get_screenshots())
    print(obj.get_video())
    print(obj.get_link())
    print(obj.name)
