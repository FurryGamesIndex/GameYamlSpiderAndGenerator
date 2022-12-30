from gameyamlspiderandgenerator.util.setting import config

config({"proxy": {"http": 'http://127.0.0.1:7890', "https": 'socks5://127.0.0.1:7891'},
        "api": {'google-play': 'a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90',
                'apple': 'a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90'}
        })
from gameyamlspiderandgenerator.plugin.steam import Search as Steam
from gameyamlspiderandgenerator.plugin.itchio import Search as Itch
import sys

sys.path.append("../gameyamlspiderandgenerator")
sys.path.append("../gameyamlspiderandgenerator/util")

print(Steam('https://store.steampowered.com/app/381210/Dead_by_Daylight/').make_yaml())
