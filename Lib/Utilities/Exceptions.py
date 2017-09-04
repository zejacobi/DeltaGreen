"""
File containing any custom exceptions used in this program
"""


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NotFoundError(Error):
    """
    Exception raised when an excepted file or database entry cannot be found

    :ivar str message: Gives context as to what exactly is missing.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
