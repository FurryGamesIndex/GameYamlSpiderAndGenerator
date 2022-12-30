setting = dict()


def config(data: dict):
    global setting
    setting = data


def get_config():
    return setting


def set_config(name: str, data: dict):
    setting[name] = data
