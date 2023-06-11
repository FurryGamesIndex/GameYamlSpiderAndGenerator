import os
import subprocess
import sys
import unittest

from gameyamlspiderandgenerator.hook.search import Search
from gameyamlspiderandgenerator.hook.validate import Verify
from gameyamlspiderandgenerator.util.config import config
from gameyamlspiderandgenerator.util.fgi import template_dict

config.load(os.path.split(os.path.realpath(__file__))[0] + "/test_config.yaml")
print(config)


class CliUnitTest(unittest.TestCase):
    """Rewritten from test_cli.py"""

    def test_cli_missing_url(self):
        result = subprocess.run([sys.executable, "-m", "gameyamlspiderandgenerator"])
        self.assertGreaterEqual(result.returncode, 1)

    def test_cli(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "gameyamlspiderandgenerator",
                "https://store.steampowered.com/app/1470120/Atopes/",
                "--fast"
            ]
        )
        self.assertEqual(result.returncode, 0)


class SpiderUnitTest(unittest.TestCase):
    """Rewritten from test_spider.py"""

    def test_spider(self):
        from gameyamlspiderandgenerator.util.spider import get_status, get_text
        self.assertGreaterEqual(get_status("https://store.steampowered.com/"), 200)
        self.assertIsInstance(get_text("https://www.so.com/"), str)


class SteamUnitTest(unittest.TestCase):
    """Rewritten from plugin/steam.py"""

    def test_steam(self):
        from gameyamlspiderandgenerator.plugin.steam import Steam
        steam = Steam("https://store.steampowered.com/app/381210/Dead_by_Daylight/")
        self.assertIsInstance(
            str(steam.to_yaml()),
            str,
        )


class ItchIOUnitTest(unittest.TestCase):
    def test_itchio(self):
        from gameyamlspiderandgenerator.plugin.itchio import ItchIO
        obj = ItchIO(link="https://fymm-game.itch.io/ddp")
        self.assertIsInstance(
            str(obj.to_yaml()),
            str,
        )


class HookUnitTest(unittest.TestCase):
    def test_search(self):
        self.assertIsInstance(Search().setup({**template_dict, 'name': 'dead-space'}), dict)

    def test_verify(self):
        self.assertIsInstance(Verify().setup(template_dict), dict)


if __name__ == "__main__":
    unittest.main()
