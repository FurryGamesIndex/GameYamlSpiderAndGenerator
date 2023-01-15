class Setting:
    def __getitem__(self, item):
        # Compatibility with the old version
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        # Compatibility with the old version
        self.__setattr__(key, value)

    def set(self, name: str, data: dict | list[str]):
        self.__setattr__(name, data)

    def update(self, data: dict):
        self.__dict__.update(data)

    def flush(self):
        self.__dict__.clear()


setting = Setting()


# TODO Deprecate these below, implement into Setting class
def config(data: dict):
    setting.__dict__.update(data)


def get_config():
    return setting.__dict__


def set_config(name: str, data: dict | list[str]):
    setting.__dict__[name] = data


config(
    {
        "proxy": {
            "http": "http://127.0.0.1:10809",
            "https": "http://127.0.0.1:10809",
        },
        "api": {
            "google-play": "a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90",
            "apple": "a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90",
        },
    }
)
set_config("hook", ["search"])
set_config("plugin", ["steam", "itchio"])
