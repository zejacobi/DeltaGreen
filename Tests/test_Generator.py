import unittest

import mongomock
import operator

from os import path

import Lib.Generator as Generator
import Lib.Utilities.Mongo as Mongo

from Lib.Utilities.Workspace import parse_json
from Tests.RandomMock import RandomMock
from Tests.TestData import data_path


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
        cls.violence_disorders = parse_json(path.join(data_path, 'violence_disorders.json'))[0]
        cls.unnatural_disorders = parse_json(path.join(data_path, 'unnatural_disorders.json'))[0]
        cls.helplessness_disorders = parse_json(path.join(data_path,
                                                          'helplessness_disorders.json'))[0]

        cls.mongo_obj.insert(cls.bonds, 'bonds')
        cls.mongo_obj.insert(cls.classes, 'classes')
        cls.mongo_obj.insert(cls.default_stats, 'default_stats')
        cls.mongo_obj.insert(cls.packages, 'packages')
        cls.mongo_obj.insert(cls.skill_mapping, 'skill_mapping')
        cls.mongo_obj.insert(cls.sub_skills, 'sub_skills')
        cls.mongo_obj.insert(cls.helplessness_disorders, 'disorders')
        cls.mongo_obj.insert(cls.unnatural_disorders, 'disorders')
        cls.mongo_obj.insert(cls.violence_disorders, 'disorders')

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

    def test_init_disorders(self):
        """Initializing the class should have grabbed the sub-skills from the database"""
        self.assertEqual(self.generator.disorders, {
            "Violence": self.violence_disorders,
            "Helplessness": self.helplessness_disorders,
            "Unnatural": self.unnatural_disorders
        })

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

        with self.subTest(msg='Testing that the class name was correctly set'):
            self.assertEqual(self.generator.character.class_name, class_name)

        with self.subTest(msg='Testing the number of bonds matches what\'s expected for the class'):
            self.assertEqual(self.generator.character.num_bonds, 3)

        with self.subTest(msg='Testing that the skill choice went as expected'):
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

    def test_random_damaged_veteran_violence(self):
        self.random_mock.choice_list = ['Violence']
        self.generator.random_damaged_veteran()

        self.assertEqual(self.generator.character.damaged_veteran, 'Extreme Violence')

    def test_random_damaged_veteran_helpless(self):
        self.random_mock.choice_list = ['Helpless']
        self.generator.random_damaged_veteran()

        self.assertEqual(self.generator.character.damaged_veteran, 'Captivity or Imprisonment')

    def test_random_damaged_veteran_unnatural(self):
        self.random_mock.choice_list = ['Unnatural', self.generator.disorders['Unnatural'][0]]
        self.generator.random_damaged_veteran()

        self.assertEqual(self.generator.character.damaged_veteran,
                         'Things Man Was Not Meant to Know')

    def test_random_damaged_veteran_experience(self):
        self.random_mock.choice_list = ['Hard Experience']
        self.random_mock.sample_list = [["Alertness", "Athletics", "Bureaucracy",
                                         "Computer Science"]]
        self.generator.character.bonds = [{"_id": "Wife"}, {"_id": "Mom"}]
        self.generator.random_damaged_veteran()

        self.assertEqual(self.generator.character.damaged_veteran, 'Hard Experience')

    def test_generate(self):
        """Tests that a random character is generated"""
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
        character = self.generator.generate()

        expected_stats = {
            'Strength': 15,
            'Dexterity': 15,
            'Constitution': 15,
            'Intelligence': 15,
            'Power': 15,
            'Charisma': 15
        }

        with self.subTest(msg='Testing that stats are set correctly'):
            self.assertEqual(self.generator.character.stats, expected_stats)

        with self.subTest(msg='Testing that the class name was set correctly'):
            self.assertEqual(self.generator.character.class_name, class_name)

        with self.subTest(msg='Testing that the package name was set correctly'):
            self.assertEqual(self.generator.character.package_name, package_name)

        with self.subTest(msg='Testing that the number of bonds were set correctly'):
            self.assertEqual(self.generator.character.num_bonds,
                             self.random_mock.choice_list[0]['Bonds'])

        with self.subTest(msg='Testing that the bonds were set correctly'):
            self.assertEqual(sorted(self.generator.character.bonds, key=operator.itemgetter('_id')),
                             sorted(self.bonds[-3:], key=operator.itemgetter('_id')))

        with self.subTest(msg='Testing that the skills are set correctly'):
            for skill in self.random_mock.choice_list[0]['Skills'].keys():
                with self.subTest(msg='Testing setting the skill: ' + skill):
                    skill_level = (self.random_mock.choice_list[0]['Skills'][skill]
                                   + 20 * (skill in self.random_mock.choice_list[1]['Skills']))
                    self.assertEqual(self.generator.character.skills[skill], skill_level)

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
                'Skills': self.generator.character.skills
            }
            self.assertEqual(character, expected)

    def test_generate_damaged_veteran(self):
        """Tests that a random character is generated with damaged veteran stats applied when
            one is randomly chosen"""
        class_name = 'Federal Agent'
        skill_choice = 'Accounting'
        package_name = 'Weasel'
        self.random_mock.choice_list = [class_obj for class_obj in self.classes
                                        if class_obj['_id'] == class_name]
        self.random_mock.choice_list.extend([package for package in self.packages
                                             if package['_id'] == package_name])
        self.random_mock.choice_list.extend(self.bonds[-3:])
        self.random_mock.range_list = [5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 1, 5, 5, 5, 1,
                                       5, 5, 5, 1, 2]
        self.random_mock.sample_list = [[skill_choice]]
        self.random_mock.choice_list.append('Violence')
        self.generator.generate()

        with self.subTest(msg='Testing that stats are set correctly'):
            self.assertEqual(self.generator.character.stats, {
                'Strength': 15,
                'Dexterity': 15,
                'Constitution': 15,
                'Intelligence': 15,
                'Power': 15,
                'Charisma': 12
            })

        with self.subTest(msg='Testing that the class name was set correctly'):
            self.assertEqual(self.generator.character.class_name, class_name)

        with self.subTest(msg='Testing that the package name was set correctly'):
            self.assertEqual(self.generator.character.package_name, package_name)

        with self.subTest(msg='Testing that the number of bonds were set correctly'):
            self.assertEqual(self.generator.character.num_bonds,
                             self.random_mock.choice_list[0]['Bonds'])

        with self.subTest(msg='Testing that the bonds were set correctly'):
            self.assertEqual(sorted(self.generator.character.bonds, key=operator.itemgetter('_id')),
                             sorted(self.bonds[-3:], key=operator.itemgetter('_id')))

        for skill in self.random_mock.choice_list[0]['Skills'].keys():
            with self.subTest(msg='Testing setting the skill: ' + skill):
                skill_level = (self.random_mock.choice_list[0]['Skills'][skill]
                               + 20 * (skill in self.random_mock.choice_list[1]['Skills']))
                self.assertEqual(self.generator.character.skills[skill], skill_level)

        with self.subTest(msg='Testing that occult was updated'):
            self.assertEqual(self.generator.character.skills['Occult'],
                             self.default_stats['Occult'] + 10)

        with self.subTest('Checking that the character is now adapted to violence'):
            self.assertEqual(self.generator.character.adapted['Violence'], True)

        with self.subTest('Checking that the type of damaged veteran was set'):
            self.assertEqual(self.generator.character.damaged_veteran, 'Extreme Violence')

    def test_save_character(self):
        """Tests saving a character."""
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
        self.generator.generate()

        character_id = self.generator.save_character()

        returned_character = self.mongo_obj.find_all('SavedCharacters')[0]

        with self.subTest(msg='Test that the ID in the DB matches that returned by the function'):
            self.assertEqual(character_id, returned_character['_id'])

        with self.subTest(msg='Test that the character is fully saved in the DB'):
            expected = {
                '_id': character_id,
                'Class': class_name,
                'Package': package_name,
                'Number_Bonds': self.random_mock.choice_list[0]['Bonds'],
                'Bonds': {bond['_id']: 15 for bond in self.bonds[-3:]},
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
                'Stats': {
                    'Strength': 15,
                    'Dexterity': 15,
                    'Constitution': 15,
                    'Intelligence': 15,
                    'Power': 15,
                    'Charisma': 15
                },
                'Skills': self.generator.character.skills
            }
            self.maxDiff = None
            self.assertEqual(returned_character, expected)


