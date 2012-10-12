"""
Test suite loader for the twentiment-api unit and functional tests.

:author: 2012, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

from unittest2 import TestSuite
from unittest2 import defaultTestLoader

from . import test_api


def suite():
    """Returns the test suite for this module."""

    result = TestSuite()
    loader = defaultTestLoader

    result.addTest(loader.loadTestsFromModule(test_api))

    return result
