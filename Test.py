from pprint import pprint

from Lib.Generator import Generator

gen = Generator()
gen.random_character_class()
gen.random_character_package()
gen.random_character_stats()
print('Class:\t\t\t', gen.character.get_class())
print('Skill Package:\t\t', gen.character.get_package())
print('Number of Bonds:\t', gen.character.bonds)
print('Attributes')
pprint(gen.character.get_attributes())
print('Stats')
pprint(gen.character.get_stats())
print('Skills')
pprint(gen.character.get_skills())