class TestGeneratorOGL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This is much less involved, as we just need to test two functions"""
        cls.mongo_obj = Mongo
        cls.mongo = mongomock.MongoClient()['Test']
        cls.mongo_obj.database = cls.mongo
        Generator.Mongo = cls.mongo_obj

        cls.classes = parse_json(path.join(data_path, 'classes.json'))[0]
        cls.classes[0]['open'] = True
        cls.packages = parse_json(path.join(data_path, 'packages.json'))[0]
        cls.packages[0]['open'] = True

        cls.mongo_obj.insert(cls.classes, 'classes')
        cls.mongo_obj.insert(cls.packages, 'packages')

        # Insert the rest of the stuff just to avoid errors
        cls.bonds = parse_json(path.join(data_path, 'bonds.json'))[0]
        cls.bonds = sorted(cls.bonds, key=operator.itemgetter('Work'), reverse=True)
        cls.default_stats = parse_json(path.join(data_path, 'default_stats.json'))[0]
        cls.skill_mapping = parse_json(path.join(data_path, 'skill_mapping.json'))[0]
        cls.sub_skills = parse_json(path.join(data_path, 'sub_skills.json'))[0]
        cls.violence_disorders = parse_json(path.join(data_path, 'violence_disorders.json'))[0]
        cls.unnatural_disorders = parse_json(path.join(data_path, 'unnatural_disorders.json'))[0]
        cls.helplessness_disorders = parse_json(path.join(data_path,
                                                          'helplessness_disorders.json'))[0]

        cls.mongo_obj.insert(cls.bonds, 'bonds')
        cls.mongo_obj.insert(cls.default_stats, 'default_stats')
        cls.mongo_obj.insert(cls.skill_mapping, 'skill_mapping')
        cls.mongo_obj.insert(cls.sub_skills, 'sub_skills')
        cls.mongo_obj.insert(cls.helplessness_disorders, 'disorders')
        cls.mongo_obj.insert(cls.unnatural_disorders, 'disorders')
        cls.mongo_obj.insert(cls.violence_disorders, 'disorders')

    def setUp(self):
        self.generator = Generator.Generator(True)

    def test_init_classes(self):
        """Initializing the class should have grabbed the classes from the database"""
        self.assertEqual(self.generator.classes, [self.classes[0]])

    def test_init_packages(self):
        """Initializing the class should have grabbed the packages from the database"""
        self.assertEqual(self.generator.packages, [self.packages[0]])
