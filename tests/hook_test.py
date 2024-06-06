import unittest
from pathlib import Path

from yamlgenerator_hook_search import Search
from yamlgenerator_hook_validate import Verify

from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.fgi import template_dict
from gameyamlspiderandgenerator.util.plugin_manager import pkg

config.load(Path(__file__).parent / "test_config.yaml")
pkg.init()


class HookUnitTest(unittest.TestCase):
    def test_search(self):
        self.assertIsInstance(
            Search().setup({**template_dict, "name": "dead-space"}), dict
        )

    def test_verify(self):
        self.assertIsInstance(Verify().setup(template_dict), dict)
