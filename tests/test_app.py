import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as app_module  # noqa: E402


class PaletteCardTest(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    def test_healthz(self):
        res = self.client.get("/healthz")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ok")

    def test_index_ok(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("きょうの配色カード", res.get_data(as_text=True))

    def test_all_combinations_have_palette(self):
        for s in app_module.SEASONS:
            for m in app_module.MOODS:
                p = app_module.get_palette(s, m)
                self.assertIsNotNone(p, (s, m))
                self.assertEqual(len(p["colors"]), 3)
                for hexcode in p["colors"]:
                    self.assertTrue(hexcode.startswith("#"))
                    self.assertEqual(len(hexcode), 7)

    def test_result_shows_palette(self):
        res = self.client.get("/?season=春&mood=元気")
        body = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("桜はじける", body)
        self.assertIn("#F783AC", body)
        self.assertIn("#FFD43B", body)
        self.assertIn("#8CE99A", body)

    def test_invalid_combo_no_result(self):
        res = self.client.get("/?season=梅雨&mood=元気")
        body = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("桜はじける", body)


if __name__ == "__main__":
    unittest.main()
