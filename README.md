![](https://github.com/FurryGamesIndex/GameYamlSpiderAndGenerator/actions/workflows/Test%20Default%20Hooks.yml/badge.svg)
![](https://github.com/FurryGamesIndex/GameYamlSpiderAndGenerator/actions/workflows/Test%20Main%20Program.yml/badge.svg)

# Quick Start

## Install

```commandline
pip install gameyamlspiderandgenerator
# install extra hook
# pip install yamlgenerator-hook-openai
python3
```

## Create a new configuration file

- config.yaml

```yaml
hook:
  - search
  - validate
proxy: { }
# if you don't want to set proxy, please fill in {}
# http: socks5://127.0.0.1:7891
# https: socks5://127.0.0.1:7891
git_proxy: null
hook_config:
  search:
    google-play: a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90
    apple: a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90

```

## Try to make yaml data file

```bash
 python -m gameyamlspiderandgenerator -f /home/user/desktop/config.yaml  https://store.steampowered.com/app/290340/Armello/ -o 1.zip
 # or omit some options
 python -m gameyamlspiderandgenerator https://store.steampowered.com/app/290340/Armello/

```

*or use the library in your script*

```python
from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg

config.load("/home/user/desktop/config.yaml")
pkg.init()
print(produce_yaml("https://store.steampowered.com/app/1470120/Atopes/"))
```

### More: see [API Reference](https://github.com/FurryGamesIndex/GameYamlSpiderAndGenerator/wiki/Api-Reference)
