import unittest
import math

import mongomock

import Lib.Utilities.Mongo as Mongo
import Lib.Character as Character

from Lib.Character import RandomCharacter, BaseCharacter
from Lib.Utilities.Exceptions import NotFoundError
from Tests.RandomMock import RandomMock
from ExternalServices import SAVE_LOCATION


class TestBaseCharacter(unittest.TestCase):
    """
    Testing the simple display functions in the BaseCharacter class
    """
    def setUp(self):
        self.character = BaseCharacter()
        self.character.skills = {
            "Accounting": 10,
            "Alertness": 20,
            "Anthropology": 0,
        }

    def test_double_underscore_str(self):
        """Tests the __str__ method of the class, ensuring it gives the expected output"""
        self.character.bonds = [{'_id': 'Hairdresser'}]
        self.character.class_name = 'Firefighter'
        self.character.package_name = 'Criminal'
        self.character.damaged_veteran = 'Gone Horribly Right'
        self.character.lost_bonds = [{'_id': 'Brother'}]
        self.character.disorders = ['OCD']
        self.character.adapted = {'Violence': True, 'Helplessness': False}

        char_str = str(self.character)
        format_args = [
            self.character.class_name, self.character.package_name, self.character.damaged_veteran,
            self.character.disorders[0], self.character.bonds[0]['_id'],
            self.character.lost_bonds[0]['_id'], 'Violence']

        expected_str = 'Class:                {}\n' \
                       'Skill package:        {}\n' \
                       'Damaged veteran type: {}\nDisorders:\n' \
                       '    {}\n\nBonds:\n' \
                       '    {}: 0\n\n' \
                       'Lost bonds:\n    {}\n\n' \
                       'Adapted to:\n    {}\n\n' \
                       'Attributes:\n' \
                       '    Hit Points:     0\n' \
                       '    Willpower:      0\n' \
                       '    Sanity:         0\n' \
                       '    Breaking Point: 0\n' \
                       '\nStats:\n' \
                       '    Strength:     0\n' \
                       '    Dexterity:    0\n' \
                       '    Constitution: 0\n' \
                       '    Intelligence: 0\n' \
                       '    Power:        0\n' \
                       '    Charisma:     0\n\nSkills:\n'.format(*format_args)

        for skill in sorted(self.character.skills.keys()):
            expected_str += '    {}: {}\n'.format(skill, self.character.skills[skill])

        self.assertEqual(char_str, expected_str)

    def test_get_skills(self):
        """It should return the character's skills object"""
        self.assertEqual(self.character.get_skills(), self.character.skills)

    def test_get_class(self):
        """It should return the character's class name"""
        self.character.class_name = 'Driver'

        self.assertEqual(self.character.get_class(), self.character.class_name)

    def test_get_package(self):
        """It should return the character's class name"""
        self.character.package_name = 'Driver'

        self.assertEqual(self.character.get_package(), self.character.package_name)

    def test_get_stats(self):
        """It should return the character's stats"""
        stats = {
            'Charisma': 15,
            'Constitution': 11,
            'Dexterity': 12,
            'Intelligence': 13,
            'Power': 14,
            'Strength': 10
        }
        self.character.stats = stats

        self.assertEqual(self.character.get_stats(), stats)

    def test_get_attributes(self):
        """It should return the character's attributes"""
        attr = {
            'Sanity': 77,
            'Hit Points': 12,
            'Willpower Points': 18,
            'Breaking Point': 72
        }
        self.character.sanity = attr['Sanity']
        self.character.hp = attr['Hit Points']
        self.character.wp = attr['Willpower Points']
        self.character.bp = attr['Breaking Point']

        self.assertEqual(self.character.get_attributes(), attr)

    def test_get_bonds(self):
        """Tests that it returns the array of bonds"""
        bonds = [{"_id": "Daughter"}, {"_id": "Son"}]
        self.character.bonds = bonds

        self.assertEqual(self.character.get_bonds(), [bond["_id"] for bond in bonds])

    def test_get_lost_bonds(self):
        """Tests that it returns the array of bonds"""
        bonds = [{"_id": "Daughter"}, {"_id": "Son"}]
        self.character.lost_bonds = bonds

        self.assertEqual(self.character.get_lost_bonds(), [bond["_id"] for bond in bonds])

    def test_get_bond_type(self):
        """Tests that it returns the expected array"""
        bonds = [{
            "_id": "Mother",
            "Required": None,
            "Family": True,
            "Romantic": False,
            "Friend": False,
            "Work": False,
            "Therapy": False
        }, {
            "_id": "Bartender",
            "Required": None,
            "Family": False,
            "Romantic": False,
            "Friend": True,
            "Work": False,
            "Therapy": True
        }]
        self.character.bonds = bonds

        self.assertEqual(self.character.get_bond_types(), {
            "Family": True,
            "Romantic": False,
            "Friend": True,
            "Work": False,
            "Therapy": True
        })

    def test_has_bond_type_type_exists_and_character_has_it(self):
        """Tests that it returns true when the type of bond exists and the character has one"""
        bonds = [{
            "_id": "Mother",
            "Required": None,
            "Family": True,
            "Romantic": False,
            "Friend": False,
            "Work": False,
            "Therapy": False
        }, {
            "_id": "Bartender",
            "Required": None,
            "Family": False,
            "Romantic": False,
            "Friend": True,
            "Work": False,
            "Therapy": True
        }]
        self.character.bonds = bonds

        self.assertEqual(self.character.has_bond_type('Family'), True)

    def test_has_bond_type_type_exists_and_character_does_not_have_it(self):
        """Tests that it returns false when the type of bond exists and the character doesn't
            have one"""
        bonds = [{
            "_id": "Mother",
            "Required": None,
            "Family": True,
            "Romantic": False,
            "Friend": False,
            "Work": False,
            "Therapy": False
        }, {
            "_id": "Bartender",
            "Required": None,
            "Family": False,
            "Romantic": False,
            "Friend": True,
            "Work": False,
            "Therapy": True
        }]
        self.character.bonds = bonds

        self.assertEqual(self.character.has_bond_type('Romantic'), False)

    def test_has_bond_type_type_does_not_exist(self):
        """Tests that it returns false when the type of doesn't exist"""
        bonds = [{
            "_id": "Mother",
            "Required": None,
            "Family": True,
            "Romantic": False,
            "Friend": False,
            "Work": False,
            "Therapy": False
        }, {
            "_id": "Bartender",
            "Required": None,
            "Family": False,
            "Romantic": False,
            "Friend": True,
            "Work": False,
            "Therapy": True
        }]
        self.character.bonds = bonds

        self.assertEqual(self.character.has_bond_type('Relative'), False)

    def test_get_disorders(self):
        """Tests that it returns the array of disorders"""
        disorders = ['Anxiety', 'Depression']
        self.character.disorders = disorders

        self.assertEqual(self.character.get_disorders(), disorders)

    def test_get_adaptations_none(self):
        """Tests that it returns an empty array when the character isn't adapted to anything"""
        self.assertEqual(self.character.get_adaptations(), [])

    def test_get_adaptations(self):
        """Tests that it returns an array with any adaptations the character might have"""
        adapted = 'Violence'
        self.character.adapted[adapted] = True

        self.assertEqual(self.character.get_adaptations(), [adapted])

    def test_get_veteran_type(self):
        """It should return the type set on the character class"""
        vet_type = 'Things Man Was Not Meant to Know'
        self.character.damaged_veteran = vet_type

        self.assertEqual(self.character.get_veteran_type(), vet_type)

    def test_get_character(self):
        """Tests that it parrots everything that has been passed to it"""
        expected = {
            'Class': 'Firefighter',
            'Package': 'Criminal',
            'Number_Bonds': 4,
            'Bonds': {'Hairdresser': 0},
            'Lost_Bonds': [],
            'Veteran': '',
            'Disorders': [],
            'Adapted_To': [],
            'Attributes': self.character.get_attributes(),
            'Stats': self.character.get_stats(),
            'Skills': self.character.get_skills()
        }
        self.character.class_name = expected['Class']
        self.character.package_name = expected['Package']
        self.character.num_bonds = expected['Number_Bonds']
        self.character.bonds = [{'_id': list(expected['Bonds'].keys())[0]}]

        self.assertEqual(self.character.get_character(), expected)


