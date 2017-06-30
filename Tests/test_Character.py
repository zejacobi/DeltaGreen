import unittest

from Lib.Character import Character
from Tests.RandomMock import RandomMock


class TestParsingJSON(unittest.TestCase):
    """Test the JSON parsing"""
    @classmethod
    def setUpClass(cls):
        cls.skills = {
            "Accounting": 10,
            "Alertness": 20,
            "Anthropology": 0,
            "Archeology": 0,
            "Artillery": 0,
        }
        cls.sub_skills = {
            "Art": [
                "Creative Writing",
                "Journalism"
            ],
            "Foreign Language": [
                "Spanish",
                "French",
                "Arabic"
            ]
        }
        cls.mappings = {
            "Accounting": ["Intelligence"],
            "Alertness": ["Intelligence"],
            "Anthropology": ["Intelligence"],
            "Archeology": ["Intelligence"],
            "Artillery": ["Intelligence"],
            "Art": ["Dexterity", "Power"],
            "Foreign Language": ["Intelligence", "Charisma"]
        }

        cls.random_mock = RandomMock()

    def setUp(self):
        self.character = Character(self.skills, self.sub_skills, self.mappings)
        self.character.random = self.random_mock  # deterministic and controllable random mock

    def tearDown(self):
        self.random_mock.range_state = 0
        self.random_mock.choice_state = 0
        self.random_mock.sample_state = 0

        self.random_mock.range_list = []
        self.random_mock.choice_list = []
        self.random_mock.sample_list = []

    def test_private_get_subskill_str(self):
        """Test that sub-skill names are properly formatted"""
        self.assertEqual(self.character._get_subskill_str('a', 'b'), 'a (b)')

    def test_private_get_random_sub_skill(self):
        """Test that ther esult from random.choice is returned"""
        self.random_mock.choice_list = [self.sub_skills['Art'][1]]
        self.assertEqual(self.character._get_random_sub_skill('Art'),
                         self.random_mock.choice_list[0])

    def test_roll_stat(self):
        """Test that roll stat correctly grabs the top three results"""
        self.random_mock.range_list = [1, 2, 3, 4]
        self.assertEqual(self.character.roll_stat(), sum(self.random_mock.range_list[1:]))
