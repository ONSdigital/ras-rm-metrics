import json
import unittest

from metrics.app import app


class TestApp(unittest.TestCase):
    def test_info_endpoint(self):
        client = app.test_client()

        response = client.get('/info')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertEqual(json.loads(response.data), {"name": "ras-rm-metrics",
                                                     "status": "OK"})
