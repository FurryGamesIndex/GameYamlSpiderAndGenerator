from bs4 import BeautifulSoup
import requests
import re
import langcodes
import html2text
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString as pss
import sys


def ScParser(videomp4: list, videowebm: list, sc: list, IsNSFW: bool):
    ret = []
    for i in range(len(videomp4)):
        ret.append({
            "type": "video",
            "src": [
                {"mime": "video/webm", 'sensitive': IsNSFW, "uri": videowebm[i]},
                {"mime": "video/mp4", 'sensitive': IsNSFW,"uri": videomp4[i]},
            ]
        })
    for i in range(len(sc)):
        ret.append(sc[i])
    return ret

yaml = YAML()

r = requests.get(sys.argv[1])
demo = r.text
soup = BeautifulSoup(demo, "html.parser")

bDesc = soup.find("meta", {"name": "Description"})["content"]

b1 = soup.body.find("div", attrs={"class": "blockbg"})
Name = b1.find("span", {"itemprop": "name"}).text

b2 = soup.body.find("div", attrs={"style": "padding-top: 14px;"})
b2b = b2.find_all("a")
Linkz = [
    b2b[i].attrs["data-tooltip-text"]
    for i in range(len(b2b))
    if "data-tooltip-text" in b2b[i].attrs
]

b3 = soup.body.find("table", attrs={"class": "game_language_options"}).find_all(
    "td", {"style": "width: 94px; text-align: left"}
)
Langs = list(set(
    [
        langcodes.find(re.sub(r"[\n\t]*", "", b3[i].text)).language
        for i in range(len(b3))
    ]
))

b4 = soup.body.find_all("a", attrs={"class": "highlight_screenshot_link"})
Sc = [b4[i].attrs["href"].split("?", 1)[0] for i in range(len(b4))]

Desc =  pss(html2text.html2text(
    str(soup.body.find("div", attrs={"class": "game_area_description"}))
))

b5 = soup.body.find_all("div", {"class": "highlight_player_item highlight_movie"})
Video_mp4 = [b5[i].attrs["data-mp4-source"].split("?", 1)[0] for i in range(len(b5))]
Video_webm = [b5[i].attrs["data-webm-source"].split("?", 1)[0] for i in range(len(b5))]

IsNSFW = soup.body.find_all("div", {"id": "game_area_content_descriptors"}) != []

b6 = soup.body.find_all("a", {"class": "app_tag"})
Tags = [re.sub(r"[\n\t\r]*", "", b6[i].text) for i in range(len(b6))]

b7 = soup.body.find_all("div", {"class": "dev_row"})
if b7[0].a.text != b7[1].a.text:
    Author = [b7[0].a.text,b7[1].a.text]
else:
    Author = [b7[0].a.text]

Thumbnail = (
    soup.body.find("img", {"class": "game_header_image_full"})
    .attrs["src"]
    .split("?", 1)[0]
)
yaml.default_flow_style=False
yaml.sort_keys=False
print(
    yaml.dump(
    {
            "name": Name,
            "brief-description":bDesc ,
            "description": Desc,
            "authors": [
            {
                "name": Author,
                "role": [
                    "producer",
                    "publisher"
                ]
            }],
            "tags":
            {   "tag": Tags,
                "lang": Langs,
                "publish": [
                ],
                "platform": [
                ],
                "sys": [
                ]
            },
            "links": Linkz,
            "thumbnail": Thumbnail,
            "screenshots": ScParser(Video_mp4,Video_webm,Sc,IsNSFW)
        }
    , sys.stdout)
)
