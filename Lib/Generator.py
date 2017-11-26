"""
Handles generation of characters
"""

from threading import Thread

import Lib.Utilities.Mongo as Mongo

from Lib.Character import RandomCharacter
from ExternalServices import SAVE_LOCATION


class Generator(object):
    """
    Class that handles the actual character generation. It gets information from the project Mongo
    Database, uses this to instantiate a character, and contains functions for ensuring some
    character features get generated correctly.
    """
    def __init__(self, open_gaming_only=False):
        """
        Gets all information from the Mongo Database and uses it to instantiate a character class.

        :param bool open_gaming_only: If set to true, only OLG licensed or homebrew materials
            where the rights-holders have given me permission to use them will be used in the
            character.
        """
        self.open_gaming_only = open_gaming_only
        self.Mongo = Mongo
        self.classes = []
        self.bonds = []
        self.packages = []
        self.disorders = {
            "Violence": [],
            "Helplessness": [],
            "Unnatural": []
        }
        self.skill_mapping = {}
        self.defaults = {}
        self.sub_skills = {}

        threads = [
            Thread(target=self._get_classes),
            Thread(target=self._get_packages),
            Thread(target=self._get_defaults),
            Thread(target=self._get_violence_disorders),
            Thread(target=self._get_helplessness_disorders),
            Thread(target=self._get_unnatural_disorders),
            Thread(target=self._get_sub_skills),
            Thread(target=self._get_skill_mapping)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.character = RandomCharacter(self.defaults, self.sub_skills, self.skill_mapping)

    def _get_classes(self):
        """
        Gets character classes from the database and appends them to the classes property.

        :return: None
        """
        if self.open_gaming_only:
            self.classes = self.Mongo.find_subset('classes', {"open": True})
        else:
            self.classes = self.Mongo.find_all('classes')

    def _get_violence_disorders(self):
        """
        Gets all violence related disorders from the database.

        :return: None
        """
        self.disorders['Violence'] = self.Mongo.find_subset('disorders', {"Violence": True})

    def _get_helplessness_disorders(self):
        """
        Gets all helplessness related disorders from the database.

        :return: None
        """
        self.disorders['Helplessness'] = self.Mongo.find_subset('disorders', {"Helplessness": True})

    def _get_unnatural_disorders(self):
        """
        Gets all unnatural related disorders from the database.

        :return: None
        """
        self.disorders['Unnatural'] = self.Mongo.find_subset('disorders', {"Unnatural": True})

    def _get_packages(self):
        """
        Gets packages from the database and appends them to the **packages** property.

        :return: None
        """
        if self.open_gaming_only:
            self.packages = self.Mongo.find_subset('packages', {"open": True})
        else:
            self.packages = self.Mongo.find_all('packages')

    def _get_defaults(self):
        """
        Gets default skills from the database and appends them to the **defaults** property.

        :return: None
        """
        self.defaults = self.Mongo.find_one('default_stats')

    def _get_skill_mapping(self):
        """
        Gets skill mappings (which determine stat order) from the database and appends them to
        the **skill_mapping** property.

        :return: None
        """
        self.skill_mapping = self.Mongo.find_one('skill_mapping')

    def _get_sub_skills(self):
        """
        Gets a dictionary mapping sub-skill categories to their specific options from the database
        and appends them to the **sub_skills** property.

        :return: None
        """
        self.sub_skills = self.Mongo.find_one('sub_skills')

    def _get_bonds(self):
        """
        Gets bonds that are available to the character (based on the class and package) from the
        database and appends them to the **bonds** property.

        :return: None
        """
        required = [None]

        character_class = self.character.get_class()
        if character_class:
            required.append(character_class)

        character_package = self.character.get_package()
        if character_package:
            required.append(character_package)

        self.bonds = self.Mongo.find_subset('bonds', {"Required": {"$in": required}})

    def random_character_class(self):
        """
        Randomly chooses a character class from among those it has access to (from the database) and
        applies it to the character object

        :return: None
        """
        class_obj = self.character.random.choice(self.classes)
        self.character.apply_class(class_obj)

    def random_character_package(self):
        """
        Randomly chooses a skill package from among those it has access to (from the database) and
        applies it to the character object

        :return: None
        """
        package = self.character.random.choice(self.packages)
        self.character.apply_package(package)

    def random_character_stats(self):
        """
        Generates stats for the attached character and uses them to calculate derived attributes.

        :return: None
        """
        self.character.apply_stats()
        self.character.calculate_attributes()

    def random_character_bonds(self):
        """
        Uses the bonds it has on file as valid for the character class and the number of bonds the
        character class allows to create the correct number of bonds, well distributed across
        potential types of bonds.

        :return: None
        """
        num_bonds = self.character.num_bonds
        if num_bonds:
            self.character.add_bond(self.character.random.choice(self.bonds))
            num_bonds -= 1

        for _ in range(num_bonds):
            bond_types = self.character.get_bond_types()
            all_types = all([bond_types[bond_type] for bond_type in bond_types])
            while True:
                proposed_bond = self.character.random.choice(self.bonds)
                if proposed_bond in self.character.bonds:
                    continue

                if all_types:
                    self.character.add_bond(proposed_bond)
                    break

                for bond_type in bond_types:
                    if proposed_bond.get(bond_type, False):  # protects against missing properties
                        proposed_bond_type = bond_type
                        break
                else:
                    continue

                if not self.character.has_bond_type(proposed_bond_type):
                    self.character.add_bond(proposed_bond)
                    break

    def random_damaged_veteran(self):
        """
        Applies a random type of random veteran to the character. This is the last thing that
        should be applied to a character

        :return: None
        """
        types = ['Violence', 'Helpless', 'Unnatural', 'Hard Experience']
        damage_type = self.character.random.choice(types)

        if damage_type == 'Violence':
            self.character.damaged_veteran_violence()
        elif damage_type == 'Helpless':
            self.character.damaged_veteran_helplessness()
        elif damage_type == 'Unnatural':
            self.character.damaged_veteran_unnatural(self.disorders['Unnatural'])
        else:
            self.character.damaged_veteran_experience()

    def generate(self):
        """
        Method that randomly generates a completed Delta Green character. Returns a dictionary
        that contains all game relevant information about the character.

        :return: A dictionary with keys **Class**, **Package**, **Number_Bonds**, **Bonds** (here
            the name of the bond is mapped to the strength of the bond, an integer), **Lost_Bonds**
            (a simple list), **Veteran** (empty string if not a veteran) **Disorders** (empty list
            if none exist), **Adapted_To** (likewise empty if the character isn't adapted to
            violence or helplessness), **Attributes** (HP, WP, San, BP in dictionary format),
            **Stats**, and **Skills**
        :rtype: dict
        """
        self.random_character_class()
        self.random_character_package()
        self._get_bonds()
        self.random_character_stats()
        self.random_character_bonds()
        if self.character.random.randrange(0, 3) == 2:
            self.random_damaged_veteran()
        return self.character.get_character()

    def save_character(self):
        """
        Method for saving a character to the database. Returns the unique ID of the record the
        character is saved to.

        :return: A MongoDB ID, corresponding to the record in which the character is saved.
        :rtype: ObjectID
        """

        return self.character.save()
