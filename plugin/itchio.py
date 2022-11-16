if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
from util.spider import get_json
from util.spider import get_text
from urllib.parse import quote_plus
from re import sub
from typing import AnyStr
from bs4 import BeautifulSoup