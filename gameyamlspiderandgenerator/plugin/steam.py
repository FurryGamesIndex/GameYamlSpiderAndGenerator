if __name__ == '__main__':
    import sys
    import os

    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
from gameyamlspiderandgenerator.util.spider import get_json, get_text
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn, List, Set, Any
from bs4 import BeautifulSoup
from langcodes import find
from urllib.parse import urlparse, parse_qs
from html2text import html2text
from ruamel.yaml.scalarstring import PreservedScalarString as PS
from ruamel.yaml import YAML
from textwrap import dedent
import re


def ls(x: AnyStr): return PS(dedent(x))


yaml = YAML(typ=['rt', 'string'])
yaml.indent(sequence=4, offset=2)
yaml.width = 4096


class Search:
    @staticmethod
    def get_steam_id(link: AnyStr) -> SupportsInt:
        return int(urlparse(link).path.split('/')[2])

    def get_steam_name(self):
        name = self.data[str(self.id)]["data"]["name"]
        return name

    @staticmethod
    def remove_query(s: str):
        s = re.sub(r"\?t=\d{6,12}", "", s)
        return s.replace('![]', '![img]')

    def __init__(self, link: AnyStr) -> None:
        self.id = self.get_steam_id(link)
        self.data = get_json(
            f'https://store.steampowered.com/api/appdetails?appids={self.id}&cc=us&l=english')
        self.data_html = get_text(link)
        self.soup = BeautifulSoup(self.data_html, "html.parser")
        self.name = self.get_steam_name()
        temp1 = self.soup.body.find_all("a", {"class": "app_tag"})
        self.tag = [re.sub(r"[\n\t\r]*", "", temp1[i].text)
                    for i in range(len(temp1))]

    def make_yaml(self) -> AnyStr | SupportsInt:
        if type(self.data) == int:
            return self.data
        ret = {
            "name": self.get_steam_name(),
            "brief-description": self.get_desc(),
            "description": self.get_brief_desc(),
            "description-format": 'markdown',
            "authors": self.get_authors(),
            "tags": {'type': self.get_type_tag(), 'lang': self.get_lang(), 'platform': self.get_platforms(),
                     'misc': self.get_misc_tag()},
            "links": self.get_link(),
            "thumbnail": 'thumbnail.png',
            "screenshots": self.get_screenshots() + self.get_video(),
        }
        bRet = yaml.dump_to_string(ret)
        for i in list(ret.keys())[1:]:
            bRet = bRet.replace('\n' + i, '\n\n' + i)
        return bRet

    def get_lang(self) -> List[str]:
        temp = self.data[str(
            self.id)]['data']['supported_languages'].split(',')
        return list(set([find(i).language for i in temp]))

    def get_desc(self):
        return ls(self.remove_query((html2text(self.data[str(self.id)]['data']['detailed_description'], bodywidth=0))))

    def get_brief_desc(self):
        return ls(html2text(self.data[str(self.id)]['data']['short_description'], bodywidth=0))

    def get_authors(self) -> List[dict]:
        temp = self.data[str(self.id)]['data']
        developers = [{'name': i, 'role': 'developer'}
                      for i in temp['developers']]
        publishers = [{'name': i, 'role': 'publisher'}
                      for i in temp['publishers']]
        return developers + publishers

    def get_platforms(self):
        temp = self.data[str(self.id)]['data']['platforms']
        repl = {'windows': 'windows', 'mac': 'macos', 'linux': 'linux'}
        return [repl[i] for i in temp if i]

    def get_type_tag(self):
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
            'Sports': 'sports',
            'Comedy': 'comedy',
            'Horror': 'horror'
        }

        ret = []
        for i in repl:
            for ii in self.tag:
                if i in ii:
                    ret.append(repl[i])
        return list(set(ret))

    def get_misc_tag(self):
        repl = {'3D': '3d',
                'Pixel': 'pixel-art',
                'Multiplayer': 'multiplayer',
                'PvP': 'pvp',
                'Sexual': 'uncensored',
                'Nudity': 'uncensored',
                'Free to Play': 'freeware',
                'Story Rich': 'multiple-endings',
                'JRPG': 'multiple-endings',
                'Co-Op': 'co-op',
                'Online': 'online'
                }
        ret = []
        for i in repl:
            for ii in self.tag:
                if i in ii:
                    ret.append(repl[i])
        return list(set(ret))

    def get_if_nsfw(self):
        return self.soup.body.find_all("div", {"id": "game_area_content_descriptors"}) != []

    def get_screenshots(self):
        return [self.remove_query(i['path_full']) for i in self.data[str(self.id)]['data']['screenshots']]

    def get_video(self):
        ret = list()
        IsNSFW = self.get_if_nsfw()
        videowebm = [self.remove_query(i['webm']['max'])
                     for i in self.data[str(self.id)]['data']['movies']]
        videomp4 = [self.remove_query(i['mp4']['max'])
                    for i in self.data[str(self.id)]['data']['movies']]
        for i in range(len(videowebm)):
            ret.append(
                {
                    "type": "video",
                    "src": [
                        {"mime": "video/webm", "sensitive": IsNSFW,
                         "uri": videowebm[i]},
                        {"mime": "video/mp4", "sensitive": IsNSFW,
                         "uri": videomp4[i]},
                    ] if IsNSFW else [
                        {"mime": "video/webm",
                         "uri": videowebm[i]},
                        {"mime": "video/mp4",
                         "uri": videomp4[i]},
                    ]
                }
            )
        return ret

    def get_link(self) -> List[dict]:
        def remove_query_string(x: AnyStr):
            if 'linkfilter' in x:
                return parse_qs(urlparse(x).query)['url'][0]
            else:
                return x

        temp1 = self.soup.body.find("div", attrs={
            'id': 'game_area_description', "class": "game_area_description"})
        temp3 = self.soup.body.find(
            "div", attrs={"style": "padding-top: 14px;"})
        temp2 = temp3.find_all('a')
        temp4 = [remove_query_string(i["data-tooltip-text"])
                 for i in temp2 if "data-tooltip-text" in i.attrs]
        temp = temp1.select("a[href]")
        ret = []
        for i in temp:
            ret.append(remove_query_string(i.attrs['href']))
        fgi_dict = [
            {'match': '^https://www.youtube.com/@?([^/]+)/?',
             'prefix': '.youtube', 'replace': "youtube:@\\g<1>"},
            {'match': '^https://www.youtube.com/channel/(.+[^/])',
             'prefix': '.youtube', 'replace': "youtube:\\g<1>"},
            {'match': '^https://twitter.com/(.{1,})',
             'prefix': '.twitter', 'replace': "twitter:\\g<1>"},
            {'match': '^https://www.patreon.com/(.+)',
             'prefix': '.patreon', 'replace': "patreon:\\g<1>"},
            {'match': '^https://discord.gg/(.+)', 'prefix': '.discord',
             'replace': "discord:\\g<1>"},
            {'match': 'https://www.facebook.com/(.+)/', 'prefix': '.facebook',
             'replace': "facebook:\\g<1>"}
        ]
        data = [{'url': i, 'processed': False} for i in list(set(ret + temp4))]
        processed_data = list()
        for i in data:
            for p in fgi_dict:
                if re.match(p['match'], i['url']) is not None:
                    processed_data.append(
                        {'name': p['prefix'], 'uri': re.sub(p['match'], p['replace'], i['url'])})
                    i['processed'] = True
        for i in data:
            if not i['processed']:
                processed_data.append({'name': '.website', 'uri': i['url']})
        return processed_data

    def get_thumbnail(self):
        return self.remove_query(self.soup.body.find("img", {"class": "game_header_image_full"}).attrs["src"])


if __name__ == '__main__':
    obj = Search('https://store.steampowered.com/app/381210/Dead_by_Daylight/')
    print(obj.make_yaml())
