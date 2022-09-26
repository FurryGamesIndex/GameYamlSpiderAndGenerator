from bs4 import BeautifulSoup
import requests
import re
import langcodes
import html2text
import ruamel
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString
import textwrap
import sys


def IsSteam(url: str):
    r = requests.get(url, timeout=20)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    bf = soup.body.find("div", {"class": "edit-comment-hide"}).find_all("a")
    for i in range(len(bf)):
        if bf[i].text.find("store.steampowered.com/app") != -1:
            return bf[i].text
    return None


def ScParser(videomp4: list, videowebm: list, sc: list, IsNSFW: bool):
    ret = []
    for i in range(len(videomp4)):
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
    for i in range(len(sc)):
        ret.append(sc[i])
    return ret


def LinkParser(lks: list, steamCode: str):
    print(lks)
    ret = []
    ret.append({
               "name": ".steam",
               "uri": "steam:"+steamCode
               })
    for i in range(len(lks)):
        if lks[i].find("twitter") != -1:
            ret.append({
                "name": ".twitter",
                "uri": "twitter:"+lks[i][lks[i].rfind('/')+1:]
            })
        elif lks[i].find("youtube") != -1:
            ret.append({
                "name": ".youtube",
                "uri": lks[i]
            })
        else:
            ret.append(lks[i])
    return ret


def GetSteamData(url: str):
    from ruamel.yaml import YAML
    yaml = YAML(typ=['rt', 'string'])
    yaml.indent(sequence=4, offset=2)
    yaml.width = 4096
    def LS(x): return PreservedScalarString(
        textwrap.dedent(x))  # avoid soft line

    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    bDesc = LS(soup.find("meta", {"name": "Description"})["content"])

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
    Langs = list(
        set(
            [
                langcodes.find(re.sub(r"[\n\t]*", "", b3[i].text)).language
                for i in range(len(b3))
            ]
        )
    )

    b4 = soup.body.find_all("a", attrs={"class": "highlight_screenshot_link"})
    Sc = [b4[i].attrs["href"].split("?", 1)[0] for i in range(len(b4))]

    Desc = LS(html2text.html2text(
        str(soup.body.find("div", attrs={
            'id': 'game_area_description', "class": "game_area_description"})), bodywidth=0))  # avoid soft line

    b5 = soup.body.find_all(
        "div", {"class": "highlight_player_item highlight_movie"})
    Video_mp4 = [
        b5[i].attrs["data-mp4-source"].split("?", 1)[0] for i in range(len(b5))
    ]
    Video_webm = [
        b5[i].attrs["data-webm-source"].split("?", 1)[0] for i in range(len(b5))
    ]

    IsNSFW = soup.body.find_all(
        "div", {"id": "game_area_content_descriptors"}) != []

    b6 = soup.body.find_all("a", {"class": "app_tag"})
    Tags = [re.sub(r"[\n\t\r]*", "", b6[i].text) for i in range(len(b6))]

    b7 = soup.body.find_all("div", {"class": "dev_row"})
    if b7[0].a.text != b7[1].a.text:
        Author = [{"name": b7[1].a.text, "role": ["publisher"]}]
        Author.append({"name": b7[0].a.text, "role": ["producer"]})
    else:
        Author = [{"name": b7[0].a.text, "role": ["publisher", "producer"]}]
    Thumbnail = (
        soup.body.find("img", {"class": "game_header_image_full"})
        .attrs["src"]
        .split("?", 1)[0]
    )
    parsedTag = TagParser(Tags)
    parsedTag['lang'] = Langs
    ret = {
        "name": Name,
        "brief-description": bDesc,
        "description": Desc,
        "description-format": 'markdown',
        "authors": Author,
        "tags": parsedTag,
        "links": LinkParser(Linkz, url.split('/')[4]),
        "thumbnail": "thumbnail"+Thumbnail[Thumbnail.rfind('.'):],
        "screenshots": ScParser(Video_mp4, Video_webm, Sc, IsNSFW),
    }
    import imghandle
    imghandle.ParserImg(Thumbnail, ret['thumbnail'])
    bRet = yaml.dump_to_string(ret)
    # add top-level key line
    for key in ['\ndescription: |', 'brief-description: |-']+[i+':' for i in list(ret.keys())[3:]]:
        bRet = bRet.replace(key, '\n'+key)
    return (bRet.replace("![]","![img]"), ret['thumbnail'])


def TagParser(tag: list):
    db = {
        "type": [
            ["Adventure", "adventure"],
            ["Action", "action"],
            ["Visual Novel", "visual-novel"],
            ["Strategy", "strategy"],
            ["RTS", "real-time-strategy"],
            ['Casual', 'casual'],
            ['Management', 'business-sim'],
            ['Card Game', 'board'],
            ['Fighting', 'fighting'],
            ['Music', 'music'],
            ['Shooter', 'shooter'],
            ['Puzzle', 'puzzle'],
            ['RPG', 'role-playing'],
            ['MMORPG', 'mmorpg'],
            ['Dating Sim', 'dating-sim'],
            ['Roguel', 'roguelike'],
            ['Sports', 'sports']
        ]
    }
    ret = {
        "type": [],
        "species": [],
        "fetish": [],
        "misc": [],
        "lang": [],
        "publish": [],
        "platform": [],
    }
    for i in range(len(tag)):
        for ii in range(len(db['type'])):
            if tag[i].find(db['type'][ii][0]) != -1:
                ret['type'].append(db['type'][ii][1])
    ret['type'] = list(set(ret['type']))
    return ret


if __name__ == '__main__':
    print(GetSteamData(sys.argv[1])[0])
