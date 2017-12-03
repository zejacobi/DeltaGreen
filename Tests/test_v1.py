import unittest
import operator
import json

import Tests._test_app as test_app

from os import path

from Lib.Character import BaseCharacter
from ExternalServices import SAVE_LOCATION
from Lib.Utilities.Workspace import parse_json
from Tests.TestData import data_path


class TestV1Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Here I get five crucial things registered: 1) the Flask app, 2) a Mongo Mock, and 3)
            a test client that allows me to make requests without having to register a server,
            4) a mock for the RNG, and 5) the API prefix."""
        cls.app = test_app.app
        cls.mongo = test_app.TEST_MONGO
        cls.random_mock = test_app.RANDOM_MOCK

        cls.bonds = parse_json(path.join(data_path, 'bonds.json'))[0]
        cls.bonds = sorted(cls.bonds, key=operator.itemgetter('Work'), reverse=True)
        cls.classes = parse_json(path.join(data_path, 'classes.json'))[0]
        cls.default_stats = parse_json(path.join(data_path, 'default_stats.json'))[0]
        cls.packages = parse_json(path.join(data_path, 'packages.json'))[0]
        cls.skill_mapping = parse_json(path.join(data_path, 'skill_mapping.json'))[0]
        cls.sub_skills = parse_json(path.join(data_path, 'sub_skills.json'))[0]
        cls.violence_disorders = parse_json(path.join(data_path, 'violence_disorders.json'))[0]
        cls.unnatural_disorders = parse_json(path.join(data_path, 'unnatural_disorders.json'))[0]
        cls.helplessness_disorders = parse_json(path.join(data_path,
                                                          'helplessness_disorders.json'))[0]

        cls.mongo.insert(cls.bonds, 'bonds')
        cls.mongo.insert(cls.classes, 'classes')
        cls.mongo.insert(cls.default_stats, 'default_stats')
        cls.mongo.insert(cls.packages, 'packages')
        cls.mongo.insert(cls.skill_mapping, 'skill_mapping')
        cls.mongo.insert(cls.sub_skills, 'sub_skills')
        cls.mongo.insert(cls.helplessness_disorders, 'disorders')
        cls.mongo.insert(cls.unnatural_disorders, 'disorders')
        cls.mongo.insert(cls.violence_disorders, 'disorders')

        cls.default_stats.pop('_id')
        cls.skill_mapping.pop('_id')
        cls.sub_skills.pop('_id')

        cls.app = test_app.app
        cls.test_client = cls.app.test_client()
        cls.url_prefix = test_app.URL_PREFIX + '/'
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
        cls.character_data = cls.character_obj.get_character()

        cls.character_id = cls.mongo.insert(cls.character_obj.get_character(), SAVE_LOCATION)

    def setUp(self):
        """Time to initialize the RNG"""
        self.random_mock.range_state = -1
        self.random_mock.choice_state = -1
        self.random_mock.sample_state = -1

        self.random_mock.range_list = []
        self.random_mock.choice_list = []
        self.random_mock.sample_list = []

    def test_post_characters_400_missing_properties(self):
        """It should return 400 if there are missing properties in the provided JSON"""
        res = self.test_client.post(self.url_prefix + 'characters',
                                    data=json.dumps({"test": True}),
                                    content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_post_characters_400_json_err(self):
        """It should return 400 if the JSON is missing or otherwise cannot be parsed"""
        res = self.test_client.post(self.url_prefix + 'characters')
        self.assertEqual(res.status_code, 400)

    def test_post_characters_200(self):
        """It should return 200 if given a full character"""
        res = self.test_client.post(self.url_prefix + 'characters',
                                    data=json.dumps(self.character_data),
                                    content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_post_characters_ID(self):
        """It should return a correctly sized ID if there are no problems with the function"""
        res = self.test_client.post(self.url_prefix + 'characters',
                                    data=json.dumps(self.character_data),
                                    content_type='application/json')
        id = json.loads(res.data.decode('utf-8'))["ID"]
        self.assertEqual(len(id), 24)

    def test_get_characters(self):
        """It should return 200 when asked to generate a character"""
        class_name = 'Federal Agent'
        skill_choice = 'Accounting'
        package_name = 'Weasel'
        self.random_mock.choice_list = [class_obj for class_obj in self.classes
                                        if class_obj['_id'] == class_name]
        self.random_mock.choice_list.extend([package for package in self.packages
                                             if package['_id'] == package_name])
        self.random_mock.choice_list.extend(self.bonds[-3:])
        self.random_mock.range_list = [5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 1,
                                       5, 5, 5, 1, 1]
        self.random_mock.sample_list = [[skill_choice]]

        expected_stats = {
            'Strength': 15,
            'Dexterity': 15,
            'Constitution': 15,
            'Intelligence': 15,
            'Power': 15,
            'Charisma': 15
        }

        res = self.test_client.get(self.url_prefix + 'characters')
        character = json.loads(res.data.decode('utf-8'))["Character"]

        with self.subTest(msg='Testing that the endpoint returns 200'):
            self.assertEqual(res.status_code, 200)

        with self.subTest(msg='Testing that the return object is correct'):
            expected = {
                'Class': class_name,
                'Package': package_name,
                'Number_Bonds': self.random_mock.choice_list[0]['Bonds'],
                'Bonds': {bond['_id']: expected_stats['Charisma'] for bond in self.bonds[-3:]},
                'Lost_Bonds': [],
                'Veteran': '',
                'Disorders': [],
                'Adapted_To': [],
                'Attributes': {
                    'Sanity': 75,
                    'Hit Points': 15,
                    'Willpower Points': 15,
                    'Breaking Point': 60
                },
                'Stats': expected_stats,
                'Skills': {'Accounting': 80,
                           'Alertness': 70,
                           'Anthropology': 0,
                           'Archeology': 0,
                           'Artillery': 0,
                           'Athletics': 30,
                           'Bureaucracy': 60,
                           'Computer Science': 0,
                           'Criminology': 70,
                           'Demolitions': 0,
                           'Disguise': 10,
                           'Dodge': 30,
                           'Drive': 50,
                           'Firearms': 50,
                           'First Aid': 10,
                           'Forensics': 30,
                           'HUMINT': 80,
                           'Heavy Machinery': 10,
                           'Heavy Weapons': 0,
                           'History': 10,
                           'Law': 50,
                           'Medicine': 0,
                           'Melee Weapons': 30,
                           'Navigate': 10,
                           'Occult': 10,
                           'Persuade': 70,
                           'Pharmacy': 0,
                           'Psychotherapy': 10,
                           'Ride': 10,
                           'SIGINT': 0,
                           'Search': 50,
                           'Stealth': 30,
                           'Surgery': 0,
                           'Survival': 10,
                           'Swim': 20,
                           'Unarmed Combat': 60,
                           'Unnatural': 0
                           },

            }
            self.assertEqual(character, expected)

    def test_load_character_400_invalid_id(self):
        """Tests that 400 is returned if the provided ID cannot be converted to an ObjectID"""
        res = self.test_client.get(self.url_prefix + 'characters/1')
        self.assertEqual(res.status_code, 400)

    def test_load_character_404_not_found_id(self):
        """Tests that 404 is returned if the provided ID cannot be found"""
        res = self.test_client.get(self.url_prefix + 'characters/' + "a" * 24)
        self.assertEqual(res.status_code, 404)

    def test_load_character(self):
        """Tests that character can be correctly loaded"""
        res = self.test_client.get(self.url_prefix + 'characters/' + str(self.character_id))

        with self.subTest(msg='Testing that the endpoint returns 200'):
            self.assertEqual(res.status_code, 200)

        character = json.loads(res.data.decode('utf-8'))["Character"]

        with self.subTest(msg='Testing that the return object is correct'):
            self.assertEqual(character, self.character_data)