class TestRandomCharacter(unittest.TestCase):
    """Test RandomCharacter Class"""
    @classmethod
    def setUpClass(cls):
        cls.skills = {
            "Accounting": 10,
            "Alertness": 20,
            "Anthropology": 0,
            "Archeology": 0,
            "Artillery": 0,
            "Athletics": 0,
            "Bureaucracy": 0,
            "Computer Science": 0,
            "Unnatural": 0,
            "Ride": 0,
            "Occult": 0
        }
        cls.skill_names = [skill for skill in cls.skills.keys()]
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
        cls.sub_skill_names = [skill for skill in cls.sub_skills.keys()]
        cls.mappings = {
            "Accounting": ["Intelligence"],
            "Alertness": ["Intelligence", "Power"],
            "Anthropology": ["Intelligence", "Charisma"],
            "Archeology": ["Intelligence"],
            "Artillery": ["Intelligence"],
            "Art": ["Dexterity", "Power"],
            "Foreign Language": ["Intelligence", "Charisma"],
            "Ride": ["Dexterity", "Constitution"]
        }

        cls.random_mock = RandomMock()

    def setUp(self):
        self.character = RandomCharacter(self.skills, self.sub_skills, self.mappings)
        self.character.random = self.random_mock  # deterministic and controllable random mock

    def tearDown(self):
        self.random_mock.range_state = -1
        self.random_mock.choice_state = -1
        self.random_mock.sample_state = -1

        self.random_mock.range_list = []
        self.random_mock.choice_list = []
        self.random_mock.sample_list = []

    def test_private_get_subskill_str(self):
        """Test that sub-skill names are properly formatted"""
        self.assertEqual(self.character._get_subskill_str('a', 'b'), 'a (b)')

    def test_private_get_random_sub_skill(self):
        """Test that the result from random.choice is returned"""
        self.random_mock.choice_list = [self.sub_skills['Art'][1]]

        self.assertEqual(self.character._get_random_sub_skill('Art'),
                         self.random_mock.choice_list[0])

    def test_private_set_skill(self):
        """Tests that setting an accessible skill returns true and actually does set the skill"""
        with self.subTest(msg='Testing that the setting the skill returns true'):
            self.assertEqual(self.character._set_skill(self.skill_names[0], 30), True)

        with self.subTest(msg='Testing that the skill was set to the desired value'):
            self.assertEqual(self.character.skills[self.skill_names[0]], 30)

    def test_private_set_skill_not_found(self):
        """Tests that trying to set the value of a non-existent skill returns false"""
        self.assertEqual(self.character._set_skill('Nonexistent', 30), False)

    def test_private_set_skill_with_a_subskill(self):
        """Tests that setting an accessible sub-skill returns true and sets a random sub-skill to
            the provided value"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]

        with self.subTest(msg='Testing that the setting the skill returns true'):
            self.assertEqual(self.character._set_skill(self.sub_skill_names[0], 30), True)

        with self.subTest(msg='Testing that the skill was set to the desired value'):
            self.assertEqual(self.character.skills[
                self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'], 30)

    def test_private_add_sub_skill(self):
        """Tests that it will add a new skill, set to 0"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        sub_skill_str = skill + ' (' + sub + ')'

        with self.subTest(msg='Testing that the sub-skill string is returned'):
            self.assertEqual(self.character._add_sub_skill(skill, sub), sub_skill_str)

        with self.subTest(msg='Testing that the sub-skill was set to 0'):
            self.assertEqual(self.character.skills[sub_skill_str], 0)

    def test_private_add_sub_skill_with_existing(self):
        """Tests that it will return the skill string without affecting the value when the skill has
            already been added to the list"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        sub_skill_str = skill + ' (' + sub + ')'
        starting_value = 50
        self.character.skills[sub_skill_str] = starting_value

        with self.subTest(msg='Testing that the sub-skill string is returned'):
            self.assertEqual(self.character._add_sub_skill(skill, sub), sub_skill_str)

        with self.subTest(msg='Testing that the sub-skill value was not changed'):
            self.assertEqual(self.character.skills[sub_skill_str], starting_value)

    def test_private_add_sub_skill_at_random(self):
        """Tests that a random sub-skill will be added if a specific one isn't provided"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]

        with self.subTest(msg='Testing that the sub-skill string is returned'):
            self.assertEqual(self.character._add_sub_skill(self.sub_skill_names[0], ''),
                             self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')')

        with self.subTest(msg='Testing that the sub-skill is added and set to 0'):
            self.assertEqual(self.character.skills[
                self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'], 0)

    def test_private_set_sub_skill(self):
        """Tests that it will add a new skill, set to the provided value"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        expected_str = skill + ' (' + sub + ')'
        value = 50

        with self.subTest(msg='Tests that it returns true'):
            self.assertEqual(self.character._set_sub_skill(skill, sub, value), True)

        with self.subTest(msg='Tests that it sets the sub-skill to the expected value'):
            self.assertEqual(self.character.skills[expected_str], value)

    def test_private_set_sub_skill_with_existing(self):
        """Tests that it will set the sub-skill to the provided value"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        expected_str = skill + ' (' + sub + ')'
        starting_value = 50
        new_value = 70
        self.character.skills[expected_str] = starting_value

        with self.subTest(msg='Tests that it returns true'):
            self.assertEqual(self.character._set_sub_skill(skill, sub, new_value), True)

        with self.subTest(msg='Tests that it sets the sub-skill to the expected value'):
            self.assertEqual(self.character.skills[expected_str], new_value)

    def test_private_set_sub_skill_at_random(self):
        """Tests that a random sub-skill will be added if a specific one isn't provided"""
        value = 50
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]

        with self.subTest(msg='Tests that it returns true'):
            self.assertEqual(self.character._set_sub_skill(self.sub_skill_names[0], '', value),
                             True)

        with self.subTest(msg='Tests that it sets the sub-skill to the expected value'):
            self.assertEqual(self.character.skills[
                self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'], value)

    def test_private_add_random_sub_skill(self):
        """Tests that this will return a string incorporating a random sub-skill and add it to the
            character"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        expected_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'

        with self.subTest(msg='Tests that it returns the expected string'):
            self.assertEqual(self.character._add_random_sub_skill(self.sub_skill_names[0]),
                             expected_str)

        with self.subTest(msg='Tests that it sets the new skill to 0'):
            self.assertEqual(self.character.skills[expected_str], 0)

    def test_private_add_random_sub_skill_novel_false(self):
        """Tests that this will return a string incorporating a random sub-skill and not overwrite
            it if it already exists (this requires the novel kwarg to be false, otherwise a
            different skill would be chose)."""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        expected_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'
        starting_value = 50
        self.character.skills[expected_str] = starting_value

        with self.subTest(msg='Tests that it returns False'):
            self.assertEqual(self.character._add_random_sub_skill(self.sub_skill_names[0], False),
                             expected_str)

        with self.subTest(msg='Tests that it does not edit the already existing sub-skill'):
            self.assertEqual(self.character.skills[expected_str], starting_value)

    def test_private_add_random_sub_skill_retry_needed(self):
        """Tests that this will try as many times as are necessary to get a new sub-skill if it picks
            one that already exists (as long as novel is true)"""
        self.random_mock.choice_list = [
            self.sub_skills[self.sub_skill_names[0]][0],
            self.sub_skills[self.sub_skill_names[0]][0],
            self.sub_skills[self.sub_skill_names[0]][0],
            self.sub_skills[self.sub_skill_names[0]][1],
        ]
        existing_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'
        new_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[-1] + ')'
        starting_value = 50
        self.character.skills[existing_str] = starting_value

        with self.subTest(msg='Test that it returns the string of the eventually chosen sub-skill'):
            self.assertEqual(self.character._add_random_sub_skill(self.sub_skill_names[0]), new_str)

        with self.subTest(msg='Test that is does not alter any of the values of the rejected '
                              'choices'):
            self.assertEqual(self.character.skills[existing_str], starting_value)

        with self.subTest(msg='Tests that it sets the new skill to 0'):
            self.assertEqual(self.character.skills[new_str], 0)

        with self.subTest(msg='Test that it retried finding a sub-skill the correct number of '
                              'times'):
            self.assertEqual(self.random_mock.choice_state, len(self.random_mock.choice_list) - 1)

    def test_private_safe_set_skill(self):
        """Test that it can set an ordinary skill still at its default value to another value"""
        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._safe_set_skill(self.skill_names[0], '', 60), True)

        with self.subTest(msg='Tests that it sets the skill to the expected value'):
            self.assertEqual(self.character.skills[self.skill_names[0]], 60)

    def test_private_safe_set_already_set(self):
        """Test that it won't overwrite an already set skill value"""
        value = 55
        self.character.skills[self.skill_names[0]] = value

        with self.subTest(msg='Tests that it returns False'):
            self.assertEqual(self.character._safe_set_skill(self.skill_names[0], '', 60), False)

        with self.subTest(msg='Tests that the skill value does not change'):
            self.assertEqual(self.character.skills[self.skill_names[0]], value)

    def test_private_safe_set_skill_random_sub_skill(self):
        """Test that if provided a sub-skill type skill without the specific sub-skill specified, it
            will pick and set one at random"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        expected_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._safe_set_skill(self.sub_skill_names[0], '', 60), True)

        with self.subTest(msg='Tests that it sets the expected random sub-skill to the expected '
                              'value'):
            self.assertEqual(self.character.skills[expected_str], 60)

    def test_private_safe_set_skill_new_sub_skill(self):
        """Test that if provided a skill and sub-skill and the sub-skill is new, that it returns
            true and set the sub-skill to the provided value"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._safe_set_skill(skill, sub, 60), True)

        with self.subTest(msg='Tests that it sets the named sub-skill to the expected value'):
            self.assertEqual(self.character.skills[expected_str], 60)

    def test_private_safe_set_skill_existing_sub_skill(self):
        """Test that if provided a skill and sub-skill and the sub-skill exists but is still 0, that
            it return true and set the sub-skill to the provided value"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.character.skills[expected_str] = 0

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._safe_set_skill(skill, sub, 60), True)

        with self.subTest(msg='Tests that it sets the named sub-skill to the expected value'):
            self.assertEqual(self.character.skills[expected_str], 60)

    def test_private_safe_set_skill_existing_sub_skill_with_value(self):
        """Test that if provided a skill and sub-skill and the sub-skill exists and is not 0, that
            it returns false and leaves the sub-skill alone"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        starting_value = 30
        self.character.skills[expected_str] = starting_value

        with self.subTest(msg='Tests that it returns False'):
            self.assertEqual(self.character._safe_set_skill(skill, sub, 60), False)

        with self.subTest(msg='Tests that the starting value is preserved'):
            self.assertEqual(self.character.skills[expected_str], starting_value)

    def test_private_add_to_skill(self):
        """Tests that it can add to an already existing skill"""
        starting_value = self.character.skills[self.skill_names[0]]

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_skill(self.skill_names[0], 20), True)

        with self.subTest(msg='Tests that it adds the appropriate amount to the skill'):
            self.assertEqual(self.character.skills[self.skill_names[0]], starting_value + 20)

    def test_private_add_to_skill_invalid(self):
        """Tests that it won't add if the skill doesn't exist"""
        self.assertEqual(self.character._add_to_skill('Moustache', 20), False)

    def test_private_add_to_skill_with_sub_skill(self):
        """Tests that it can add to a sub skill"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.random_mock.choice_list = [sub]

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_skill(skill, 20), True)

        with self.subTest(msg='Tests that it adds the appropriate amount to the sub-skill'):
            self.assertEqual(self.character.skills[expected_str], 20)

    def test_private_add_to_skill_with_sub_skill_existing_but_not_novel(self):
        """Tests that it can add to a sub-skill if it already exists but novel is false"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.character.skills[expected_str] = 20
        self.random_mock.choice_list = [sub]

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_skill(skill, 20, False), True)

        with self.subTest(msg='Tests that it adds the appropriate amount to the sub-skill'):
            self.assertEqual(self.character.skills[expected_str], 40)

    def test_private_add_to_skill_with_sub_skill_existing_and_novel(self):
        """Tests that it will try as many times as it needs to in order to add to a novel
            sub-skill"""
        skill = self.sub_skill_names[0]
        sub1 = self.sub_skills[skill][0]
        sub2 = self.sub_skills[skill][1]
        original_string = skill + ' (' + sub1 + ')'
        new_string = skill + ' (' + sub2 + ')'
        self.character.skills[original_string] = 20
        self.random_mock.choice_list = [sub1, sub1, sub1, sub1, sub2]

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_skill(skill, 20), True)

        with self.subTest(msg='Tests that it will not add to non-novel skills, even when they are'
                              'picked in intermediate steps'):
            self.assertEqual(self.character.skills[original_string], 20)

        with self.subTest(msg='Tests that it adds the appropriate amount to the sub-skill'):
            self.assertEqual(self.character.skills[new_string], 20)

        with self.subTest(msg='Tests that it took the expected number of tries to find a novel '
                              'sub-skill'):
            self.assertEqual(self.random_mock.choice_state, len(self.random_mock.choice_list) - 1)

    def test_private_add_to_sub_skill(self):
        """Tests that it can add to an already existing sub-skill"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        starting_value = 20
        self.character.skills[expected_str] = starting_value

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_sub_skill(skill, sub, 20), True)

        with self.subTest(msg='Tests that it adds the appropriate amount to the sub-skill'):
            self.assertEqual(self.character.skills[expected_str], starting_value + 20)

    def test_private_add_to_sub_skill_with_new_sub_skill(self):
        """Tests that it can add a sub skill and add the provided value to 0"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_sub_skill(skill, sub, 20), True)

        with self.subTest(msg='Tests that it puts the sub-skill at 20'):
            self.assertEqual(self.character.skills[expected_str], 20)

    def test_private_add_to_sub_skill_with_sub_skill_existing_but_not_novel(self):
        """Tests that it will add to the first randomly chosen sub-skill if that skill already
            exists and novel is false"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.character.skills[expected_str] = 20
        self.random_mock.choice_list = [sub]

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_sub_skill(skill, '', 20), True)

        with self.subTest(msg='Tests that it adds 20 to the sub-skill'):
            self.assertEqual(self.character.skills[expected_str], 40)

        with self.subTest(msg='Tests that it only calls random.choice once'):
            self.assertEqual(self.random_mock.choice_state, 0)

    def test_private_add_to_sub_skill_with_sub_skill_existing_and_novel(self):
        """Tests that it will try as many times as it needs to in order to add to a novel
            sub-skill"""
        skill = self.sub_skill_names[0]
        sub1 = self.sub_skills[skill][0]
        sub2 = self.sub_skills[skill][1]
        original_string = skill + ' (' + sub1 + ')'
        new_string = skill + ' (' + sub2 + ')'
        self.character.skills[original_string] = 20
        self.random_mock.choice_list = [sub1, sub1, sub1, sub1, sub2]

        with self.subTest(msg='Tests that it returns True'):
            self.assertEqual(self.character._add_to_sub_skill(skill, '', 20, True), True)

        with self.subTest(msg='Tests that it leaves the original sub-skill alone'):
            self.assertEqual(self.character.skills[original_string], 20)

        with self.subTest(msg='Tests that it adds 20 to the eventually chosen sub-skill'):
            self.assertEqual(self.character.skills[new_string], 20)

        with self.subTest(msg='Tests that it  calls random.choice as many times as is necessary'):
            self.assertEqual(self.random_mock.choice_state, len(self.random_mock.choice_list) - 1)

    def test_roll_stat(self):
        """Test that roll stat correctly grabs the top three results"""
        self.random_mock.range_list = [1, 2, 3, 4]

        self.assertEqual(self.character.roll_stat(), sum(self.random_mock.range_list[1:]))

    def test_apply_class(self):
        """Tests that applying a class with skills and sub-skills, but no choices, works"""
        class_obj = {
            "_id": "Test",
            "Skills": {
                "Anthropology": 40,
                "Archeology": 40,
            },
            "Choices": {
                "Number": 0,
                "Skills": {
                }
            },
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 50
                },
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 40
                }
            ],
            "Bonds": 4
        }
        language_choices = ['Spanish', 'Arabic']
        self.random_mock.choice_list = language_choices
        self.character.apply_class(class_obj)

        with self.subTest(msg='Test that the correct number of bonds are added to the character'):
            self.assertEqual(self.character.num_bonds, class_obj['Bonds'])

        with self.subTest(msg='Test that the class name is added to the character'):
            self.assertEqual(self.character.class_name, class_obj['_id'])

        with self.subTest(msg='Test that the class skill "Anthropology" is added to the character'):
            self.assertEqual(self.character.skills['Anthropology'], 40)

        with self.subTest(msg='Test that the class skill "Archeology" is added to the character'):
            self.assertEqual(self.character.skills['Archeology'], 40)

        with self.subTest(msg='Test that non-class skills aren\'t added to the character'):
            self.assertEqual(self.character.skills['Artillery'], 0)

        with self.subTest(msg='Test that the first random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[0] + ')'], 50)

        with self.subTest(msg='Test that the second random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[1] + ')'], 40)

    def test_apply_class_simple_choices(self):
        """Tests that applying a class with skill choices (but no overlap or sub-skills) works"""
        class_obj = {
            "_id": "Test",
            "Skills": {
                "Anthropology": 40,
                "Archeology": 40,
            },
            "Choices": {
                "Number": 1,
                "Skills": {
                    "Accounting": 50,
                    "Artillery": 40
                }
            },
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 50
                },
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 40
                }
            ],
            "Bonds": 4
        }
        language_choices = ['Spanish', 'Arabic']
        self.random_mock.choice_list = language_choices
        self.random_mock.sample_list = [['Artillery']]
        self.character.apply_class(class_obj)

        with self.subTest(msg='Test that the correct number of bonds are added to the character'):
            self.assertEqual(self.character.num_bonds, class_obj['Bonds'])

        with self.subTest(msg='Test that the class name is added to the character'):
            self.assertEqual(self.character.class_name, class_obj['_id'])

        with self.subTest(msg='Test that the class skill "Anthropology" is added to the character'):
            self.assertEqual(self.character.skills['Anthropology'], 40)

        with self.subTest(msg='Test that the class skill "Archeology" is added to the character'):
            self.assertEqual(self.character.skills['Archeology'], 40)

        with self.subTest(msg='Test any skill choices made are added to the character'):
            self.assertEqual(self.character.skills['Artillery'], 40)

        with self.subTest(msg='Test that the first random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[0] + ')'], 50)

        with self.subTest(msg='Test that the second random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[1] + ')'], 40)

    def test_apply_class_repeated_choices(self):
        """Tests that applying a class with overlap between set sub-skills and random sub-skills
            chosen as a choice will result in repeated attempts to find a workable random
            sub-skill"""
        class_obj = {
            "_id": "Test",
            "Skills": {
                "Anthropology": 40,
                "Archeology": 40,
            },
            "Choices": {
                "Number": 2,
                "Skills": {
                    "Accounting": 50,
                    "Artillery": 40,
                    "Foreign Language": 60
                }
            },
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 50
                },
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 40
                }
            ],
            "Bonds": 4
        }
        language_choices = ['Spanish', 'Arabic', 'Spanish', 'Arabic', 'French']
        self.random_mock.choice_list = language_choices
        self.random_mock.sample_list = [['Artillery', 'Foreign Language']]
        self.character.apply_class(class_obj)

        with self.subTest(msg='Test that the correct number of bonds are added to the character'):
            self.assertEqual(self.character.num_bonds, class_obj['Bonds'])

        with self.subTest(msg='Test that the class name is added to the character'):
            self.assertEqual(self.character.class_name, class_obj['_id'])

        with self.subTest(msg='Test that the class skill "Anthropology" is added to the character'):
            self.assertEqual(self.character.skills['Anthropology'], 40)

        with self.subTest(msg='Test that the class skill "Archeology" is added to the character'):
            self.assertEqual(self.character.skills['Archeology'], 40)

        with self.subTest(msg='Test any skill choices made are added to the character'):
            self.assertEqual(self.character.skills['Artillery'], 40)

        with self.subTest(msg='Test that the first random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[0] + ')'], 50)

        with self.subTest(msg='Test that the second random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[1] + ')'], 40)

        with self.subTest(msg='Test that the randomly chosen sub-skill is added correctly'):
            self.assertEqual(self.random_mock.choice_state, len(language_choices)-1)

    def test_apply_class_no_sub_skills_chosen(self):
        """Tests that applying a class with skill choices and sub-skill choices will still
            apply all of the skills if no sub-skills are chosen"""
        class_obj = {
            "_id": "Test",
            "Skills": {
                "Anthropology": 40,
                "Archeology": 40,
            },
            "Choices": {
                "Number": 1,
                "Skills": {
                    "Accounting": 50,
                    "Artillery": 40
                },
                "Subskills": [
                    {
                        "Skill": "Art",
                        "Sub": "Journalism",
                        "Value": 40
                    }
                ]
            },
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 50
                },
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 40
                }
            ],
            "Bonds": 4
        }
        language_choices = ['Spanish', 'Arabic']
        self.random_mock.choice_list = language_choices
        self.random_mock.sample_list = [[False], ['Artillery']]
        self.character.apply_class(class_obj)

        with self.subTest(msg='Test that the correct number of bonds are added to the character'):
            self.assertEqual(self.character.num_bonds, class_obj['Bonds'])

        with self.subTest(msg='Test that the class name is added to the character'):
            self.assertEqual(self.character.class_name, class_obj['_id'])

        with self.subTest(msg='Test that the class skill "Anthropology" is added to the character'):
            self.assertEqual(self.character.skills['Anthropology'], 40)

        with self.subTest(msg='Test that the class skill "Archeology" is added to the character'):
            self.assertEqual(self.character.skills['Archeology'], 40)

        with self.subTest(msg='Test any skill choices made are added to the character'):
            self.assertEqual(self.character.skills['Artillery'], 40)

        with self.subTest(msg='Test that the first random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[0] + ')'], 50)

        with self.subTest(msg='Test that the second random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[1] + ')'], 40)

    def test_apply_class_sub_skills_chosen(self):
        """Tests that applying a class with skill choices and sub-skill choices will replace any
            skills that might be applied with sub-skills if sub-skills are chosen"""
        class_obj = {
            "_id": "Test",
            "Skills": {
                "Anthropology": 40,
                "Archeology": 40,
            },
            "Choices": {
                "Number": 1,
                "Skills": {
                    "Accounting": 50,
                    "Artillery": 40
                },
                "Subskills": [
                    {
                        "Skill": "Art",
                        "Sub": "Journalism",
                        "Value": 40
                    }
                ]
            },
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 50
                },
                {
                    "Skill": "Foreign Language",
                    "Sub": "",
                    "Value": 40
                }
            ],
            "Bonds": 4
        }
        language_choices = ['Spanish', 'Arabic']
        self.random_mock.choice_list = language_choices
        self.random_mock.sample_list = [[class_obj['Choices']['Subskills'][0]]]
        self.character.apply_class(class_obj)

        with self.subTest(msg='Test that the correct number of bonds are added to the character'):
            self.assertEqual(self.character.num_bonds, class_obj['Bonds'])

        with self.subTest(msg='Test that the class name is added to the character'):
            self.assertEqual(self.character.class_name, class_obj['_id'])

        with self.subTest(msg='Test that the class skill "Anthropology" is added to the character'):
            self.assertEqual(self.character.skills['Anthropology'], 40)

        with self.subTest(msg='Test that the class skill "Archeology" is added to the character'):
            self.assertEqual(self.character.skills['Archeology'], 40)

        with self.subTest(msg='Test that un-chosen random skills will not be added to the '
                              'character'):
            self.assertEqual(self.character.skills['Artillery'], 0)

        with self.subTest(msg='Test that the first random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[0] + ')'], 50)

        with self.subTest(msg='Test that the second random Foreign Language sub-skill is added'):
            self.assertEqual(
                self.character.skills['Foreign Language (' + language_choices[1] + ')'], 40)

        with self.subTest(msg='Test that a randomly chosen sub-skill will be applied to the '
                              'character'):
            self.assertEqual(
                self.character.skills['Art (' + class_obj['Choices']['Subskills'][0]['Sub'] + ')'],
                40)

    def test_add_package_skill_normal_skill(self):
        """Tests that it will return true and apply +20 to a normal skill"""
        starting = self.character.skills[self.skill_names[0]]

        with self.subTest(msg='It should return true'):
            self.assertEqual(self.character.add_package_skill(self.skill_names[0], ''), True)

        with self.subTest(msg='It should give + 20 to the expected skill'):
            self.assertEqual(self.character.skills[self.skill_names[0]], starting + 20)

    def test_add_package_skill_sub_skill(self):
        """Tests that it will return true and apply +20 to a sub-skill with the specific type
            given"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'

        with self.subTest(msg='It should return true'):
            self.assertEqual(self.character.add_package_skill(skill, sub), True)

        with self.subTest(msg='It should give + 20 to the expected sub-skill'):
            self.assertEqual(self.character.skills[expected_str], 20)

    def test_add_package_skill_random_sub_skill(self):
        """Tests that it will return true and apply +20 to a sub-skill with a random type given"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.random_mock.choice_list = [sub]

        with self.subTest(msg='It should return true'):
            self.assertEqual(self.character.add_package_skill(skill, ''), True)

        with self.subTest(msg='It should give + 20 to a random sub-skill'):
            self.assertEqual(self.character.skills[expected_str], 20)

    def test_apply_package_simple_package(self):
        """It should add the skills and sub-skills to the character"""
        package = {
            "_id": "Test",
            "Skills": [
                "Alertness"
            ],
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "Spanish"
                }],
            "Choices": {
                "Number": 0,
                "All": False,
                "List": []
            }
        }
        self.character.apply_package(package)

        with self.subTest(msg='It should add the package name to the character'):
            self.assertEqual(self.character.package_name, package['_id'])

        with self.subTest(msg='It should increase the Alertness skill'):
            self.assertEqual(self.character.skills['Alertness'], 40)

        with self.subTest(msg='It should increase the Foreign Language (Spanish) skill'):
            self.assertEqual(self.character.skills['Foreign Language (Spanish)'], 20)

    def test_apply_package_one_all_choice(self):
        """It should add the skills and sub-skills to the character, then add one of the skills
            from all.
        """
        package = {
            "_id": "Test",
            "Skills": [
                "Alertness"
            ],
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "Spanish"
                }],
            "Choices": {
                "Number": 1,
                "All": True,
                "List": []
            }
        }
        self.skill_names.sort()
        expected_all_skill_value = self.character.skills[self.skill_names[0]] + 20
        self.character.apply_package(package)

        with self.subTest(msg='It should add the package name to the character'):
            self.assertEqual(self.character.package_name, package['_id'])

        with self.subTest(msg='It should increase the Alertness skill'):
            self.assertEqual(self.character.skills['Alertness'], 40)

        with self.subTest(msg='It should increase one random skill by 20'):
            self.assertEqual(self.character.skills[self.skill_names[0]], expected_all_skill_value)

        with self.subTest(msg='It should increase the Foreign Language (Spanish) skill'):
            self.assertEqual(self.character.skills['Foreign Language (Spanish)'], 20)

    def test_apply_package_one_choice(self):
        """It should add the skills and sub-skills to the character, then add one of the skills
            from the list of choices.
        """
        package = {
            "_id": "Test",
            "Skills": [
                "Alertness"
            ],
            "Subskills": [
                {
                    "Skill": "Foreign Language",
                    "Sub": "Spanish"
                }],
            "Choices": {
                "Number": 1,
                "All": False,
                "List": ['Foreign Language']
            }
        }
        self.random_mock.choice_list = ['Arabic']
        self.character.apply_package(package)

        with self.subTest(msg='It should add the package name to the character'):
            self.assertEqual(self.character.package_name, package['_id'])

        with self.subTest(msg='It should increase the Alertness skill'):
            self.assertEqual(self.character.skills['Alertness'], 40)

        with self.subTest(msg='It should increase the Foreign Language (Spanish) skill'):
            self.assertEqual(self.character.skills['Foreign Language (Spanish)'], 20)

        with self.subTest(msg='It should increase the Foreign Language (Arabic) skill as the '
                              'random choice'):
            self.assertEqual(self.character.skills['Foreign Language (Arabic)'], 20)

    def test_set_stat(self):
        """It should return true and modify the character if the stat exists"""
        with self.subTest(msg='It should return True'):
            self.assertEqual(self.character.set_stat('Strength', 10), True)

        with self.subTest(msg='It should return change the Strength stat to be equal to 10'):
            self.assertEqual(self.character.stats['Strength'], 10)

    def test_set_stat_does_not_exist(self):
        """It should return false and leave the character untouched if the stat doesn't exist"""
        with self.subTest(msg='It should return False'):
            self.assertEqual(self.character.set_stat('Wisdom', 10), False)

        with self.subTest(msg='It should not affect the stats object'):
            self.assertEqual(self.character.stats, {
                'Strength': 0,
                'Dexterity': 0,
                'Constitution': 0,
                'Intelligence': 0,
                'Power': 0,
                'Charisma': 0
            })

    def test_apply_stats_floor(self):
        """It should apply stats in order of best to worst based on available skills"""
        self.random_mock.range_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                       1, 1, 1, 1, 1, 2, 3, 5, 1, 3, 3, 5, 1, 3, 4, 5, 1, 3, 4, 6,
                                       1, 3, 5, 6, 1, 3, 6, 6]
        self.character.skills['Foreign Language (French)'] = 50
        self.character.skills['Art (Journalism)'] = 40
        self.character.skills['Anthropology'] = 30
        self.character.skills['Ride'] = 60
        self.character.num_bonds = 4
        self.character.apply_stats()

        self.assertEqual(self.character.stats, {'Charisma': 15,
                                                'Constitution': 11,
                                                'Dexterity': 12,
                                                'Intelligence': 13,
                                                'Power': 14,
                                                'Strength': 10})

    def test_apply_stats_no_floor(self):
        """It should re-roll nothing if the floor doesn't exist"""
        self.random_mock.range_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                       1, 1, 1, 1, 1, 2, 3, 5, 1, 3, 3, 5, 1, 3, 4, 5, 1, 3, 4, 6,
                                       1, 3, 5, 6, 1, 3, 6, 6]
        self.character.skills['Foreign Language (French)'] = 50
        self.character.skills['Art (Journalism)'] = 40
        self.character.skills['Anthropology'] = 30
        self.character.skills['Ride'] = 60
        self.character.num_bonds = 4
        self.character.apply_stats(0)

        self.assertEqual(self.character.stats, {'Charisma': 3,
                                                'Constitution': 3,
                                                'Dexterity': 3,
                                                'Intelligence': 3,
                                                'Power': 3,
                                                'Strength': 3})

    def test_calculate_attributes(self):
        """It should correctly set the attributes based on the stats"""
        self.character.stats = {'Charisma': 15,
                                'Constitution': 11,
                                'Dexterity': 12,
                                'Intelligence': 13,
                                'Power': 14,
                                'Strength': 10}
        self.character.calculate_attributes()

        with self.subTest(msg='Test that HP was set correctly'):
            self.assertEqual(
                self.character.hp, int(math.ceil((self.character.stats['Strength']
                                                  + self.character.stats['Constitution'])/2)))

        with self.subTest(msg='Test that WP was set correctly'):
            self.assertEqual(self.character.wp, self.character.stats['Power'])

        with self.subTest(msg='Test that Sanity was set correctly'):
            self.assertEqual(self.character.sanity, self.character.stats['Power'] * 5)

        with self.subTest(msg='Test that BP was set correctly'):
            self.assertEqual(self.character.bp, self.character.stats['Power'] * 4)

    def test_add_bond(self):
        """Tests that it adds a bond to the array of bonds"""
        bond = {
            "_id": "Mother",
            "Required": None,
            "Family": True,
            "Romantic": False,
            "Friend": False,
            "Work": False,
            "Therapy": False
        }
        self.character.add_bond(bond)

        self.assertEqual(self.character.bonds, [bond])

    def test_damaged_veteran_violence(self):
        """Tests that all properties from the Extreme Violence damaged veteran were properly set"""
        new_occult = self.character.skills['Occult'] + 10
        new_charisma = self.character.stats['Charisma'] - 3
        new_sanity = self.character.sanity - 5
        self.character.damaged_veteran_violence()

        with self.subTest('Checking that occult increased'):
            self.assertEqual(self.character.skills['Occult'], new_occult)

        with self.subTest('Checking that sanity decreased'):
            self.assertEqual(self.character.sanity, new_sanity)

        with self.subTest('Checking that Charisma decreased'):
            self.assertEqual(self.character.stats['Charisma'], new_charisma)

        with self.subTest('Checking that the character is now adapted to violence'):
            self.assertEqual(self.character.adapted['Violence'], True)

        with self.subTest('Checking that the type of damaged veteran was set'):
            self.assertEqual(self.character.damaged_veteran, 'Extreme Violence')

    def test_damaged_veteran_helplessness(self):
        """Tests that all properties from the Captivity or Imprisonment damaged veteran were
        properly set"""
        new_occult = self.character.skills['Occult'] + 10
        new_power = self.character.stats['Power'] - 3
        new_sanity = self.character.sanity - 5
        self.character.damaged_veteran_helplessness()

        with self.subTest('Checking that occult increased'):
            self.assertEqual(self.character.skills['Occult'], new_occult)

        with self.subTest('Checking that sanity decreased'):
            self.assertEqual(self.character.sanity, new_sanity)

        with self.subTest('Checking that Power decreased'):
            self.assertEqual(self.character.stats['Power'], new_power)

        with self.subTest('Checking that the character is now adapted to violence'):
            self.assertEqual(self.character.adapted['Helplessness'], True)

        with self.subTest('Checking that the type of damaged veteran was set'):
            self.assertEqual(self.character.damaged_veteran, 'Captivity or Imprisonment')

    def test_damaged_veteran_experience(self):
        """Tests that all properties from the Hard Experience damaged veteran were
            properly set"""
        remaining_bond = {"_id": "Mom"}
        lost_bond = {"_id": "Wife"}
        self.character.num_bonds = 2
        expected_bonds = self.character.num_bonds - 1
        self.random_mock.sample_list = [["Alertness", "Athletics", "Bureaucracy",
                                         "Computer Science"]]
        self.character.bonds = [remaining_bond, lost_bond]
        new_skills = {skill: self.character.skills[skill] + 10
                      for skill in self.random_mock.sample_list[0]}
        new_skills['Occult'] = self.character.skills['Occult'] + 10
        new_sanity = self.character.sanity - 5
        self.character.damaged_veteran_experience()

        for skill in new_skills:
            with self.subTest('Checking that there was an appropriate increase in the skill: '
                              + skill):
                self.assertEqual(self.character.skills[skill], new_skills[skill])

        with self.subTest('Checking that sanity decreased'):
            self.assertEqual(self.character.sanity, new_sanity)

        with self.subTest('Checking that number of bonds decreased'):
            self.assertEqual(self.character.num_bonds, expected_bonds)

        with self.subTest('Checking that only one bond is left'):
            self.assertEqual(self.character.bonds, [remaining_bond])

        with self.subTest('Checking that the lost bond was recorded'):
            self.assertEqual(self.character.lost_bonds, [lost_bond])

        with self.subTest('Checking that the type of damaged veteran was set'):
            self.assertEqual(self.character.damaged_veteran, 'Hard Experience')

    def test_damaged_veteran_unnatural(self):
        """Tests that all properties from the Things Man Was Not Meant to Know damaged veteran were
        properly set"""
        new_occult = self.character.skills['Occult'] + 20
        new_unnatural = self.character.skills['Unnatural'] + 10
        disorder = {'_id': 'Depression'}
        self.random_mock.choice_list = [disorder]

        self.character.stats['Power'] = 5

        new_sanity = self.character.sanity - self.character.stats['Power']
        new_bp = self.character.bp - self.character.stats['Power']

        self.character.damaged_veteran_unnatural([disorder])

        with self.subTest('Checking that occult increased'):
            self.assertEqual(self.character.skills['Occult'], new_occult)

        with self.subTest('Checking that Unnatural increased'):
            self.assertEqual(self.character.skills['Unnatural'], new_unnatural)

        with self.subTest('Checking that sanity decreased'):
            self.assertEqual(self.character.sanity, new_sanity)

        with self.subTest('Checking that breaking point decreased'):
            self.assertEqual(self.character.bp, new_bp)

        with self.subTest('Checking that the disorder was added'):
            self.assertEqual(self.character.disorders, [disorder['_id']])

        with self.subTest('Checking that the type of damaged veteran was set'):
            self.assertEqual(self.character.damaged_veteran, 'Things Man Was Not Meant to Know')

    def test_damaged_veteran_violence_exists(self):
        """It should not change the veteran type or apply any veteran logic if type already set"""
        existing_type = 'Something or other'
        starting_san = self.character.sanity
        self.character.damaged_veteran = existing_type

        self.character.damaged_veteran_violence()

        with self.subTest('It should not change the damaged veteran type'):
            self.assertEqual(self.character.damaged_veteran, existing_type)

        with self.subTest('It should not change the sanity'):
            self.assertEqual(self.character.sanity, starting_san)

    def test_damaged_veteran_helplessness_exists(self):
        """It should not change the veteran type or apply any veteran logic if type already set"""
        existing_type = 'Something or other'
        starting_san = self.character.sanity
        self.character.damaged_veteran = existing_type

        self.character.damaged_veteran_helplessness()

        with self.subTest('It should not change the damaged veteran type'):
            self.assertEqual(self.character.damaged_veteran, existing_type)

        with self.subTest('It should not change the sanity'):
            self.assertEqual(self.character.sanity, starting_san)

    def test_damaged_veteran_experience_exists(self):
        """It should not change the veteran type or apply any veteran logic if type already set"""
        existing_type = 'Something or other'
        starting_san = self.character.sanity
        self.character.damaged_veteran = existing_type

        self.character.damaged_veteran_experience()

        with self.subTest('It should not change the damaged veteran type'):
            self.assertEqual(self.character.damaged_veteran, existing_type)

        with self.subTest('It should not change the sanity'):
            self.assertEqual(self.character.sanity, starting_san)

    def test_damaged_veteran_unnatural_exists(self):
        """It should not change the veteran type or apply any veteran logic if type already set"""
        existing_type = 'Something or other'
        starting_san = self.character.sanity
        self.character.damaged_veteran = existing_type

        self.character.damaged_veteran_unnatural([{"_id": "Lupus"}])

        with self.subTest('It should not change the damaged veteran type'):
            self.assertEqual(self.character.damaged_veteran, existing_type)

        with self.subTest('It should not change the sanity'):
            self.assertEqual(self.character.sanity, starting_san)


