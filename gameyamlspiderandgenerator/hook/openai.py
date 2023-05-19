from random import choice
import openai as openai
from langcodes import Language

from ..hook import BaseHook
from ..util.config import config


class OpenAI(BaseHook):
    CHANGED = ["brief-description"]

    def setup(self, data: dict):
        if not data["brief-description"]:
            temp = data.copy()
            chat_dict = [{"role": "user", "content": data[
                                                         "description"] + f"输出游戏文本相应语言的40字游戏简介（用{Language.get(config['lang']).display_name('zh')}回答！）"}]
            openai.api_key = config["api"]["openai"]
            openai.proxy = config["proxy"]
            rzt = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_dict)
            temp["brief-description"] = choice(rzt["choices"])["message"]["content"] + "\n\nby openai"
            return temp
        return data
