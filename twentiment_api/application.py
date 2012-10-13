"""
Twentiment API Flask application.

:author: 2012, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

from __future__ import absolute_import

from flask import Flask, jsonify


class JSONFlask(Flask):
    """Creates a JSON repsonse if the returned object contains a ``to_json``
    method.
    """

    def make_response(self, rv):
        if hasattr(rv, 'to_json'):
            return jsonify(rv.to_json())

        if isinstance(rv, tuple):
            if len(rv) == 2 and hasattr(rv[0], 'to_json'):
                return Flask.make_response(self, (jsonify(rv[0].to_json()),
                                                  rv[1]))

        return Flask.make_response(self, rv)


def create_app(config=None):
    from .api import api
    from . import settings

    app = JSONFlask("twentiment_api")

    app.config.from_object(settings)
    if config is not None:
        app.config.update(config)

    app.register_blueprint(api)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
