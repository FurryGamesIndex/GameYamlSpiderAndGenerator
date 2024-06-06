import subprocess
import sys
import unittest
from pathlib import Path

from gameyamlspiderandgenerator.util.config import config

config.load(Path(__file__).parent / "test_config.yaml")
print(config)
print("*" * 10)


class CliUnitTest(unittest.TestCase):
    """Rewritten from test_cli.py"""

    def test_cli_missing_url(self):
        result = subprocess.run([sys.executable, "-m", "gameyamlspiderandgenerator"])
        self.assertGreaterEqual(result.returncode, 1)

    def test_steam(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "gameyamlspiderandgenerator",
                "https://store.steampowered.com/app/1470120/Atopes/",
            ]
        )
        self.assertEqual(result.returncode, 0)

    def test_itchio(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "gameyamlspiderandgenerator",
                "https://fymm-game.itch.io/ddp",
            ]
        )
        self.assertEqual(result.returncode, 0)


class SpiderUnitTest(unittest.TestCase):
    """Rewritten from test_spider.py"""

    def test_spider(self):
        from gameyamlspiderandgenerator.util.spider import get_bytes, get_text

        self.assertIsInstance(get_bytes("https://example.com/"), bytes)
        self.assertIsInstance(get_text("https://example.com/"), str)


if __name__ == "__main__":
    unittest.main()
