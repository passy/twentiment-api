"""
ZMQ client

:author: 2012, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

import zmq


class ClientError(Exception):
    def __init__(self, result):
        if result.count(" "):
            self.code, self.message = result.split(" ", 1)
        else:
            self.code = result


class Client(object):
    """ZeroMQ client for twentiment."""

    def __init__(self, host, port):
        context = zmq.Context()

        self.socket = context.socket(zmq.REQ)
        self.socket.connect('tcp://{}:{}'.format(host, port))

    @classmethod
    def from_config(cls):
        from flask import current_app

        config = current_app.config
        return cls(config['TWENTIMENT_HOST'], config['TWENTIMENT_PORT'])

    def guess(self, message):
        self.socket.send_unicode("GUESS {}".format(message))
        return self._handle_guess_result(self.socket.recv_string())

    def _handle_guess_result(self, result):
        if result.startswith("OK "):
            return float(result.split(" ", 1)[1])
        else:
            return ClientError(result)
