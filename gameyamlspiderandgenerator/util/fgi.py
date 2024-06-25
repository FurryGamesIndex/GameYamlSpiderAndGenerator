fgi_dict = [
    {
        "match": r"^https://www.youtube.com/(?!watch\?v=)(?!channel/)(@?.+)",
        "prefix": ".youtube",
        "replace": "youtube:@\\g<1>",
    },
    {
        "match": "^https://www.youtube.com/channel/(.+[^/])/",
        "prefix": ".youtube",
        "replace": "youtube:\\g<1>",
    },
    {
        "match": "^https://twitter.com/([A-Za-z0-9_]+).*",
        "prefix": ".twitter",
        "replace": "twitter:\\g<1>",
    },
    {
        "match": "^https://www.patreon.com/(.+)",
        "prefix": ".patreon",
        "replace": "patreon:\\g<1>",
    },
    {
        "match": "^https://discord.gg/(.+)",
        "prefix": ".discord",
        "replace": "discord:\\g<1>",
    },
    {
        "match": "^https://www.facebook.com/(.+)/",
        "prefix": ".facebook",
        "replace": "facebook:\\g<1>",
    },
    {
        "match": "^https://www.furaffinity.net/user/(.+)/",
        "prefix": ".furaffinity",
        "replace": "furaffinity:\\g<1>",
    },
    {
        "match": "(https://weibo.com/u/.+)",
        "prefix": ".weibo",
        "replace": "\\g<1>",
    },
]
default_config = {
    "hook_configs": {
        "search": {
            "apple": "a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90",
            "google-play": "a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90",
        }
    },
    "git_proxy": None,
    "api": {},
    "hook": ["search", "validate"],
    "plugin": ["steam", "itchio"],
    "proxy": {},
}
template_dict = {
    "name": "NAME",
    "brief-description": "BRIEF-DESC",
    "description": "DESC",
    "description-format": "markdown",
    "authors": [],
    "tags": {
        "type": [],
        "lang": [],
        "platform": [],
        "publish": [],
        "misc": [],
    },
    "links": [],
    "thumbnail": "THUMBNAIL.PNG",
    "screenshots": [],
}
