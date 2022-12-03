if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
from util.spider import get_json
from util.spider import get_text
from urllib.parse import quote_plus
from re import sub, match
from typing import AnyStr, Dict, List
from bs4 import BeautifulSoup
from json import loads
from html2text import html2text
from langcodes import find


class Search:
    def __init__(self, link: AnyStr) -> None:
        self.data_html = get_text(link)
        self.soup = BeautifulSoup(self.data_html, "html.parser")
        self.data = [ii for ii in [loads(i.text) for i in self.soup.find_all(
            'script', attrs={'type': "application/ld+json"})] if 'name' in ii][0]

    def get_thumbnail(self):
        return self.soup.select_one('#header > img').attrs['src']

    def get_brief_desc(self):
        return self.data['aggregateRating']['description'] if 'description' in self.data['aggregateRating'] else None

    def get_name(self):
        return self.data['name']

    def get_screenshots(self):
        return [i.attrs['src'] for i in self.soup.find_all('img', attrs={'class': "screenshot"})]

    def get_desc(self):
        return html2text(str(self.soup.select_one('div.formatted_description.user_formatted')), bodywidth=0).strip()

    def get_platforms(self):
        repl = {'Windows': 'windows', 'macOS': 'macos',
                'Linux': 'linux', 'Android': 'android'}
        return [repl[i.strip()] for i in self.soup.select_one('div.info_panel_wrapper > div > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.split(',')]

    def get_authors(self) -> List[dict]:
        temp = self.soup.select_one(
            'div.info_panel_wrapper > div > table > tbody > tr:nth-child(6) > td:nth-child(2)').text.split(',')
        author = [{'name': i, 'role': 'developer'}
                  for i in temp]
        return author

    def get_tag(self) -> List[str]:
        temp = self.soup.select_one(
            'div.info_panel_wrapper > div > table > tbody > tr:nth-child(7) > td:nth-child(2)').text.split(',')
        temp1 = self.soup.select_one(
            'div.info_panel_wrapper > div > table > tbody > tr:nth-child(9) > td:nth-child(2)').text.split(',')
        temp2 = [i.strip() for i in (temp1+temp)]
        return temp2

    def get_lang(self) -> List[str]:
        temp = self.soup.select_one(
            'div.info_panel_wrapper > div > table > tbody > tr:nth-child(11) > td:nth-child(2)').text.split(',')
        return list(set([find(i).language for i in temp]))

    def get_link(self) -> List[dict]:
        link = [i.attrs['href'] for i in self.soup.select('a[href]')]
        fgi_dict = [
            {'match': '^https://www\.youtube\.com/@?([^/]+)/?',
             'prefix': '.youtube', 'replace': "youtube:@\\g<1>"},
            {'match': '^https://www\.youtube\.com/channel/(.+[^/])',
             'prefix': '.youtube', 'replace': "youtube:\\g<1>"},
            {'match': '^https://twitter\.com/(.{1,})',
             'prefix': '.twitter', 'replace': "twitter:\\g<1>"},
            {'match': '^https://www\.patreon\.com/(.+)',
             'prefix': '.patreon', 'replace': "patreon:\\g<1>"},
            {'match': '^https://discord\.gg/(.+)', 'prefix': '.discord',
             'replace': "discord:\\g<1>"},
            {'match': 'https://www\.facebook\.com/(.+)/', 'prefix': '.facebook',
             'replace': "facebook:\\g<1>"}
        ]
        data = [i for i in list(set(link))]
        processed_data = list()
        for i in data:
            for p in fgi_dict:
                if match(p['match'], i) != None:
                    processed_data.append(
                        {'name': p['prefix'], 'uri':  sub(p['match'], p['replace'], i)})
        return processed_data


if __name__ == '__main__':
    obj = Search(link='https://horrorbuns.itch.io/clawstar-wrestling')
    print(obj.get_thumbnail())
    print(obj.get_desc())
    print(obj.get_name())
    print(obj.get_screenshots())
    print(obj.get_desc())
    print(obj.get_platforms())
    print(obj.get_authors())
    print(obj.get_tag())
    print(obj.get_lang())
    print(obj.get_link())
