"""Top level script for running tests, necessary for coverage.py"""

import unittest
import os
import shutil

import coverage


if __name__ == '__main__':
    missing_file = 'ExternalServices.py'
    if not os.path.isfile(missing_file):
        # For safety, we can't checkin this file. Which breaks the tests. Need to copy a version of
        # it for CI.
        path = os.path.join('Tests', 'TestData', missing_file)
        shutil.copy(path, missing_file)

from Tests.test_Character import *
from Tests.test_Exceptions import *
from Tests.test_Generator import *
from Tests.test_SeedDB import *
from Tests.test_Utilities_Mongo import *
from Tests.test_Utilities_Workspace import *
from Tests.test_v1 import *

if __name__ == '__main__':
    unittest.main(exit=False)
