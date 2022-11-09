import re
import requests
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
proxies = {"http": "http://127.0.0.1:7890", "https": "socks5://127.0.0.1:7891"}


class SearchGame:
    def __init__(self, name: str) -> None:
        self.pure = re.sub('[^A-z]', ' ', name)
        self.encode = quote(re.sub('[^A-z]', ' ', name))
    def search_steam(self):
        url = f'https://store.steampowered.com/api/storesearch/?term={self.encode}&l=english&cc=US'
        response = requests.get(url, proxies=proxies)
        data = json.loads(response.text)['items']
        if not data:
            return None
        for i in data:
            i.pop('type')
            i.pop('price', 'Error')
            i.pop('tiny_image')
            i.pop('streamingvideo')
            i.pop('controller_support', 'Error')
            i.pop('metascore', 'Error')
        return data
    def search_epic(self):
        r = requests.get(f'https://en.softonic.com/s/{self.encode}',
                         timeout=20, proxies=proxies)
        demo = r.text
        soup = BeautifulSoup(demo, "html.parser")
        bf = soup.body.find_all("a", {"class": "track-search-results"})
        ret = []
        for i in range(len(bf)):
            ret.append(
                {'name': bf[i].div['data-meta-data'], 'website': bf[i].a['href']})
        return (ret)

if __name__ == '__main__':
    s = SearchGame('流浪 / Stray')


