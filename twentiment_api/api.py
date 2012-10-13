"""
Blueprint implementing the API wrapper.


:author: 2012, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

from flask import Blueprint, request

api = Blueprint("api", __name__, url_prefix="/v1")


class GuessResponse(object):
    def __init__(self, score):
        self.score = score

    @property
    def label(self):
        # Should get some tweaking
        if self.score < 0:
            return 'negative'
        elif self.score > 0:
            return 'positive'
        else:
            return 'neutral'

    def to_json(self):
        return {'score': self.score,
                'label': self.label}


@api.route('/guess', methods=['GET'])
def guess():
    message = request.args['message']

    return GuessResponse(0.0)
