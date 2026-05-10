import re

from loguru import logger

from ._base import BasePlugin, YamlData
from ..util.spider import get_json

import jsonpath

class Gcores(BasePlugin):
    _VERIFY_PATTERN = re.compile(r"https://www\.gcores\.com/games/(\d+)/?")

    def __init__(self, link: str):
        m = re.search(self._VERIFY_PATTERN, link)
        if not m:
            raise ValueError(f"Invalid Gcores link: {link}")

        self.id = m.group(1)
        self.json = get_json(
            f"https://www.gcores.com/gapi/v1/games/{self.id}?include="
            "tags%2Cuser%2Cgame-stores%2Cgame-links%2Cinvolvements.entity.user%2Cactive-entry-vote-activities%2Cactive-entry-vote-activities.vote-activity-options%2Cactive-entry-vote-activity-records%2Cactive-entry-vote-activity-records.vote-activity-option&fields[users]=nickname%2Cthumb&fields[involvements]=position%2Ctitle%2Crank%2Centity&fields[celebrities]=user&fields[organizations]=name&fields[tags]=name%2Ctag-type&meta[tags]=%2C&meta[users]=%2C&meta[celebrities]=%2C&meta[organizations]=%2C"
        )
        self.tags = self.get_tags()
        self.link = link
        logger.warning(self.tags)

    def parser(self, expr: str, data: dict | str | None = None, method: str = "first"):
        """
        method:
            - "first": return first matched value or None
            - "all": return all matched values
        """
        try:
            result = jsonpath.findall(expr, self.json if data is None else data)
            if method == "all":
                return result
            return result[0] if result else None
        except Exception as e:
            logger.warning(f"Parse /{expr}/ failed!({e!r})")
            logger.debug(self.json if data is None else data)
            return [] if method == "all" else None

    def get_name(self) -> str:
        return self.parser("$.data.attributes.title")

    def get_desc(self) -> str:
        return self.parser("$.data.attributes.description")

    def get_brief_desc(self) -> str:
        return self.parser("$.data.attributes.introduction")

    def get_thumbnail(self) -> str:
        return "https://image.gcores.com/" + self.parser("$.data.attributes.cover")

    def get_authors(self) -> list[dict]:
        _position_dict = {
            "策划": "producer",
            "文案": "screenwriter",
            "美术": "artist",
            "动画": "animation",
            "制作": "producer",
            "开发": "producer",
            "音乐": "musician",
            "音效": "musician",
            "场景": "scenographer",
            "配音": "voice-actor",
            "程序": "programmer",
            "编程": "programmer",
        }

        def parse_role(role: str | list):
            _ret = set()
            if isinstance(role, list):
                _ret = {
                    _position_dict[key]
                    for single_role in role
                    for key in _position_dict
                    if key in single_role
                }
            else:
                _ret = {_position_dict[key] for key in _position_dict if key in role}

            if isinstance(role, str) and not _ret:
                logger.warning(f"Can't find {role}")
                return ["producer"]
            elif isinstance(role, list) and len(role) != len(_ret):
                logger.warning(f"Can't find {role}")
                return ["producer"]
            else:
                return list(_ret)

        # jq:
        # .included | map(select(.type == "users") | [ .attributes.nickname, .id ])
        # jsonpath:
        # 先取出 users，再用 Python 组装成 [nickname, id]
        users = self.parser('$.included[?@.type == "users"]', method="all") or []
        author_id: list[list[str]] = [
            [u["attributes"]["nickname"], u["id"]]
            for u in users
        ]

        position = []
        for _name, _uid in author_id:
            user_json = get_json(
                f"https://www.gcores.com/gapi/v1/users/{_uid}?include=entities.involvements.entry",
            )

            position_id = self.parser(
                f'$.included[?@.relationships.entry.data.id == "{self.id}"].id',
                user_json,
                "all",
            ) or []

            if len(position_id) > 1:
                _tmp = [
                    self.parser(
                        f'$.included[?@.id == "{pid}"].attributes.title',
                        user_json,
                    )
                    for pid in position_id
                ]
                position.append(_tmp)
            elif position_id:
                position.append(
                    self.parser(
                        f'$.included[?@.id == "{position_id[0]}"].attributes.title',
                        user_json,
                    )
                )
            else:
                position.append("制作")

        for count in range(len(position)):
            author_id[count][1] = position[count]

        ret = []
        for name, role in author_id:
            ret.append({"name": name, "role": parse_role(role)})

        ret.append(
            {
                "name": self.parser('$.data.attributes["booom-group-title"]'),
                "role": ["producer"],
            }
        )
        return ret

    def get_tags(self) -> list[str]:
        return self.parser('$.included[?@.type == "tags"].attributes.name', method="all") or []

    def get_misc_tags(self) -> list[dict]:
        return []

    def get_platforms(self) -> list[str]:
        repl = {
            "Windows": "windows",
        }
        return [repl[i.strip()] for i in self.tags if i in repl.keys()]

    def get_langs(self) -> list[str]:
        return ["zh"]

    def get_links(self) -> list[dict]:
        downlink = self.parser('$.data.attributes["download-link"]')
        if downlink:
            return [
                {"name": ".demo-version", "uri": downlink},
                {"name": ".website", "uri": self.link},
            ]
        return []

    def get_screenshots(self) -> list[str]:
        link: list[str] = self.parser("$.data.attributes.screenshots") or []
        return ["https://image.gcores.com/" + _ for _ in link]

    def to_yaml(self) -> YamlData:
        ret = {
            "name": self.get_name(),
            "brief-description": self.get_brief_desc(),
            "description": self.get_desc(),
            "description-format": "markdown",
            "authors": self.get_authors(),
            "tags": {
                "type": self.get_type_tags(),
                "lang": self.get_langs(),
                "platform": self.get_platforms(),
                "publish": ["website"],
                "misc": self.get_misc_tags(),
            },
            "links": self.get_links(),
            "thumbnail": self.get_thumbnail(),
            "screenshots": self.get_screenshots(),
        }
        return YamlData(self._load_hook(ret))

    def get_type_tags(self) -> list[dict]:
        return []