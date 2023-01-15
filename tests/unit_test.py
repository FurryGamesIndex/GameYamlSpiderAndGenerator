import os
import sys
import unittest

from gameyamlspiderandgenerator.util.spider import get_status, get_text


def update_config():
    from gameyamlspiderandgenerator.util.setting import config, set_config

    config(
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
    set_config("hook", ["search"])
    set_config("plugin", ["steam", "itchio"])


class CliUnitTest(unittest.TestCase):
    """Rewritten from test_cli.py"""

    def test_cli(self):
        status_code = os.system(
            f"{sys.executable} -m gameyamlspiderandgenerator.cli url"
        )
        status_code = os.waitstatus_to_exitcode(status_code)
        self.assertEqual(status_code, 0)


class InitUnitTest(unittest.TestCase):
    """Rewritten from test_init.py"""

    def test_init(self):
        from gameyamlspiderandgenerator.plugin.steam import Search as Steam

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
        update_config()
        self.assertGreaterEqual(get_status("https://store.steampowered.com/"), 0)
        self.assertIsInstance(get_text("https://www.so.com/"), str)


if __name__ == "__main__":
    unittest.main()
