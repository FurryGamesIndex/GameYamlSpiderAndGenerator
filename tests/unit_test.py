import logging
import subprocess
import sys
import unittest

from gameyamlspiderandgenerator.hook.search import Search


def update_config():
    from gameyamlspiderandgenerator.util.config import config

    config.update(
        {
            "proxy": {
                "http": "http://127.0.0.1:10809",
                "https": "http://127.0.0.1:10809",
            },
            "api": {
                "google-play": "a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90",
                "apple": "a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90",
            },
        }
    )
    config.set("hook", ["search"])
    config.set("plugin", ["steam", "itchio"])


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
            ]
        )
        self.assertEqual(result.returncode, 0)


class InitUnitTest(unittest.TestCase):
    """Rewritten from test_init.py"""

    def test_init(self):
        from gameyamlspiderandgenerator.plugin.steam import Steam as Steam

        update_config()
        self.assertIsInstance(
            Steam(
                "https://store.steampowered.com/app/381210/Dead_by_Daylight/"
            ).to_yaml(),
            str,
        )


class SpiderUnitTest(unittest.TestCase):
    """Rewritten from test_spider.py"""

    def test_spider(self):
        from gameyamlspiderandgenerator.util.spider import get_status, get_text

        update_config()
        self.assertGreaterEqual(get_status("https://store.steampowered.com/"), 0)
        self.assertIsInstance(get_text("https://www.so.com/"), str)


class ConfigUnitTest(unittest.TestCase):
    def test_update(self):
        from gameyamlspiderandgenerator.util.config import config

        update_config()
        self.assertEqual(
            config.proxy,
            {
                "http": "http://127.0.0.1:10809",
                "https": "http://127.0.0.1:10809",
            },
        )

    def test_flush(self):
        from gameyamlspiderandgenerator.util.config import config

        update_config()
        config.flush()
        self.assertFalse(bool(config.__dict__))

    def test_set(self):
        from gameyamlspiderandgenerator.util.config import config

        update_config()
        config.set("foo", ["bar"])
        self.assertEqual(
            getattr(config, "foo"),
            ["bar"],
        )
        update_config()


class SteamUnitTest(unittest.TestCase):
    """Rewritten from plugin/steam.py"""

    def test_steam(self):
        from gameyamlspiderandgenerator.plugin.steam import Steam as Steam

        update_config()
        steam = Steam("https://store.steampowered.com/app/381210/Dead_by_Daylight/")
        self.assertIsInstance(
            steam.to_yaml(),
            str,
        )


class ItchIOUnitTest(unittest.TestCase):
    def test_itchio(self):
        from gameyamlspiderandgenerator.plugin.itchio import ItchIO

        update_config()
        obj = ItchIO(link="https://fymm-game.itch.io/ddp")
        with self.assertLogs("itchio") as _:
            self._extract_log(obj)

    @staticmethod
    def _extract_log(obj):
        logging.getLogger("itchio").info(f"{obj.get_thumbnail() = }")
        logging.getLogger("itchio").info(f"{obj.get_desc() = }")
        logging.getLogger("itchio").info(f"{obj.get_name() = }")
        logging.getLogger("itchio").info(f"{obj.get_screenshots() = }")
        logging.getLogger("itchio").info(f"{obj.get_brief_desc() = }")
        logging.getLogger("itchio").info(f"{obj.get_platforms() = }")
        logging.getLogger("itchio").info(f"{obj.get_authors() = }")
        logging.getLogger("itchio").info(f"{obj.get_langs() = }")
        logging.getLogger("itchio").info(f"{obj.get_links() = }")
        logging.getLogger("itchio").info(f"{obj.get_misc_tags() = }")


class SearchUnitTest(unittest.TestCase):
    def test_search(self):
        self.assertIsInstance(Search("dead-space").search_all(), list)


if __name__ == "__main__":
    unittest.main()
