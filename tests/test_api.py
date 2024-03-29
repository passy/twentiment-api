"""
Test suite for the API module.

:author: 2012, Pascal Hartig <phartig@weluse.de>
"""

import json
import urllib
import mock
import contextlib
from unittest2 import TestCase, TestSuite
from twentiment_api.application import create_app


class ApiTestCase(TestCase):
    config = {
        'TWENTIMENT_HOST': "localhost",
        'TWENTIMENT_PORT': 10001
    }

    def setUp(self):
        self.app = create_app(self.config)
        self.app.testing = True
        self.ctx = self.app.test_request_context()
        self.ctx.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.ctx.pop()


class ClientTestCase(TestCase):
    @contextlib.contextmanager
    def _mock_socket(self):
        with mock.patch('twentiment_api.client.zmq', spec=True) as zmq:
            yield zmq.Context.return_value.socket.return_value

    def test_send(self):
        from twentiment_api.client import Client

        with self._mock_socket() as socket:
            client = Client("localhost", 10001)
            client.guess("Hello, World!")

            socket.send_unicode.assert_called_once_with("GUESS Hello, World!")

    def test_okay(self):
        from twentiment_api.client import Client

        with self._mock_socket() as socket:
            socket.recv_string.return_value = "OK 0.5"

            client = Client("localhost", 10001)
            response = client.guess("Hello, World!")

            self.assertEquals(response, 0.5)

    def test_error(self):
        from twentiment_api.client import Client, ClientError

        with self._mock_socket() as socket:
            socket.recv_string.return_value = "ERROR UNKNOWN_COMMAND"

            client = Client("localhost", 10001)
            call = lambda: client.guess("Hello, World!")
            self.assertRaises(ClientError, call)

    def test_unicode(self):
        """Smoke regression test for unicode messages"""
        from twentiment_api.client import Client

        with self._mock_socket():
            client = Client("localhost", 10001)
            # This used to blow the formatting up.
            client.guess(u'@laliminati LAL\u0130 2500 OMAMA YARDIM ET X')


class LiveGuessApiTestCase(ApiTestCase):
    """Test case against the live API populated with samples/few_tweets.json"""

    def _send_message(self, message):
        response = self.client.get("/v1/guess?" + urllib.urlencode({
            'message': message
        }))
        self.assertEqual(200, response.status_code)
        return json.loads(response.data)

    def test_positive(self):
        data = self._send_message("I like my best friend.")
        self.assertEqual(data['score'], 0.5)
        self.assertEqual(data['label'], 'positive')

    def test_negative(self):
        data = self._send_message("I hate my worst enemy.")
        self.assertEqual(data['score'], -0.5)
        self.assertEqual(data['label'], 'negative')

    def test_neutral_gibberisch(self):
        data = self._send_message("Babbel quabbel wrabble.")
        self.assertEqual(data['score'], 0.0)
        self.assertEqual(data['label'], 'neutral')

    def test_bad_request(self):
        response = self.client.get("/v1/guess?")
        self.assertEqual(400, response.status_code)


class CORSTestCase(ApiTestCase):
    """Tests for some CORS stuff."""

    def setUp(self):
        config = self.config.copy()
        self.config = config

        config['CORS_ENABLED'] = True
        config['CORS_ORIGIN'] = "localhost"

        ApiTestCase.setUp(self)

    def test_preflight(self):
        response = self.client.open("/something", method='OPTIONS', headers={
            'origin': "localhost"
        })
        self.assertEqual(response.status_code, 200)

    def test_nopreflight(self):
        response = self.client.open("/something", method='OPTIONS')
        self.assertEqual(response.status_code, 404)

    def test_headers(self):
        with mock.patch('twentiment_api.api.Client', spec=True) as Client:
            Client.from_config.return_value.guess.return_value = 0.5

            response = self.client.get("/v1/guess?message=Hello", headers={
                'origin': "localhost"
            })
            self.assertEqual(response.headers['Access-Control-Allow-Origin'],
                            "localhost")


def load_tests(loader, standard_tests, pattern):
    """Loads the tests from this module"""

    suite = TestSuite()
    # Only enable if you have a local server running.
    # TODO: Consider automatic skipping if zmq fails to connect
    # suite.addTest(loader.loadTestsFromTestCase(LiveGuessApiTestCase))
    suite.addTest(loader.loadTestsFromTestCase(ClientTestCase))
    suite.addTest(loader.loadTestsFromTestCase(CORSTestCase))

    return suite
