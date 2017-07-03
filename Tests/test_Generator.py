import unittest
import mongomock

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
        cls.MongoObj = Mongo
        cls.mongo = mongomock.MongoClient()['Test']
        cls.MongoObj.database = cls.mongo
        Generator.Mongo = cls.MongoObj
        cls.random_mock = RandomMock()

        cls.bonds = parse_json(path.join(data_path, 'bonds.json'))[0]
        cls.classes = parse_json(path.join(data_path, 'classes.json'))[0]
        cls.default_stats = parse_json(path.join(data_path, 'default_stats.json'))[0]
        cls.packages = parse_json(path.join(data_path, 'packages.json'))[0]
        cls.skill_mapping = parse_json(path.join(data_path, 'skill_mapping.json'))[0]
        cls.sub_skills = parse_json(path.join(data_path, 'sub_skills.json'))[0]

        cls.MongoObj.insert(cls.bonds, 'bonds')
        cls.MongoObj.insert(cls.classes, 'classes')
        cls.MongoObj.insert(cls.default_stats, 'default_stats')
        cls.MongoObj.insert(cls.packages, 'packages')
        cls.MongoObj.insert(cls.skill_mapping, 'skill_mapping')
        cls.MongoObj.insert(cls.sub_skills, 'sub_skills')

        cls.default_stats.pop('_id')
        cls.skill_mapping.pop('_id')
        cls.sub_skills.pop('_id')

    def setUp(self):
        self.generator = Generator.Generator()
        self.generator.character.random = self.random_mock

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
