from threading import Thread

import random

import Lib.Mongo as Mongo

from Lib.Character import Character


class Generator(object):
    """
    Class that handles the actual character generation. It gets information from the project Mongo
    Database, uses this to instantiate a character, and contains functions for ensuring some
    character features get generated correctly.
    """
    def __init__(self):
        """
        Gets all information from the Mongo Database and uses it to instantiate a character class.
        """
        self.classes = []
        self.bonds = []
        self.packages = []
        self.skill_mapping = {}
        self.defaults = {}
        self.sub_skills = {}

        threads = [
            Thread(target=self._get_classes),
            Thread(target=self._get_packages),
            Thread(target=self._get_defaults),
            Thread(target=self._get_sub_skills),
            Thread(target=self._get_skill_mapping)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.character = Character(self.defaults, self.sub_skills, self.skill_mapping)

    def _get_classes(self):
        """
        Gets character classes from the database and appends them to the classes property.

        :return: None
        """
        self.classes = Mongo.find_all('classes')

    def _get_packages(self):
        """
        Gets packages from the database and appends them to the **packages** property.

        :return: None
        """
        self.packages = Mongo.find_all('packages')

    def _get_defaults(self):
        """
        Gets default skills from the database and appends them to the **defaults** property.

        :return: None
        """
        self.defaults = Mongo.find_one('default_stats')

    def _get_skill_mapping(self):
        """
        Gets skill mappings (which determine stat order) from the database and appends them to
        the **skill_mapping** property.

        :return: None
        """
        self.skill_mapping = Mongo.find_one('skill_mapping')

    def _get_sub_skills(self):
        """
        Gets a dictionary mapping sub-skill categories to their specific options from the database
        and appends them to the **sub_skills** property.

        :return: None
        """
        self.sub_skills = Mongo.find_one('sub_skills')

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

        self.bonds = Mongo.find_subset('bonds', {"Required": {"$in": required}})

    def random_character_class(self):
        """
        Randomly chooses a character class from among those it has access to (from the database) and
        applies it to the character object

        :return: None
        """
        class_obj = random.choice(self.classes)
        self.character.apply_class(class_obj)

    def random_character_package(self):
        """
        Randomly chooses a skill package from among those it has access to (from the database) and
        applies it to the character object

        :return: None
        """
        package = random.choice(self.packages)
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
            self.character.add_bond(random.choice(self.bonds))
            num_bonds -= 1

        for _ in range(num_bonds):
            bond_types = self.character.get_bond_types()
            all_types = all([bond_types[bond_type] for bond_type in bond_types])
            while True:
                proposed_bond = random.choice(self.bonds)
                if proposed_bond in self.character.bonds:
                    continue

                if all_types:
                    self.character.add_bond(proposed_bond)
                    break

                for bond_type in bond_types:
                    if proposed_bond[bond_type]:
                        proposed_bond_type = bond_type
                        break
                else:
                    continue

                if not self.character.has_bond_type(proposed_bond_type):
                    self.character.add_bond(proposed_bond)
                    break

    def generate(self):
        """
        Method that randomly generates a completed Delta Green character. Doesn't return anything,
        but the properties are accessible through the **character** property on this Class.

        :return: None
        """
        self.random_character_class()
        self.random_character_package()
        self._get_bonds()
        self.random_character_stats()
        self.random_character_bonds()
