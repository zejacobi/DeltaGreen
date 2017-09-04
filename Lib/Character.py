"""
Contains classes that represent characters, the transformations that can be applied to characters,
and functions for displaying created characters.
"""

import random
import copy
import operator
import math

import Lib.Utilities.Mongo as Mongo

from ExternalServices import SAVE_LOCATION
from Lib.Utilities.Exceptions import NotFoundError


class BaseCharacter(object):
    """
    Class that contains all important properties of a character and the methods for reading those.
    This class won't have any logic for setting or changing these; those show up in the
    specialized sub-classes.
    """

    def __init__(self):
        self.skills = {}
        self.num_bonds = 0
        self.bonds = []
        self.lost_bonds = []
        self.class_name = ''
        self.package_name = ''
        self.disorders = []
        self.adapted = {
            "Violence": False,
            "Helplessness": False
        }
        self.damaged_veteran = ''
        self.stats = {
            'Strength': 0,
            'Dexterity': 0,
            'Constitution': 0,
            'Intelligence': 0,
            'Power': 0,
            'Charisma': 0
        }

        self.hp = 0
        self.wp = 0
        self.sanity = 0
        self.bp = 0

    def __str__(self):
        """Gives a formatted plain text version of the character

        :return: A string giving all information needed to play the character
        :rtype: str
        """
        outstr = 'Class:                {}\n' \
                 'Skill package:        {}\n'.format(self.class_name, self.package_name)

        outstr += 'Damaged veteran type: {}\nDisorders:\n'.format(self.damaged_veteran)
        for disorder in self.disorders:
            outstr += '    {}\n'.format(disorder)

        outstr += '\nBonds:\n'

        for bond in self.get_bonds():
            outstr += '    {}: {}\n'.format(bond, self.stats['Charisma'])

        outstr += '\n'

        outstr += 'Lost bonds:\n'
        for bond in self.get_lost_bonds():
            outstr += '    {}\n'.format(bond)

        outstr += '\n'

        outstr += 'Adapted to:\n'
        for adaptation in self.get_adaptations():
            outstr += '    {}\n'.format(adaptation)

        outstr += '\nAttributes:\n' \
                  '    Hit Points:     {hp}\n' \
                  '    Willpower:      {wp}\n' \
                  '    Sanity:         {san}\n' \
                  '    Breaking Point: {bp}\n'.format(hp=self.hp, wp=self.wp, san=self.sanity,
                                                      bp=self.bp)

        outstr += '\nStats:\n' \
                  '    Strength:     {Strength}\n' \
                  '    Dexterity:    {Dexterity}\n' \
                  '    Constitution: {Constitution}\n' \
                  '    Intelligence: {Intelligence}\n' \
                  '    Power:        {Power}\n' \
                  '    Charisma:     {Charisma}\n\nSkills:\n'.format(**self.stats)

        for skill in sorted(self.skills.keys()):
            outstr += '    {}: {}\n'.format(skill, self.skills[skill])

        return outstr

    def get_skills(self):
        """
        Gives the dictionary containing all of the character's skills.

        :return: A dictionary with all skills, mapping to the value associated with this skill
        :rtype: dict
        """
        return self.skills

    def get_class(self):
        """
        Gives the character's class

        :return: The name of the class that the character has.
        :rtype: str
        """
        return self.class_name

    def get_package(self):
        """
        Gives the package that the character had applied to them

        :return: The name of the package the character has.
        :rtype: str
        """
        return self.package_name

    def get_stats(self):
        """
        Gives the character's stats

        :return: A dictionary mapping the six stats (Strength, Dexterity, Constitution,
            Intelligence, Wisdom, Charisma)
        :rtype: dict
        """
        return self.stats

    def get_attributes(self):
        """
        Gives the attributes derived from the characters stats

        :return: A dictionary mapping names of attributes to their integer values. Keys are:
            **Sanity**, **Hit Points**, **Willpower Points**, and **Breaking Point**
        :rtype: dict
        """
        return {
            'Sanity': self.sanity,
            'Hit Points': self.hp,
            'Willpower Points': self.wp,
            'Breaking Point': self.bp
        }

    def get_bonds(self):
        """
        Gives a list containing all bonds a character has

        :return: The names of all of the bonds the character has
        :rtype: list
        """
        return [bond["_id"] for bond in self.bonds]

    def get_lost_bonds(self):
        """
        Gives a list containing all bonds a character has lost.

        :return: The names of all of the bonds the character has lost.
        :rtype: list
        """
        return [bond["_id"] for bond in self.lost_bonds]

    def get_bond_types(self):
        """
        Gives a dictionary which maps the bond types to booleans that show if the character does or
        doesn't have a bond of that type.

        :return: A dict with keys **Family**, **Romantic**, **Friend**, **Work**, **Therapy**, all
            of which map to booleans
        :rtype: dict
        """
        types = {
            "Family": False,
            "Romantic": False,
            "Friend": False,
            "Work": False,
            "Therapy": False
        }
        for bond in self.bonds:
            for bond_type in types:
                types[bond_type] = types[bond_type] or bond[bond_type]

        return types

    def has_bond_type(self, bond_type):
        """
        Determines if the character already has a bond of that bond type.

        :param str bond_type: The name for the type of bond (one of: "Family", "Romantic",
            "Friend", "Work", "Therapy")
        :return: True if the character already has a bond of that type, false otherwise.
        :rtype: bool
        """
        types = self.get_bond_types()
        if bond_type in types:
            return types[bond_type]
        return False

    def get_disorders(self):
        """
        Gives a list containing all disorders the character has

        :return: The names of all of the disorders the character has picked up.
        :rtype: list
        """
        return self.disorders

    def get_adaptations(self):
        """Determines what type of sanity damage (if any) the character is already adapted to.

        :return: A list of which types of sanity damage a character is adapted to.
        :rtype: list
        """
        return [name for name in self.adapted.keys() if self.adapted[name]]

    def get_veteran_type(self):
        """
        Gives the type of damaged veteran that has been applied to the character, if any has.

        :return: The type of damaged veteran the character is
        :rtype: string
        """
        return self.damaged_veteran

    def get_character(self):
        """
        Gives a dictionary containing all game relevant information about the character.

        :return: A dictionary with keys **Class**, **Package**, **Number_Bonds**, **Bonds** (here
            the name of the bond is mapped to the strength of the bond, an integer), **Lost_Bonds**
            (a simple list), **Veteran** (empty string if not a veteran) **Disorders** (empty list
            if none exist), **Adapted_To** (likewise empty if the character isn't adapted to
            violence or helplessness), **Attributes** (HP, WP, San, BP in dictionary format),
            **Stats**, and **Skills**
        :rtype: dict
        """
        stats = self.get_stats()
        character = {
            'Class': self.class_name,
            'Package': self.package_name,
            'Number_Bonds': self.num_bonds,
            'Bonds': {bond: stats['Charisma'] for bond in self.get_bonds()},
            'Lost_Bonds': self.get_lost_bonds(),
            'Veteran': self.damaged_veteran,
            'Disorders': self.disorders,
            'Adapted_To': self.get_adaptations(),
            'Attributes': self.get_attributes(),
            'Stats': self.stats,
            'Skills': self.skills
        }
        return character


