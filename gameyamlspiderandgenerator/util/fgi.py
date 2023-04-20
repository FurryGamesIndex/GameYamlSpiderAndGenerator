fgi_dict = [
    {
        "match": "^https://www.youtube.com/(?!watch\?v=)(@?.+)",
        "prefix": ".youtube",
        "replace": "youtube:@\\g<1>",
    },
    {
        "match": "^https://www.youtube.com/channel/(.+[^/])",
        "prefix": ".youtube",
        "replace": "youtube:\\g<1>",
    },
    {
        "match": "^https://twitter.com/(.{1,})",
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
default_config = {'api': {'apple': 'a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90',
                          'google-play': 'a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90'},
                  'gitToken': 'your token',
                  'hook': ['search'],
                  'plugin': ['steam', 'itchio'],
                  'proxy': {}}
