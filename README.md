![](https://github.com/FurryGamesIndex/GameYamlSpiderAndGenerator/actions/workflows/Test%20Default%20Hooks.yml/badge.svg)
![](https://github.com/FurryGamesIndex/GameYamlSpiderAndGenerator/actions/workflows/Test%20Main%20Program.yml/badge.svg)
<details>
  <summary><h2>🕯️ In memory of nullqwertyuiop</h2></summary>
We are deeply saddened by the loss of our dear friend, [nullqwertyuiop](https://github.com/nullqwertyuiop), who passed away on December 30, 2024. His kindness, generosity, and contributions to this project will never be forgotten. His commitment to excellence and selflessness made a lasting impact, and we are forever grateful for his support and friendship.
Rest in peace, nullqwertyuiop.
</details>

# Quick Start

## Install

```sh
pip install gameyamlspiderandgenerator
pip install yamlgenerator-hook-openai # install extra hook
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
hook_configs:
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

```python3
from gameyamlspiderandgenerator import produce_yaml
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.plugin_manager import pkg

config.load("/home/user/desktop/config.yaml")
pkg.init()
print(produce_yaml("https://store.steampowered.com/app/1470120/Atopes/"))
```

### More: see [API Reference](https://github.com/FurryGamesIndex/GameYamlSpiderAndGenerator/wiki/Api-Reference)