class RandomCharacter(BaseCharacter):
    """
    Class that contains functions for randomly generating a character. Subclasses BaseCharacter
    so that all character display methods only need to be implemented once.

    .. note::
        Note that there is a distinction made between Skills (which can only be taken once and are
        always the same) and sub-skills (which are a catch-all for a category of skills, such as
        Foreign Language and Craft; these can be taken multiple times picking a different
        sub-skill every time, such as Craft (Microelectronics) and Craft (Mechanic)). Understanding
        this distinction is important, because it comes up multiple times.

    :param dict default_skills: A dictionary containing all skills (except skills with
        associated sub-skills) and their default values
    :param dict sub_skills: A dictionary containing as keys all of the skills classified
        as sub-skills, mapped to lists of all sub-skill options for each
    :param dict skill_mappings: A dictionary that maps Skills with the stats that they're
        associated with. Used to give reasonable looking stats to each character.
    """
    def __init__(self, default_skills, sub_skills, skill_mappings):
        BaseCharacter.__init__(self)
        self.skills = copy.deepcopy(default_skills)
        self.defaults = default_skills
        self.sub_skills = sub_skills
        self.sub_skill_types = sub_skills.keys()
        self.skill_mappings = skill_mappings

        self.random = random  # this will make my life easier with unit testing

    @staticmethod
    def _get_subskill_str(skill, sub):
        """
        Generates a properly formatted skill string in the format <skill> (<sub>)

        :param str skill: The name of the primary skill
        :param str sub: The name of the sub-skill
        :return: the formatted skill name, comprised of the skill and subskill
        :rtype: str
        """
        return skill + ' (' + sub + ')'

    def roll_stat(self):
        """
        Does a classic 4d6 drop lowest roll, to be used as the value of a stat
        :return: An integer between 3 and 18
        :rtype: int
        """
        rolls = [self.random.randrange(1, 7) for _ in range(4)]
        return sum(sorted(rolls, reverse=True)[:3])

    def _get_random_sub_skill(self, skill):
        """
        Given a skill which is further broken down into sub-skills (e.g. Foreign Language),
        searches the record of available sub-skills and returns one of them at random

        :param str skill: A skill which has associated subskills (e.g. Craft, Foreign Language)

        :return: The name of one sub-skill under the aegis of the parent skill (e.g. Mechanic for
            Craft, French for Foreign Language)
        :rtype: str
        """
        choices = self.sub_skills[skill]
        return self.random.choice(choices)

    def _set_skill(self, skill, value):
        """
        Sets the provided skill to the provided value. If the skill has subcomponents (i.e.
        Foreign Language has the French, Spanish, etc. subcomponents), one of them will be chosen
        at random and the skill/sub-skill combo will be set to the provided value.

        :param str skill: The name of a skill
        :param int value: The number to set the skill to
        :return: True (if a skill was successfully set to the desired value) or False (if no skill
            could be set to the desired value)
        :rtype: bool
        """
        if skill in self.skills:
            self.skills[skill] = value
            return True
        elif skill in self.sub_skill_types:
            self._set_skill(self._add_random_sub_skill(skill), value)
            return True
        return False

    def _add_sub_skill(self, skill, sub):
        """
        Generates the display string for a sub-skill ("Foreign Language", "French" becomes
        "Foreign Language (French)") and adds it the **skills** property of the character class,
        with a starting value of 0. If no *sub* value provided, one will be chosen at random.
        If a sub-skill is chosen at random, it will specifically be one that isn't already use.

        :param str skill: A skill which has associated subskills (e.g. Craft, Foreign Language)
        :param str sub: name of one sub-skill under the aegis of the parent skill (e.g. Mechanic for
            Craft, French for Foreign Language), or a falsey value for a random sub-skill to be
            chosen instead of a specific sub-skill.
        :return: The display string for the sub-skill
        :rtype: str
        """
        if not sub:
            return self._add_random_sub_skill(skill)
        string = self._get_subskill_str(skill, sub)
        if string not in self.skills:
            self.skills[string] = 0
        return string
    
    def _set_sub_skill(self, skill, sub, value):
        """
        Convenience function for setting a sub-skill to a certain value. It adds the skill/sub-skill
        to the list of skills (randomly generating a sub-skill if none passed) and then sets that
        specific skill to the provided value.

        :param str skill: A skill which has associated subskills (e.g. Craft, Foreign Language)
        :param str sub: name of one sub-skill under the aegis of the parent skill (e.g. Mechanic for
            Craft, French for Foreign Language), or a falsey value for a random sub-skill to be
            chosen instead of a specific sub-skill.
        :param int value: The number to set the sub-skill to
        :return: True (if a skill was successfully set to the desired value) or False (if no skill
            could be set to the desired value)
        :rtype: bool
        """
        return self._set_skill(self._add_sub_skill(skill, sub), value)

    def _add_random_sub_skill(self, skill, novel=True):
        """
        Adds a random sub-skill to the character (setting it to 0 in the process).

        :param str skill: A skill which has associated subskills (e.g. Craft, Foreign Language)
        :param bool novel: If true, then the potential sub-skill will be generated and regenerated
            until one not already in the character's skill list is found.

        :return: The display string (e.g. "Foreign Language (French)") for the sub-skill
        :rtype: str
        """
        choice = self._get_random_sub_skill(skill)
        string = self._get_subskill_str(skill, choice)
        if novel:
            while string in self.skills:
                choice = self._get_random_sub_skill(skill)
                string = self._get_subskill_str(skill, choice)
        self._add_sub_skill(skill, choice)
        return string

    def _safe_set_skill(self, skill, sub, value):
        """
        Safely sets a skill or a sub-skill to the requested value. "Safely" means this function
        will only modify skills that are set to their default value. It won't overwrite any skills
        that have already been modified.

        :param str skill: A skill which may or may not have associated subskills (e.g. *"Craft"*,
            *"Foreign Language"* have associated sub-skills, "Swim" does not)
        :param str sub: name of one sub-skill under the aegis of the parent skill (e.g. Mechanic for
            Craft, French for Foreign Language), or a falsey value for a random sub-skill to be
            chosen instead of a specific sub-skill. If the *skill* parameter isn't a sub-skill,
            this will be ignored
        :param int value: The number to set the skill/sub-skill to
        :return: True (if a skill was successfully set to the desired value) or False (if no skill
            could be set to the desired value, or if the skill has already been modified)
        :rtype: bool
        """
        if not sub:
            if skill in self.skills:
                if self.skills[skill] == self.defaults[skill]:
                    self._set_skill(skill, value)
                    return True
                return False
            else:
                return self._set_skill(skill, value)
        else:
            string = self._get_subskill_str(skill, sub)
            if string in self.skills:
                if self.skills[string] == 0:
                    self._set_skill(string, value)
                    return True
                return False
            else:
                self._set_sub_skill(skill, sub, value)
                return True

    def apply_class(self, class_obj):
        """
        Applies a class to this character. Classes are defined in dictionaries. For an example of
        what these classes look like, see `OpenGamingJSON/classes.json`. Applying a class sets
        many skills to non-default values and sets the number of bonds.

        :param class_obj: A dictionary containing the keys **_id** (the class name),
            **Skills** (a dictionary mapping skills to their starting value), **Choices** (a
            dictionary with keys **Skills**, **Number** and sometimes **Subskills**, which is
            used when a class is allowed to choose one from a number of skills), **Subskills**
            (an array of dictionaries; each inner one contains the keys **Skill**, **Sub**, and
            **Value** - which are used to set up skills the character class gets when sub-skills
            like Craft (Microelectronics) are specified in the class description, or when a
            skill with sub-skills is included multiple times in the class), and **Bonds** (the
            number of bonds the character class gets)
        :return: None
        :rtype: None
        """
        skills = class_obj['Skills']
        sub_skills = class_obj['Subskills']
        self.num_bonds = class_obj['Bonds']
        self.class_name = class_obj['_id']

        for skill in skills:
            self._set_skill(skill, skills[skill])
        
        for obj in sub_skills:
            self._set_sub_skill(obj['Skill'], obj['Sub'], obj['Value'])

        choices = class_obj['Choices']
        skill_choices = choices['Skills']
        num_choices = choices['Number']

        if num_choices:
            skill_list = list(skill_choices.keys())
            if 'Subskills' in choices:
                choice_sub_skills = choices['Subskills']
                sample_list = [False for _ in skill_list]
                sample_list.extend(choice_sub_skills)
                for tf in self.random.sample(sample_list, num_choices):
                    # picks a fair amount of sub-skills, proportional to the number there are
                    if tf:
                        num_choices -= 1
                        self._safe_set_skill(tf['Skill'], tf['Sub'], tf['Value'])
            if num_choices:
                for skill in self.random.sample(skill_list, num_choices):
                    self._safe_set_skill(skill, '', skill_choices[skill])

    def _add_to_skill(self, skill, addition, novel_sub_skill=True):
        """
        Adds a set value to a skill. If the skill is one that has sub-skills, it picks a random
        sub-skill to add the value to. If the bool *novel_sub_skill* is True, this skill will be
        one that the character doesn't already have. Otherwise it *might* be added to a skill the
        character already has.

        :param str skill: The name of a skill or sub-skill
        :param int addition: The amount to add to the skill or sub-skill
        :param bool novel_sub_skill: If True and the *skill* parameter is a sub-skill, then the
            amount will be added to a new sub-skill that the character doesn't already have
        :return: True if the value was successfully added to the desired skill/one of its
            sub-skills, false otherwise
        :rtype: bool
        """
        if skill in self.skills:
            self.skills[skill] += addition
            return True
        elif skill in self.sub_skill_types:
            self._add_to_skill(self._add_random_sub_skill(skill, novel_sub_skill), addition)
            return True
        return False

    def _add_to_sub_skill(self, skill, sub, addition, novel_sub_skill=False):
        """
        Adds a set value to a skill that has sub-skills. If *sub* is falsey, it picks a random
        sub-skill to add the value to. If the bool *novel_sub_skill* is True, this skill will be
        one that the character doesn't already have. Otherwise it *might* be added to a skill the
        character already has. Defaults to leaving the option open on an existing skill.

        :param str skill: A skill which may or may not have associated subskills (e.g. *"Craft"*,
            *"Foreign Language"* have associated sub-skills, "Swim" does not)
        :param str sub: name of one sub-skill under the aegis of the parent skill (e.g. Mechanic for
            Craft, French for Foreign Language), or a falsey value for a random sub-skill to be
            chosen instead of a specific sub-skill.
        :param int addition: The amount to add to the skill or sub-skill
        :param bool novel_sub_skill: If True and the *skill* parameter is a sub-skill, then the
            amount will be added to a new sub-skill that the character doesn't already have
        :return: True if the value was successfully added to the desired skill/one of its
            sub-skills, false otherwise
        :rtype: bool
        """
        if sub:
            string = self._get_subskill_str(skill, sub)
            if string in self.skills:
                return self._add_to_skill(string, addition)
            else:
                return self._add_to_skill(self._add_sub_skill(skill, sub), addition)
        else:
            return self._add_to_skill(skill, addition, novel_sub_skill=novel_sub_skill)

    def add_package_skill(self, skill, sub):
        """
        Takes advantage of the fact that package skills are always +20 to simplify the process of
        adding them. Works for equally well for skill, fully defined sub-skills, or the category of
        a sub-skill where a random choice of specific sub-skill is necessary

        :param str skill: The name of a skill or sub-skill category
        :param str sub: Optional parameter; used when you wish to define a sub-skill precisely.
        :return: True if the skill was successfully added, false otherwise
        :rtype: bool
        """
        if sub:
            return self._add_to_sub_skill(skill, sub, 20)
        else:
            return self._add_to_skill(skill, 20, False)

    def apply_package(self, package):
        """
        Applies a package (normally 8 skills that each get +20) to a character. Also sets the
        **package_name** property on the character.

        :param dict package: A dictionary with keys **Skills**, **Subskills** and **Choices**.
            This is similar to the character dictionary, but there are no values involved and the
            **Skills** top level key maps to an array.
        :return: None
        :rtype: None
        """
        skills = package['Skills']
        sub_skills = package['Subskills']
        self.package_name = package['_id']

        for skill in skills:
            self.add_package_skill(skill, '')

        for obj in sub_skills:
            self.add_package_skill(obj['Skill'], obj['Sub'])
        
        choices = package['Choices']
        skill_choices = choices['List']
        all_skills = choices['All']
        num_choices = choices['Number']
        if num_choices:
            if all_skills:
                skill_choices = list(self.skills.keys())
                skill_choices.remove('Unnatural')  # Can't improve this through normal channels
            self.random.shuffle(skill_choices)
            for skill in skill_choices[:num_choices]:
                self.add_package_skill(skill, '')

    def set_stat(self, stat, value):
        """
        Sets a stat (Strength, Dexterity, Constitution, Intelligence, Power, Charisma) to a value.

        :param str stat: The name of the stat. Has to be one of the ones enumerated above.
        :param int value: The value to set the stat to. Should be between 3 and 18.
        :return: True if the stat was successfully set to the value, false otherwise.
        :rtype: bool
        """
        if stat in self.stats:
            self.stats[stat] = value
            return True
        return False

    def apply_stats(self, floor=68):
        """
        Generates stats using 4d6 drop lowest
        and applies them, with the best stats going to where the program thinks the character
        should be best. This is based off of skills (with some weighting given to game useful
        qualities, to ensure characters aren't weak)

        :param int floor: The minimum allowable sum of all of the randomly generated statistics.
            Having this set to a value significantly increases the strength of a character (although
            this effect is less pronounced for values less than 65 and practically non-existent
            below 60). Set to 0 for the hardcore gamer cred of taking whatever the dice gives you.
        :return: None
        :rtype: None
        """
        best_skills = sorted(self.skills.items(), key=operator.itemgetter(1), reverse=True)[:5]
        stat_count = {
            'Power': 2,  # San, Willpower
            'Strength': 1,  # 1/2 HP
            'Constitution': 1,  # 1/2 HP,
            'Dexterity': 0.5,  # Initiative
            'Intelligence': 0,  # Practically every skill gives this anyway
            'Charisma': self.num_bonds * 2 / 3  # Bond strength (2/3 to be a good modifier)
        }
        observed_stats = []
        for skill, _ in best_skills:
            if skill in self.skill_mappings:
                observed_stats.extend(self.skill_mappings[skill])
            else:
                for skill_type in self.sub_skill_types:
                    if skill_type in skill:
                        observed_stats.extend(self.skill_mappings[skill_type])
                        break

        for stat in observed_stats:
            stat_count[stat] += 1

        die_rolls = sorted([self.roll_stat() for _ in range(6)], reverse=True)
        if floor:
            while sum(die_rolls) < floor:
                die_rolls = sorted([self.roll_stat() for _ in range(6)], reverse=True)
        stat_order = sorted(stat_count.items(), key=operator.itemgetter(1), reverse=True)
        self.stats = {stat[0]: die_rolls[i] for i, stat in enumerate(stat_order)}

    def calculate_attributes(self):
        """
        Uses the stats (Str, Dex, Con, Int, Pow, Cha) to calculate the four derived attributes:
        Sanity, Hit Points, Willpower Points and Breaking Point.

        :return: None
        :rtype: None
        """
        self.hp = int(math.ceil(self.stats['Strength']/2 + self.stats['Constitution']/2))
        self.wp = self.stats['Power']
        self.sanity = self.stats['Power'] * 5
        self.bp = self.stats['Power'] * 4

    def add_bond(self, bond):
        """
        Adds a bond to the character's list of bonds

        :param dict bond: A dictionary with parameters **_id** (the bond's name), **Required**
            (an array listing any package or class requirements for having the bond), and the
            classes of bond (**Family**, **Romantic**, **Friend**, **Work**, **Therapy**),
            booleans which are used to ensure an even and reasonable distribution of bonds.

        :return: None
        :rtype: None
        """
        self.bonds.append(bond)

    def damaged_veteran_violence(self):
        """
        Applies the damaged veteran template "Extreme Violence", lowering Charisma and Sanity
        but increasing skill with Occult and adapting the agent to violence.

        :return: None
        :rtype: None
        """
        if self.damaged_veteran:
            return None
        self._add_to_skill('Occult', 10)
        self.sanity -= 5
        self.stats['Charisma'] -= 3
        self.adapted['Violence'] = True
        self.damaged_veteran = 'Extreme Violence'

    def damaged_veteran_helplessness(self):
        """
        Applies the damaged veteran template "Captivity or Imprisonment", lowering Power and Sanity
        but increasing skill with Occult and adapting the agent to helplessness.

        :return: None
        :rtype: None
        """
        if self.damaged_veteran:
            return None
        self._add_to_skill('Occult', 10)
        self.sanity -= 5
        self.stats['Power'] -= 3
        self.adapted['Helplessness'] = True
        self.damaged_veteran = 'Captivity or Imprisonment'

    def damaged_veteran_experience(self):
        """
        Applies the damaged veteran template "Hard Experience", lowering the number of bonds and
        Sanity but increasing skill five skills (one of which must be Occult)

        :return: None
        :rtype: None
        """
        if self.damaged_veteran:
            return None
        self._add_to_skill('Occult', 10)
        self.sanity -= 5
        self.damaged_veteran = 'Hard Experience'
        self.lost_bonds.append(self.bonds.pop())
        self.num_bonds -= 1
        plausible_skills = ["Alertness", "Athletics", "Bureaucracy", "Computer Science",
                            "Criminology", "Demolitions", "Dodge", "Drive", "Firearms",
                            "First Aid", "Forensics", "Heavy Machinery", "Heavy Weapons", "History",
                            "HUMINT", "Law", "Melee Weapons", "Navigate", "Occult", "Persuade",
                            "Pharmacy", "Psychotherapy", "Search", "Stealth", "Survival",
                            "Unarmed Combat"]
        skills = self.random.sample(plausible_skills, 4)

        for skill in skills:
            self._add_to_skill(skill, 10)

    def damaged_veteran_unnatural(self, disorders):
        """
        Applies the damaged veteran template "Things Man Was Not Meant to Know", breaking the agent
        (giving them a disorder and lowered sanity), but giving them a hefty boost to their
        occult skill and giving them a starting unnatural score. Can only be applied as the first
        type of damaged veteran.

        :param list disorders: A list of disorders. One will be chosen from the list. Disorders
            are displayed using their "_id" property, which should contain their name.

        :return: None
        :rtype: None
        """
        if self.damaged_veteran:
            return None
        self._add_to_skill('Occult', 20)
        self._add_to_skill('Unnatural', 10)
        self.sanity -= self.stats['Power']
        self.bp -= self.stats['Power']
        disorder = self.random.choice(disorders)
        self.add_disorder(disorder)
        self.damaged_veteran = 'Things Man Was Not Meant to Know'

    def add_disorder(self, disorder):
        """
        Strips away all chafe attached to a disorder object and just puts the name into the
        list of the character's disorders

        :param dict disorder: A dict containing information about the disorder, with an "_id"
            property that gives the name of the disorder

        :return: None
        :rtype: None
        """
        self.disorders.append(disorder['_id'])


