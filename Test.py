from Lib.Generator import Generator

gen = Generator()
gen.generate()
print('Class:\t\t\t', gen.character.get_class())
print('Skill Package:\t\t', gen.character.get_package())
vet_type = gen.character.get_veteran_type()
if vet_type:
    print('Damaged Veteran Type:\t', vet_type)
    disorders = gen.character.get_disorders()
    if len(disorders):
        print('Disorder:\t\t', disorders[0])
print('Number of Bonds:\t', gen.character.num_bonds)
print('Bonds:')
for bond in gen.character.get_bonds():
    print('   ', bond, '-', gen.character.get_stats()['Charisma'])
lost_bonds = gen.character.get_lost_bonds()
if len(lost_bonds):
    print('Former Bonds:')
    for bond in lost_bonds:
        print('   ', bond)
print('Adapted To:')
for adaptation in gen.character.get_adaptations():
    print('   ', adaptation)
print('Attributes')
attributes = gen.character.get_attributes()
for attribute_name in ['Hit Points', 'Willpower Points', 'Sanity', 'Breaking Point']:
    print('   ', attribute_name + ':', attributes[attribute_name])
print('Stats')
stats = gen.character.get_stats()
for stat_name in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Power',
                  'Charisma']:
    print('   ', stat_name + ':', stats[stat_name])
print('Skills')
skills = gen.character.get_skills()
for skill in sorted(skills.keys()):
    print('   ', skill + ':', skills[skill])
