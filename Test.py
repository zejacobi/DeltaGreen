from pprint import pprint

from Lib.Generator import Generator

gen = Generator()
gen.random_character_class()
gen.random_character_package()
print(gen.character.get_class())
print(gen.character.get_package())
pprint(gen.character.get_skills())
