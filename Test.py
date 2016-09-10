from pprint import pprint

from Lib.Generator import Generator
from Lib.Character import Character

gen = Generator()
gen.set_class()
pprint(gen.character.get_skills())
