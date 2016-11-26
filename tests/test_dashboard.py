# -*- coding: utf-8 -*-
import json
import unittest

from wt import dashboard
from wt.scripts import create_bot


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.app = dashboard.create_app(config_name="testing")
        self.client = self.app.test_client()

    def test_entry(self):
        expected = {
            "test": "success"
        }

        rv = self.client.get('/test')
        self.assertEqual(json.loads(rv.data), expected)

    def test_main_view(self):
        rv = self.client.get('/')
        self.assertTrue(b'Main page' in rv.data)

    def test_help_view(self):
        rv = self.client.get('/help')
        self.assertTrue(b'Help' in rv.data)


if __name__ == '__main__':
    unittest.main()
