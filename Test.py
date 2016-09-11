from pprint import pprint

from Lib.Generator import Generator

gen = Generator()
gen.generate()
print('Class:\t\t\t', gen.character.get_class())
print('Skill Package:\t\t', gen.character.get_package())
print('Number of Bonds:\t', gen.character.num_bonds)
print('Bonds:')
for bond in gen.character.get_bonds():
    print('   ', bond)

print('Attributes')
attributes = gen.character.get_attributes()
for attribute_name in ['Hit Points', 'Willpower Points', 'Sanity', 'Breaking Point']:
    print('   ', attribute_name + ':', attributes[attribute_name])
print('Stats')
stats = gen.character.get_stats()
for stat_name in sorted(stats.keys()):
    print('   ', stat_name + ':', stats[stat_name])
print('Skills')
skills = gen.character.get_skills()
for skill in sorted(skills.keys()):
    print('   ', skill + ':', skills[skill])
