import openai
from loguru import logger
from json import loads
from random import choice
from ..hook import BaseHook
from ..util.config import config


class OpenAI(BaseHook):
    CHANGED = None

    def setup(self, data: dict):
        chat_dict = [{"role": "user", "content": data["description"] + f"visual-novel strategy real-time-strategy "
                                                                       f"casual business-sim adventure board action "
                                                                       f"fantasy fighting music shooter puzzle "
                                                                       f"role-playing mmorpg dating-sim roguelike "
                                                                       f"sports non-indie bara yuri yiff gore comedy "
                                                                       f"tragedy horror "
                                                                       f"根据以上游戏介绍只用以上所给出的英文标签给这个游戏打上最有可能的标签，输出为json，不需要带键名\n如果实在没有相匹配的标签输出空列表[]"}]
        openai.api_key = config["api"]["openai"]
        openai.proxy = config["proxy"]
        rzt = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_dict)
        logger.info("tags that may exist: " + ', '.join(loads(choice(rzt["choices"])["message"]["content"])))
        return data
