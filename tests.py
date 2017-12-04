"""Top level script for running tests, necessary for coverage.py"""

import unittest

import coverage

from Tests.test_Character import *
from Tests.test_Exceptions import *
from Tests.test_Generator import *
from Tests.test_SeedDB import *
from Tests.test_Utilities_Mongo import *
from Tests.test_Utilities_Workspace import *
from Tests.test_v1 import *

if __name__ == '__main__':
    unittest.main(exit=False)
