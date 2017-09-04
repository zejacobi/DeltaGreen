import unittest

from Lib.Utilities.Exceptions import NotFoundError


class TestNotFoundError(unittest.TestCase):
    def test_raisable(self):
        """Test that using the exception with the raise keyword raises an actual exception"""
        with self.assertRaises(NotFoundError):
            raise NotFoundError('This is a test')

    def test_str_representation(self):
        error_str = 'This is a test'
        try:
            raise NotFoundError(error_str)
        except NotFoundError as error:
            self.assertEqual(str(error), error_str)
