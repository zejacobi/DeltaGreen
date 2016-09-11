import random
import copy


class Character(object):
    def __init__(self, default_skills, sub_skills):
        self.skills = copy.deepcopy(default_skills)
        self.defaults = default_skills
        self.sub_skills = sub_skills
        self.sub_skill_types = sub_skills.keys()
        self.bonds = 0
        self.class_name = ''
        self.package_name = ''

    @staticmethod
    def get_subskill_str(skill, sub):
        return skill + ' (' + sub + ')'

    def get_random_sub_skill(self, skill):
        choices = self.sub_skills[skill]
        return random.choice(choices)

    def set_skill(self, skill, value):
        if skill in self.skills:
            self.skills[skill] = value
            return True
        elif skill in self.sub_skill_types:
            self.set_skill(self.add_random_sub_skill(skill), value)
            return True
        return False

    def add_sub_skill(self, skill, sub):
        if not sub:
            return self.add_random_sub_skill(skill)
        string = self.get_subskill_str(skill, sub)
        if string not in self.skills:
            self.skills[string] = 0
        return string
    
    def set_sub_skill(self, skill, sub, value):
        return self.set_skill(self.add_sub_skill(skill, sub), value)

    def add_random_sub_skill(self, skill, novel=True):
        choice = self.get_random_sub_skill(skill)
        string = self.get_subskill_str(skill, choice)
        if novel:
            while string in self.skills:
                choice = self.get_random_sub_skill(skill)
                string = self.get_subskill_str(skill, choice)
        self.add_sub_skill(skill, choice)
        return string

    def safe_set_skill(self, skill, sub, value):
        if not sub:
            if skill in self.skills:
                if self.skills[skill] == self.defaults[skill]:
                    self.set_skill(skill, value)
                    return True
                return False
            else:
                return self.set_skill(skill, value)
        else:
            string = self.get_subskill_str(skill, sub)
            if string in self.skills:
                if self.skills[string] == 0:
                    self.set_skill(string, value)
                    return True
                return False
            else:
                self.set_sub_skill(skill, sub, value)
                return True

    def apply_class(self, class_obj):
        skills = class_obj['Skills']
        sub_skills = class_obj['Subskills']
        self.bonds = class_obj['Bonds']
        self.class_name = class_obj['_id']

        for skill in skills:
            self.set_skill(skill, skills[skill])
        
        for obj in sub_skills:
            self.set_sub_skill(obj['Skill'], obj['Sub'], obj['Value'])

        choices = class_obj['Choices']
        skill_choices = choices['Skills']
        num_choices = choices['Number']

        if num_choices:
            skill_list = list(skill_choices.keys())
            random.shuffle(skill_list)
            for skill in skill_list[:num_choices]:
                success = self.safe_set_skill(skill, '', skill_choices[skill])
                while success is not True:
                    success = self.safe_set_skill(skill, '', skill_choices[skill])

    def add_to_skill(self, skill, addition, novel_sub_skill=True):
        if skill in self.skills:
            self.skills[skill] += addition
            return True
        elif skill in self.sub_skill_types:
            self.add_to_skill(self.add_random_sub_skill(skill, novel_sub_skill), addition)
            return True
        return False

    def add_to_sub_skill(self, skill, sub, addition, novel_sub_skill=False):
        if sub:
            string = self.get_subskill_str(skill, sub)
            if string in self.skills:
                return self.add_to_skill(string, addition)
            else:
                return self.add_to_skill(self.add_sub_skill(skill, sub), addition)
        else:
            return self.add_to_skill(skill, addition, novel_sub_skill=novel_sub_skill)

    def add_package_skill(self, skill, sub):
        if sub:
            return self.add_to_sub_skill(skill, sub, 20)
        else:
            return self.add_to_skill(skill, 20)

    def apply_package(self, package):
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
            for skill in skill_choices[:num_choices]:
                success = self.add_package_skill(skill, '')
                while success is not True:
                    success = self.add_package_skill(skill, '')

    def get_skills(self):
        return self.skills

    def get_class(self):
        return self.class_name

    def get_package(self):
        return self.package_name
