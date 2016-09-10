from threading import Thread

import random

from Lib.Character import Character
from Lib.Mongo import database


class Generator(object):
    def __init__(self):
        self.classes = []
        self.class_name = ''
        self.defaults = {}
        self.sub_skills = {}

        threads = [
            Thread(target=self.get_classes),
            Thread(target=self.get_defaults),
            Thread(target=self.get_sub_skills)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.character = Character(self.defaults, self.sub_skills)

    def get_classes(self):
        pointer = database['classes'].find()
        for class_obj in pointer:
            self.classes.append(class_obj)

    def get_defaults(self):
        res = database['default_stats'].find_one()
        del res['_id']
        self.defaults = res

    def get_sub_skills(self):
        res = database['sub_skills'].find_one()
        del res['_id']
        self.sub_skills = res

    def set_class(self):
        class_obj = random.choice(self.classes)
        self.class_name = class_obj["_id"]
        self.character.apply_class(class_obj)

