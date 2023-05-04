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
```
Example:
- python3.11 -m gameyamlspiderandgenerator **url**
- python3.11 -m gameyamlspiderandgenerator **url** -o zip
- python3.11 -m gameyamlspiderandgenerator **url** -o /home/user/desktop/output.yaml

## hook
### hook.search.Search(BaseHook)
Hook plugin for processing data

You cannot directly use
### hook.validate.Verify(BaseHook)
Hook plugin to verify whether the format of the data file is correct

You cannot directly use

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
