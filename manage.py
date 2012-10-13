#!/usr/bin/env python
"""
Management script for the twentiment_api Flask project.

:author: 2012, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

import sys
import os
from flask.ext.script import Manager, Server


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))


from twentiment_api.application import create_app


manager = Manager(create_app())
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


@manager.command
def test():
    os.system("unit2 discover")


if __name__ == "__main__":
    manager.run()