class TestCharacterFromDict(unittest.TestCase):
    """Tests for CharacterFromDict class"""

    @classmethod
    def setUpClass(cls):
        """We need to set up the character dictionary"""
        cls.character_obj = BaseCharacter()
        cls.character_obj.skills = {
            "Accounting": 10,
            "Alertness": 20,
            "Anthropology": 0,
        }
        cls.character_obj.bonds = [{'_id': 'Hairdresser'}]
        cls.character_obj.class_name = 'Firefighter'
        cls.character_obj.package_name = 'Criminal'
        cls.character_obj.damaged_veteran = 'Gone Horribly Right'
        cls.character_obj.lost_bonds = [{'_id': 'Brother'}]
        cls.character_obj.disorders = ['OCD']
        cls.character_obj.adapted = {'Violence': True, 'Helplessness': False}
        cls.character_dict = cls.character_obj.get_character()

    def test_exception_on_missing_id(self):
        """Testing an exception is raised when we pass in a dictionary missing keys"""
        with self.assertRaises(NotFoundError):
            Character.CharacterFromDict({})

    def test_initialization(self):
        """
        Tests that the CharacterFromDict can be initialized without errors and correctly sets all
        properties
        """
        try:
            character = Character.CharacterFromDict(self.character_dict)
        except NotFoundError:
            self.fail('__init__() unexpectedly raised NotFoundError')

        with self.subTest(mgs='It should successfully set the skills'):
            self.assertDictEqual(character.skills, self.character_obj.skills)

        with self.subTest(mgs='It should successfully set the number of bonds'):
            self.assertEqual(character.num_bonds, self.character_obj.num_bonds)

        with self.subTest(mgs='It should successfully set the bonds'):
            self.assertEqual(character.bonds, self.character_obj.bonds)

        with self.subTest(mgs='It should successfully set the lost bonds'):
            self.assertEqual(character.lost_bonds, self.character_obj.lost_bonds)

        with self.subTest(mgs='It should successfully set the class name'):
            self.assertEqual(character.class_name, self.character_obj.class_name)

        with self.subTest(mgs='It should successfully set the package name'):
            self.assertEqual(character.package_name, self.character_obj.package_name)

        with self.subTest(mgs='It should successfully set the disorders'):
            self.assertEqual(character.disorders, self.character_obj.disorders)

        with self.subTest(mgs='It should successfully set the adapted properties'):
            self.assertEqual(character.adapted, self.character_obj.adapted)

        with self.subTest(mgs='It should successfully set the veteran type'):
            self.assertEqual(character.damaged_veteran, self.character_obj.damaged_veteran)

        with self.subTest(mgs='It should successfully set the stats'):
            self.assertDictEqual(character.stats, self.character_obj.stats)

        with self.subTest(mgs='It should successfully set the HP'):
            self.assertEqual(character.hp, self.character_obj.hp)

        with self.subTest(mgs='It should successfully set the WP'):
            self.assertEqual(character.wp, self.character_obj.wp)

        with self.subTest(mgs='It should successfully set the BP'):
            self.assertEqual(character.bp, self.character_obj.bp)

        with self.subTest(mgs='It should successfully set the San'):
            self.assertEqual(character.sanity, self.character_obj.sanity)


