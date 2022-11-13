if __name__=='__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from util.yaml_parse import read_config
setting=read_config('config.yaml')