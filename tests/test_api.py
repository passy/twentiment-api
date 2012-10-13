"""
Test suite for the API module.

:author: 2012, Pascal Hartig <phartig@weluse.de>
"""

import json
import urllib
from unittest2 import TestCase, TestSuite
from twentiment_api.application import create_app


class ApiTestCase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.ctx = self.app.test_request_context()
        self.ctx.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.ctx.pop()


class LiveGuessApiTestCase(ApiTestCase):
    """Test case against the live API populated with samples/few_tweets.json"""

    def test_positive(self):
        response = self.client.get("/v1/guess?" + urllib.urlencode({
            'message': "I like my best friend."
        }))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(data['score'], 0.5)
        self.assertEqual(data['label'], 'positive')

    def test_negative(self):
        response = self.client.get("/v1/guess?" + urllib.urlencode({
            'message': "I hate my worst enemy."
        }))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(data['score'], -0.5)
        self.assertEqual(data['label'], 'negative')

    def test_neutral_gibberisch(self):
        response = self.client.get("/v1/guess?" + urllib.urlencode({
            'message': "Babbel quabbel wrabble."
        }))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(data['score'], 0.0)
        self.assertEqual(data['label'], 'neutral')

    def test_bad_request(self):
        response = self.client.get("/v1/guess?")
        self.assertEqual(400, response.status_code)


def load_tests(loader, standard_tests, pattern):
    """Loads the tests from this module"""

    suite = TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(LiveGuessApiTestCase))

    return suite
