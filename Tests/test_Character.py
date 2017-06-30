import unittest

from Lib.Character import Character
from Tests.RandomMock import RandomMock


class TestCharacter(unittest.TestCase):
    """Test the JSON parsing"""
    @classmethod
    def setUpClass(cls):
        cls.skills = {
            "Accounting": 10,
            "Alertness": 20,
            "Anthropology": 0,
            "Archeology": 0,
            "Artillery": 0,
            "Unnatural": 0
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
        self.assertEqual(self.character._set_skill(self.skill_names[0], 30), True)
        self.assertEqual(self.character.skills[self.skill_names[0]], 30)

    def test_private_set_skill_not_found(self):
        """Tests that trying to set the value of a non-existent skill returns false"""
        self.assertEqual(self.character._set_skill('Nonexistent', 30), False)

    def test_private_set_skill_with_a_subskill(self):
        """Tests that setting an accessible sub-skill returns true and sets a random sub-skill to the
        provided value"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        self.assertEqual(self.character._set_skill(self.sub_skill_names[0], 30), True)
        self.assertEqual(self.character.skills[
            self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'], 30)

    def test_private_add_sub_skill(self):
        """Tests that it will add a new skill, set to 0"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        str = skill + ' (' + sub + ')'
        self.assertEqual(self.character._add_sub_skill(skill, sub), str)
        self.assertEqual(self.character.skills[str], 0)

    def test_private_add_sub_skill_with_existing(self):
        """Tests that it will return the skill string without affecting the value when the skill has
        already been added to the list"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        str = skill + ' (' + sub + ')'
        starting_value = 50
        self.character.skills[str] = starting_value
        self.assertEqual(self.character._add_sub_skill(skill, sub), str)
        self.assertEqual(self.character.skills[str], starting_value)

    def test_private_add_sub_skill_at_random(self):
        """Tests that a random sub-skill will be added if a specific one isn't provided"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        self.assertEqual(self.character._add_sub_skill(self.sub_skill_names[0], ''),
                         self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')')
        self.assertEqual(self.character.skills[
            self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'], 0)

    def test_private_set_sub_skill(self):
        """Tests that it will add a new skill, set to the provided value"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        expected_str = skill + ' (' + sub + ')'
        value = 50
        self.assertEqual(self.character._set_sub_skill(skill, sub, value), True)
        self.assertEqual(self.character.skills[expected_str], value)

    def test_private_set_sub_skill_with_existing(self):
        """Tests that it will set the sub-skill to the provided value"""
        skill = 'Foreign Language'
        sub = 'Spanish'
        expected_str = skill + ' (' + sub + ')'
        starting_value = 50
        new_value = 70
        self.character.skills[expected_str] = starting_value
        self.assertEqual(self.character._set_sub_skill(skill, sub, new_value), True)
        self.assertEqual(self.character.skills[expected_str], new_value)

    def test_private_set_sub_skill_at_random(self):
        """Tests that a random sub-skill will be added if a specific one isn't provided"""
        value = 50
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        self.assertEqual(self.character._set_sub_skill(self.sub_skill_names[0], '', value), True)
        self.assertEqual(self.character.skills[
            self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'], value)

    def test_private_add_random_sub_skill(self):
        """Tests that this will return a string incorporating a random sub-skill and add it to the
        character"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        expected_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'
        self.assertEqual(self.character._add_random_sub_skill(self.sub_skill_names[0]),
                         expected_str)
        self.assertEqual(self.character.skills[expected_str], 0)

    def test_private_add_random_sub_skill_novel_false(self):
        """Tests that this will return a string incorporating a random sub-skill and not overwrite it
        if it already exists (this requires the novel kwarg to be false, otherwise a different
        skill would be chose)."""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        expected_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'
        starting_value = 50
        self.character.skills[expected_str] = starting_value
        self.assertEqual(self.character._add_random_sub_skill(self.sub_skill_names[0], False),
                         expected_str)
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
        self.assertEqual(self.character._add_random_sub_skill(self.sub_skill_names[0]), new_str)
        self.assertEqual(self.character.skills[existing_str], starting_value)
        self.assertEqual(self.character.skills[new_str], 0)
        self.assertEqual(self.random_mock.choice_state, len(self.random_mock.choice_list) - 1)

    def test_private_safe_set_skill(self):
        """Test that it can set an ordinary skill still at its default value to another value"""
        self.assertEqual(self.character._safe_set_skill(self.skill_names[0], '', 60), True)
        self.assertEqual(self.character.skills[self.skill_names[0]], 60)

    def test_private_safe_set_already_set(self):
        """Test that it won't overwrite an already set skill value"""
        value = 55
        self.character.skills[self.skill_names[0]] = value
        self.assertEqual(self.character._safe_set_skill(self.skill_names[0], '', 60), False)
        self.assertEqual(self.character.skills[self.skill_names[0]], value)

    def test_private_safe_set_skill_random_sub_skill(self):
        """Test that if provided a sub-skill type skill without the specific sub-skill specified, it
        will pick and set one at random"""
        self.random_mock.choice_list = [self.sub_skills[self.sub_skill_names[0]][0]]
        expected_str = self.sub_skill_names[0] + ' (' + self.random_mock.choice_list[0] + ')'
        self.assertEqual(self.character._safe_set_skill(self.sub_skill_names[0], '', 60), True)
        self.assertEqual(self.character.skills[expected_str], 60)

    def test_private_safe_set_skill_new_sub_skill(self):
        """Test that if provided a skill and sub-skill and the sub-skill is new, that it returns true
        and set the sub-skill to the provided value"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.assertEqual(self.character._safe_set_skill(skill, sub, 60), True)
        self.assertEqual(self.character.skills[expected_str], 60)

    def test_private_safe_set_skill_existing_sub_skill(self):
        """Test that if provided a skill and sub-skill and the sub-skill exists but is still 0, that
        it return true and set the sub-skill to the provided value"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.character.skills[expected_str] = 0
        self.assertEqual(self.character._safe_set_skill(skill, sub, 60), True)
        self.assertEqual(self.character.skills[expected_str], 60)

    def test_private_safe_set_skill_existing_sub_skill_with_value(self):
        """Test that if provided a skill and sub-skill and the sub-skill exists and is not 0, that
        it returns false and leaves the sub-skill alone"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        starting_value = 30
        self.character.skills[expected_str] = starting_value
        self.assertEqual(self.character._safe_set_skill(skill, sub, 60), False)
        self.assertEqual(self.character.skills[expected_str], starting_value)

    def test_private_add_to_skill(self):
        """Tests that it can add to an already existing skill"""
        starting_value = self.character.skills[self.skill_names[0]]
        self.assertEqual(self.character._add_to_skill(self.skill_names[0], 20), True)
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
        self.assertEqual(self.character._add_to_skill(skill, 20), True)
        self.assertEqual(self.character.skills[expected_str], 20)

    def test_private_add_to_skill_with_sub_skill_existing_but_not_novel(self):
        """Tests that it can add to a sub skill if it already exists but novel is false"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.character.skills[expected_str] = 20
        self.random_mock.choice_list = [sub]
        self.assertEqual(self.character._add_to_skill(skill, 20, False), True)
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
        self.assertEqual(self.character._add_to_skill(skill, 20), True)
        self.assertEqual(self.character.skills[original_string], 20)
        self.assertEqual(self.character.skills[new_string], 20)
        self.assertEqual(self.random_mock.choice_state, len(self.random_mock.choice_list) - 1)

    def test_private_add_to_sub_skill(self):
        """Tests that it can add to an already existing sub-skill"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        starting_value = 20
        self.character.skills[expected_str] = starting_value
        self.assertEqual(self.character._add_to_sub_skill(skill, sub, 20), True)
        self.assertEqual(self.character.skills[expected_str], starting_value + 20)

    def test_private_add_to_sub_skill_with_new_sub_skill(self):
        """Tests that it can add a sub skill and add the provided value to 0"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.assertEqual(self.character._add_to_sub_skill(skill, sub, 20), True)
        self.assertEqual(self.character.skills[expected_str], 20)

    def test_private_add_to_sub_skill_with_sub_skill_existing_but_not_novel(self):
        """Tests that it will add to the first randomly chosen sub-skill if that skill already
        exists and novel is false"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.character.skills[expected_str] = 20
        self.random_mock.choice_list = [sub]
        self.assertEqual(self.character._add_to_sub_skill(skill, '', 20), True)
        self.assertEqual(self.character.skills[expected_str], 40)
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
        self.assertEqual(self.character._add_to_sub_skill(skill, '', 20, True), True)
        self.assertEqual(self.character.skills[original_string], 20)
        self.assertEqual(self.character.skills[new_string], 20)
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
        self.assertEqual(self.character.num_bonds, class_obj['Bonds'])
        self.assertEqual(self.character.class_name, class_obj['_id'])
        self.assertEqual(self.character.skills['Anthropology'], 40)
        self.assertEqual(self.character.skills['Archeology'], 40)
        self.assertEqual(self.character.skills['Artillery'], 0)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[0] + ')'],
                         50)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[1] + ')'],
                         40)

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
        self.assertEqual(self.character.num_bonds, class_obj['Bonds'])
        self.assertEqual(self.character.class_name, class_obj['_id'])
        self.assertEqual(self.character.skills['Anthropology'], 40)
        self.assertEqual(self.character.skills['Archeology'], 40)
        self.assertEqual(self.character.skills['Artillery'], 40)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[0] + ')'],
                         50)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[1] + ')'],
                         40)

    def test_apply_class_repeated_choices(self):
        """Tests that applying a class with overlap between set sub-skills and random sub-skills
        chosen as a choice will result in repeated attempts to find a workable random sub-skill"""
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
        self.assertEqual(self.character.num_bonds, class_obj['Bonds'])
        self.assertEqual(self.character.class_name, class_obj['_id'])
        self.assertEqual(self.character.skills['Anthropology'], 40)
        self.assertEqual(self.character.skills['Archeology'], 40)
        self.assertEqual(self.character.skills['Artillery'], 40)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[0] + ')'],
                         50)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[1] + ')'],
                         40)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[-1] + ')'],
                         60)
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
        self.assertEqual(self.character.num_bonds, class_obj['Bonds'])
        self.assertEqual(self.character.class_name, class_obj['_id'])
        self.assertEqual(self.character.skills['Anthropology'], 40)
        self.assertEqual(self.character.skills['Archeology'], 40)
        self.assertEqual(self.character.skills['Artillery'], 40)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[0] + ')'],
                         50)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[1] + ')'],
                         40)

    def test_apply_class_sub_skills_chosen(self):
        """Tests that applying a class with skill choices and sub-skill choices will replace any
        skills that might be applied with subskills if subskills are chosen"""
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
        self.assertEqual(self.character.num_bonds, class_obj['Bonds'])
        self.assertEqual(self.character.class_name, class_obj['_id'])
        self.assertEqual(self.character.skills['Anthropology'], 40)
        self.assertEqual(self.character.skills['Archeology'], 40)
        self.assertEqual(self.character.skills['Artillery'], 0)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[0] + ')'],
                         50)
        self.assertEqual(self.character.skills['Foreign Language (' + language_choices[1] + ')'],
                         40)
        self.assertEqual(
            self.character.skills['Art (' + class_obj['Choices']['Subskills'][0]['Sub'] + ')'], 40)

    def test_add_package_skill_normal_skill(self):
        """Tests that it will return true and apply +20 to a normal skill"""
        starting = self.character.skills[self.skill_names[0]]
        self.assertEqual(self.character.add_package_skill(self.skill_names[0], ''), True)
        self.assertEqual(self.character.skills[self.skill_names[0]], starting + 20)

    def test_add_package_skill_sub_skill(self):
        """Tests that it will return true and apply +20 to a sub-skill with the specific type
        given"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.assertEqual(self.character.add_package_skill(skill, sub), True)
        self.assertEqual(self.character.skills[expected_str], 20)

    def test_add_package_skill_random_sub_skill(self):
        """Tests that it will return true and apply +20 to a sub-skill with a random type given"""
        skill = self.sub_skill_names[0]
        sub = self.sub_skills[skill][0]
        expected_str = skill + ' (' + sub + ')'
        self.random_mock.choice_list = [sub]
        self.assertEqual(self.character.add_package_skill(skill, ''), True)
        self.assertEqual(self.character.skills[expected_str], 20)