import random
import copy


class Character(object):
    def __init__(self, default_skills, sub_skills):
        self.skills = copy.deepcopy(default_skills)
        self.defaults = default_skills
        self.sub_skills = sub_skills
        self.sub_skill_types = sub_skills.keys()

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

    def add_to_skill(self, skill, addition):
        if skill in self.skills:
            self.skills[skill] += addition
            return True
        elif skill in self.sub_skill_types:
            self.add_to_skill(self.add_random_sub_skill(skill), addition)
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

    def get_skills(self):
        return self.skills
