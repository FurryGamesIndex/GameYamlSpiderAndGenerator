if __name__=='__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from util.spider import get_json
from util.spider import get_text
from util.spider import get_status
from loguru import logger
from typing import Dict, AnyStr, SupportsInt, NoReturn

class search:
    @staticmethod
    def is_id_exist(url: AnyStr,id: SupportsInt):
        return get_status(url)==200 and get_json(url)[str(id)]['success']
    def make_yaml(self,id: SupportsInt)->Dict | SupportsInt:
        self.data=get_json(f'https://store.steampowered.com/api/appdetails?appids={id}&cc=us&l=english')
        self.data_html=get_text(f'https://store.steampowered.com/app/{id}/')
        if type(self.data)==int:
            return self.data
    #def get_
        

