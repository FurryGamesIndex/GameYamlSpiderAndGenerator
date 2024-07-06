import unittest
from pathlib import Path


from gameyamlspiderandgenerator.util.fgi import template_dict
from gameyamlspiderandgenerator.util.plugin_manager import pkg

from gameyamlspiderandgenerator.util.config import config

config.load(Path(__file__).parent / "test_config.yaml")
pkg.init()


class HookUnitTest(unittest.TestCase):
    def test_all(self):
        test_config = {
            "search": {"name": "dead-space"},
            "validate": {},
        }
        for i in config.hook:
            print(template_dict | test_config[i])
            self.assertIsInstance(
                pkg.hook[f"yamlgenerator_hook_{i}"]().setup(
                    template_dict | test_config[i]
                ),
                dict,
            )
