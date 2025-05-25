fgi_dict = [
    {
        "match": "^https://www\.youtube\.com/(?!watch\?v=)(?!channel/)(@?[^/]+)/?$",
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
        "match": "^https://x.com/([A-Za-z0-9_]+).*",
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
            "apple": None,
            "google-play": None,
        }
    },
    "git_proxy": None,
    "hook": ["search", "validate"],
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
