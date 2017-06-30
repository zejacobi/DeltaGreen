"""
Package that provides a deterministic mock of the functions from the built-in  random module I use
"""


class RandomMock(object):
    """
    Class that is a random mock
    """
    def __init__(self):
        self.range_state = -1
        self.choice_state = -1
        self.sample_state = -1

        self.range_list = []
        self.choice_list = []
        self.sample_list = []

    def randrange(self, *_):
        self.range_state += 1
        return self.range_list[self.range_state % len(self.range_list)]

    def choice(self, *_):
        self.choice_state += 1
        return self.choice_list[self.choice_state % len(self.choice_list)]

    def sample(self, *_):
        self.sample_state += 1
        return self.sample_list[self.sample_state % len(self.sample_list)]
