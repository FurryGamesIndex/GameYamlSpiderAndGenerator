## gameyamlspiderandgenerator
- *python3.11 -m gameyamlspiderandgenerator -h*
```text
usage: __main__.py [-h] [-f CONFIG] [-o OUTPUT] URL

positional arguments:
  URL

options:
  -h, --help            show this help message and exit
  -f CONFIG, --config CONFIG
                        The location of config.yaml (default null)
  -o OUTPUT, --output OUTPUT
                        The location of the output file (zip format or yaml format)
  --fast                Whether to disable all hooks (default: false)

```
Example:
- python3.11 -m gameyamlspiderandgenerator **url**
- python3.11 -m gameyamlspiderandgenerator **url** -o zip
- python3.11 -m gameyamlspiderandgenerator **url** -o /home/user/desktop/output.yaml

## hook
### hook.search.Search(BaseHook)
Hook plugin for processing data
- Example：
```python
from gameyamlspiderandgenerator.hook.search import Search
from gameyamlspiderandgenerator.util.fgi import template_dict
assert type(Search().setup({**template_dict, 'name':'dead-space'})) is dict
```
### hook.openai.OpenAI(BaseHook)
Hook plugin that uses openai to write a brief introduction to the data file for the introduction

**You need to fill in the config.yaml with your secret**
- Example：
```python
from gameyamlspiderandgenerator.hook.openai import OpenAI
from gameyamlspiderandgenerator.util.fgi import template_dict
assert type(OpenAI().setup({**template_dict,"description": "YOUR DESC"})) is dict

```
### hook.validate.Verify(BaseHook)
Hook plugin to verify whether the format of the data file is correct
- Example：
```python
from gameyamlspiderandgenerator.hook.validate import Verify
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
