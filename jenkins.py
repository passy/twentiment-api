#!/usr/bin/env python

import xmlrunner
import coverage
from tests import suite


if __name__ == '__main__':
    cov = coverage.coverage()
    cov.erase()
    cov.start()
    xmlrunner.XMLTestRunner(output='test-reports').run(suite())
    cov.stop()
    cov.save()
    cov.xml_report()
