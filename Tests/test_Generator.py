import unittest
import mongomock
import operator

from os import path

from Lib.Utilities.Workspace import parse_json
from Tests.RandomMock import RandomMock
from Tests.TestData import data_path

import Lib.Mongo as Mongo
import Lib.Generator as Generator


class TestGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """We need to set up two mocks (a Mongo Database and the random package) as well as
            populate the Mongo database with test data."""
        cls.mongo_obj = Mongo
        cls.mongo = mongomock.MongoClient()['Test']
        cls.mongo_obj.database = cls.mongo
        Generator.Mongo = cls.mongo_obj
        cls.random_mock = RandomMock()

        cls.bonds = parse_json(path.join(data_path, 'bonds.json'))[0]
        cls.bonds = sorted(cls.bonds, key=operator.itemgetter('Work'), reverse=True)
        cls.classes = parse_json(path.join(data_path, 'classes.json'))[0]
        cls.default_stats = parse_json(path.join(data_path, 'default_stats.json'))[0]
        cls.packages = parse_json(path.join(data_path, 'packages.json'))[0]
        cls.skill_mapping = parse_json(path.join(data_path, 'skill_mapping.json'))[0]
        cls.sub_skills = parse_json(path.join(data_path, 'sub_skills.json'))[0]

        cls.mongo_obj.insert(cls.bonds, 'bonds')
        cls.mongo_obj.insert(cls.classes, 'classes')
        cls.mongo_obj.insert(cls.default_stats, 'default_stats')
        cls.mongo_obj.insert(cls.packages, 'packages')
        cls.mongo_obj.insert(cls.skill_mapping, 'skill_mapping')
        cls.mongo_obj.insert(cls.sub_skills, 'sub_skills')

        cls.default_stats.pop('_id')
        cls.skill_mapping.pop('_id')
        cls.sub_skills.pop('_id')

    def setUp(self):
        self.generator = Generator.Generator()
        self.generator.character.random = self.random_mock

        self.random_mock.range_state = -1
        self.random_mock.choice_state = -1
        self.random_mock.sample_state = -1

        self.random_mock.range_list = []
        self.random_mock.choice_list = []
        self.random_mock.sample_list = []

    def test_init_classes(self):
        """Initializing the class should have grabbed the classes from the database"""
        self.assertEqual(self.generator.classes, self.classes)

    def test_init_packages(self):
        """Initializing the class should have grabbed the packages from the database"""
        self.assertEqual(self.generator.packages, self.packages)

    def test_init_defaults(self):
        """Initializing the class should have grabbed the defaults from the database"""
        self.assertEqual(self.generator.defaults, self.default_stats)

    def test_init_skill_mappings(self):
        """Initializing the class should have grabbed the skill mappings from the database"""
        self.assertEqual(self.generator.skill_mapping, self.skill_mapping)

    def test_init_sub_skills(self):
        """Initializing the class should have grabbed the sub-skills from the database"""
        self.assertEqual(self.generator.sub_skills, self.sub_skills)

    def test_private_get_bonds_no_class(self):
        """Tests that no class specific bonds will be returned when it's run without a class or
            package"""
        self.generator._get_bonds()
        self.assertEqual(self.generator.bonds,
                         [bond for bond in self.bonds if bond["Required"] is None])

    def test_private_get_bonds_all(self):
        """Tests that all bonds will be returned if the character has the correct prerequisites"""
        self.generator.character.class_name = "Federal Agent"
        self.generator.character.package_name = "Office Worker"
        self.generator._get_bonds()
        self.assertEqual(self.generator.bonds, self.bonds)

    def test_random_character_class(self):
        """Tests that applying a character class is done randomly and sets the all expected
            skills"""
        class_name = 'Federal Agent'
        skill_choice = 'Accounting'
        self.random_mock.choice_list = [class_obj for class_obj in self.classes
                                        if class_obj['_id'] == class_name]
        self.random_mock.sample_list = [[skill_choice]]
        self.generator.random_character_class()
        self.assertEqual(self.generator.character.class_name, class_name)
        self.assertEqual(self.generator.character.num_bonds, 3)
        self.assertEqual(self.generator.character.skills[skill_choice], 60)
        for skill in self.random_mock.choice_list[0]['Skills'].keys():
            with self.subTest(msg='Testing setting the skill: ' + skill):
                self.assertEqual(self.generator.character.skills[skill],
                                 self.random_mock.choice_list[0]['Skills'][skill])

    def test_random_character_package(self):
        """Tests that applying a package is done randomly and adds 20 to all 8 skills"""
        package_name = 'Weasel'
        self.random_mock.choice_list = [package for package in self.packages
                                        if package['_id'] == package_name]
        self.generator.random_character_package()
        for skill in self.random_mock.choice_list[0]['Skills']:
            with self.subTest(msg='Testing setting the skill: ' + skill):
                self.assertEqual(self.generator.character.skills[skill],
                                 self.default_stats[skill] + 20)

    def test_random_character_stats(self):
        """Tests that it correctly sets the stats based on the existing skills"""
        self.random_mock.range_list = [3, 3, 4, 1, 3, 3, 5, 1, 3, 4, 6, 1, 3, 4, 6, 1, 3, 5, 6, 1,
                                       3, 6, 6, 1]
        self.generator.character.num_bonds = 1
        self.generator.character.skills['Unarmed Combat'] = 99
        self.generator.character.skills['Melee Weapons'] = 98
        self.generator.character.skills['Swim'] = 97
        self.generator.character.skills['Athletics'] = 96
        self.generator.character.skills['Psychotherapy'] = 95
        self.generator.random_character_stats()
        self.assertEqual(self.generator.character.stats, {
            'Strength': 15,
            'Dexterity': 14,
            'Constitution': 13,
            'Intelligence': 10,
            'Power': 13,
            'Charisma': 11
        })

    def test_random_character_bonds_no_bonds(self):
        """Tests the no bonds are added if the character has no capacity for bonds"""
        self.generator.character.num_bonds = 0
        self.generator.random_character_bonds()
        self.assertEqual(self.generator.character.bonds, [])

    def test_random_character_bonds_one_bond(self):
        """Tests that only one bond is added when the character only has the capacity for one
            bond"""
        self.generator.character.num_bonds = 1
        self.random_mock.choice_list = [self.bonds[0]]
        self.generator.random_character_bonds()
        self.assertEqual(self.generator.character.bonds, self.random_mock.choice_list)

    def test_random_character_bonds_ignore_repeats(self):
        """Tests that the same bond cannot be added multiple times"""
        self.generator.character.num_bonds = 2
        self.random_mock.choice_list = [self.bonds[0], self.bonds[0], self.bonds[-1]]
        self.generator.random_character_bonds()
        self.assertEqual(self.generator.character.bonds, [self.bonds[0], self.bonds[-1]])

    def test_random_character_bonds_ignore_invalid(self):
        """Tests that invalid bonds will be ignored"""
        self.generator.character.num_bonds = 2
        self.random_mock.choice_list = [self.bonds[0], {"_id": "Fake"}, self.bonds[-1]]
        self.generator.random_character_bonds()
        self.assertEqual(self.generator.character.bonds, [self.bonds[0], self.bonds[-1]])

    def test_random_character_bonds_ignore_same_type(self):
        """Tests that the same type of bond cannot be added multiple times"""
        self.generator.character.num_bonds = 2
        self.random_mock.choice_list = [self.bonds[0], self.bonds[1], self.bonds[-1]]
        self.generator.random_character_bonds()
        self.assertEqual(self.generator.character.bonds, [self.bonds[0], self.bonds[-1]])

    def test_random_character_bonds_add_all_bonds(self):
        """Tests that all bonds become fair game once all types are full"""
        self.generator.character.num_bonds = len(self.bonds)
        self.random_mock.choice_list = self.bonds
        self.generator.random_character_bonds()
        self.assertEqual(sorted(self.generator.character.bonds, key=operator.itemgetter('_id')),
                         sorted(self.bonds, key=operator.itemgetter('_id')))
