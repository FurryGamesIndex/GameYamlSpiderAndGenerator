## How to write

- `poetry new <hook_name>`
- Create a new \_\_init\_\_.py file

```python
from gameyamlspiderandgenerator.hook import BaseHook
class YourHookName(BaseHook):
    CHANGED : list | None = None # Which key names in the dictionary did you change
    def setup(self, data: dict):
        pass  # Your main Hook program
```

## Install

```shell
pip install yamlgenerator-hook-<hook_name>
```