class TestLoadedCharacter(unittest.TestCase):
    """Tests for LoadedCharacters class"""

    @classmethod
    def setUpClass(cls):
        """
        We need to set a mocked database for the whole character package here, then we need to
        save a character to that database and note the _id
        """
        cls.mongo_obj = Mongo
        cls.mongo = mongomock.MongoClient()['Test']
        cls.mongo_obj.database = cls.mongo
        Character.Mongo = cls.mongo_obj
        cls.character_obj = BaseCharacter()
        cls.character_obj.skills = {
            "Accounting": 10,
            "Alertness": 20,
            "Anthropology": 0,
        }
        cls.character_obj.bonds = [{'_id': 'Hairdresser'}]
        cls.character_obj.class_name = 'Firefighter'
        cls.character_obj.package_name = 'Criminal'
        cls.character_obj.damaged_veteran = 'Gone Horribly Right'
        cls.character_obj.lost_bonds = [{'_id': 'Brother'}]
        cls.character_obj.disorders = ['OCD']
        cls.character_obj.adapted = {'Violence': True, 'Helplessness': False}

        cls.character_id = cls.mongo_obj.insert(cls.character_obj.get_character(), SAVE_LOCATION)

    def test_exception_on_missing_id(self):
        """Testing an exception is raised when the saved character isn't found"""
        with self.assertRaises(NotFoundError):
            Character.LoadedCharacter('AAAA1234AAAA1234AAAA1234')

    def test_initialization(self):
        """
        Tests that the LoadedCharacter can be initialized without errors and correctly sets all
        properties
        """
        try:
            character = Character.LoadedCharacter(str(self.character_id))
        except NotFoundError:
            self.fail('__init__() unexpectedly raised NotFoundError')

        with self.subTest(mgs='It should successfully set the skills'):
            self.assertDictEqual(character.skills, self.character_obj.skills)

        with self.subTest(mgs='It should successfully set the number of bonds'):
            self.assertEqual(character.num_bonds, self.character_obj.num_bonds)

        with self.subTest(mgs='It should successfully set the bonds'):
            self.assertEqual(character.bonds, self.character_obj.bonds)

        with self.subTest(mgs='It should successfully set the lost bonds'):
            self.assertEqual(character.lost_bonds, self.character_obj.lost_bonds)

        with self.subTest(mgs='It should successfully set the class name'):
            self.assertEqual(character.class_name, self.character_obj.class_name)

        with self.subTest(mgs='It should successfully set the package name'):
            self.assertEqual(character.package_name, self.character_obj.package_name)

        with self.subTest(mgs='It should successfully set the disorders'):
            self.assertEqual(character.disorders, self.character_obj.disorders)

        with self.subTest(mgs='It should successfully set the adapted properties'):
            self.assertEqual(character.adapted, self.character_obj.adapted)

        with self.subTest(mgs='It should successfully set the veteran type'):
            self.assertEqual(character.damaged_veteran, self.character_obj.damaged_veteran)

        with self.subTest(mgs='It should successfully set the stats'):
            self.assertDictEqual(character.stats, self.character_obj.stats)

        with self.subTest(mgs='It should successfully set the HP'):
            self.assertEqual(character.hp, self.character_obj.hp)

        with self.subTest(mgs='It should successfully set the WP'):
            self.assertEqual(character.wp, self.character_obj.wp)

        with self.subTest(mgs='It should successfully set the BP'):
            self.assertEqual(character.bp, self.character_obj.bp)

        with self.subTest(mgs='It should successfully set the San'):
            self.assertEqual(character.sanity, self.character_obj.sanity)
