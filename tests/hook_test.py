import sys
import unittest
from importlib.metadata import version
from pathlib import Path

from loguru import logger

from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.fgi import template_dict
from gameyamlspiderandgenerator.util.plugin_manager import pkg

config.load(Path(__file__).parent / "test_config.yaml")
pkg.init()

logger.remove()
logger.add(sys.stdout, level="DEBUG")


class HookUnitTest(unittest.TestCase):
    def test_all(self):
        test_config = {
            "search": {"name": "dead-space"},
            "validate": {},
        }
        print(config.hook)
        for i in config.hook:
            print(template_dict | test_config[i])
            print("version: " + version(f"yamlgenerator_hook_{i}"))
            self.assertIsInstance(
                pkg.hook[f"yamlgenerator_hook_{i}"]().setup(
                    template_dict | test_config[i]
                ),
                dict,
            )
