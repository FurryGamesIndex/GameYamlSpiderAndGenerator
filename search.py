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
        self.cmp = re.sub('\s','',re.match('[\s]*[A-z]*', self.pure).group().lower())

    def SearchSteam(self) -> list | None:
        url = f'https://store.steampowered.com/api/storesearch/?term={self.encode}&l=english&cc=US'
        response = requests.get(url, proxies=proxies)
        data = json.loads(response.text)['items']
        if data == []:
            return None
        for i in data:
            i.pop('type')
            i.pop('price', 'Error')
            i.pop('tiny_image')
            i.pop('streamingvideo')
            i.pop('controller_support', 'Error')
            i.pop('metascore', 'Error')
        data
        return data

    def SearchEpic(self):
        r = requests.get('https://en.softonic.com/s/stray',
                         timeout=20, proxies=proxies)
        demo = r.text
        soup = BeautifulSoup(demo, "html.parser")
        bf = soup.body.find_all("a", {"class": "track-search-results"})
        ret = []
        for i in range(len(bf)):
            ret.append(
                {'name': bf[i].div['data-meta-data'], 'website': bf[i].a['href']})
        print(json.dumps(ret))
        print(self.cmpName(ret[0]['name']))

    def cmpName(self, n: str) -> bool:
        print(self.cmpablize(n))
        print(self.cmp)
        if self.cmp == self.cmpablize(n):
            return True
        return False
    def cmpablize(self,n) -> str:
        '''
        make comparable
        '''
        return re.sub('\s','',re.match('[\s]*[A-z]*', n).group().lower())



if __name__ == '__main__':
    s = SearchGame('流浪 / Stray')
    print(s.SearchSteam())
    s.SearchEpic()
