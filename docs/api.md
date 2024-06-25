## gameyamlspiderandgenerator

- *python -m gameyamlspiderandgenerator -h*

```text
usage: __main__.py [-h] [--silent | --debug] [-f CONFIG] [--proxy PROXY] [-o OUTPUT] [--lang LANG] [--fast] URL

positional arguments:
  URL

options:
  -h, --help            show this help message and exit
  --silent              Enable silent log mode
  --debug               Enable debug log mode
  -f CONFIG, --config CONFIG
                        The location of config.yaml (default null)
  --proxy PROXY
  -o OUTPUT, --output OUTPUT
                        The location of the output file (zip format or yaml format)
  --lang LANG           The display language of the game. ISO 639-1 code(default: en)
  --fast                Whether to disable all hooks (default: false)
```

Example:

- python -m gameyamlspiderandgenerator **url**
- python -m gameyamlspiderandgenerator **url** -o zip
- python -m gameyamlspiderandgenerator **url** -o /home/user/desktop/output.yaml

## hook

### hook.search.Search(BaseHook)

Hook plugin for processing data

- Example：

```python
from yamlgenerator_hook_search import Search
from gameyamlspiderandgenerator.util.fgi import template_dict
assert type(Search().setup({**template_dict, 'name':'dead-space'})) is dict
```

### hook.openai.OpenAI(BaseHook)

Hook plugin that uses openai to write a brief introduction to the data file for the introduction

**You need to fill in the config.yaml with your secret**

- Example：

```python
from yamlgenerator_hook_openai import OpenAI
from gameyamlspiderandgenerator.util.fgi import template_dict
assert type(OpenAI().setup({**template_dict,"description": "YOUR DESC"})) is dict

```

### hook.validate.Verify(BaseHook)

Hook plugin to verify whether the format of the data file is correct

- Example：

```python
from yamlgenerator_hook_validate import Verify
from gameyamlspiderandgenerator.util.fgi import template_dict
assert type(Verify().setup(template_dict)) is dict
```

## plugin

### plugin.itchio.ItchIO(BasePlugin)

Script to generate YAML for itchio url

- Example：

```python
from gameyamlspiderandgenerator.plugin.itchio import ItchIO

print(ItchIO("https://mangledmaw.itch.io/amanda-the-adventurer").to_yaml())
```

### plugin.steam.Steam(BasePlugin)

Script to generate YAML for steam url

- Example：

```python
from gameyamlspiderandgenerator.plugin.steam import Steam

print(Steam("https://store.steampowered.com/app/290340/Armello/").to_yaml())
```