class LoadedCharacter(BaseCharacter):
    """
    Class that loads an existing character into the BaseCharacter class so that it can be displayed.
    Raises NotFoundError if the character cannot be found in the database.

    :param str character_id: The unique ID of the character. This is set by MongoDB and is how we
        find the character in the database.

    :raises: NotFoundError
    """
    def __init__(self, character_id):
        BaseCharacter.__init__(self)
        self.Mongo = Mongo

        character = self.Mongo.find_by_id(SAVE_LOCATION, character_id)

        if not character:
            raise NotFoundError('Could not find character with ID {0!s}'.format(character_id))

        self.skills = character['Skills']
        self.num_bonds = character['Number_Bonds']
        self.bonds = [{"_id": bond} for bond in character['Bonds'].keys()]
        self.lost_bonds = [{"_id": bond} for bond in character['Lost_Bonds']]
        self.class_name = character['Class']
        self.package_name = character['Package']
        self.disorders = character['Disorders']
        self.adapted = {
            "Violence": "Violence" in character['Adapted_To'],
            "Helplessness": "Helplessness" in character['Adapted_To'],
        }
        self.damaged_veteran = character['Veteran']
        self.stats = character['Stats']
        self.hp = character['Attributes']['Hit Points']
        self.bp = character['Attributes']['Breaking Point']
        self.wp = character['Attributes']['Willpower Points']
        self.sanity = character['Attributes']['Sanity']

