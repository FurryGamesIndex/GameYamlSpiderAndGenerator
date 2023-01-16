fgi_dict = [
    {
        "match": "^https://www.youtube.com/@?([^/]+)/?",
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
        "match": "https://www.facebook.com/(.+)/",
        "prefix": ".facebook",
        "replace": "facebook:\\g<1>",
    },
]
