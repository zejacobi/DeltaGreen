import random


class Character(object):
    def __init__(self, default_skills, sub_skills):
        self.skills = default_skills
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

    def add_to_skill(self, skill, addition):
        if skill in self.skills:
            self.skills[skill] += addition

    def add_sub_skill(self, skill, sub):
        string = self.get_subskill_str(skill, sub)
        if string not in self.skills:
            self.skills[string] = 0

    def add_random_sub_skill(self, skill):
        choice = self.get_random_sub_skill(skill)
        self.add_sub_skill(skill, choice)
        return choice

    def no_skill(self, skill_string):
        return skill_string not in self.skills

    def make_random(self, classes):
        pass

if __name__ == '__main__':
    pass
