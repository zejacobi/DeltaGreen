from Lib.Generator import Generator

gen = Generator()
character = gen.generate()
print('Class:\t\t\t', character['Class'])
print('Skill Package:\t\t', character['Package'])
vet_type = character['Veteran']
if vet_type:
    print('Damaged Veteran Type:\t', vet_type)
    disorders = character['Disorders']
    if len(disorders):
        print('Disorder:\t\t', disorders[0])
print('Number of Bonds:\t', character['Number_Bonds'])
print('Bonds:')
for bond in character['Bonds']:
    print('   ', bond, '-', character['Bonds'][bond])
lost_bonds = character['Lost_Bonds']
if len(lost_bonds):
    print('Former Bonds:')
    for bond in lost_bonds:
        print('   ', bond)
print('Adapted To:')
for adaptation in character['Adapted_To']:
    print('   ', adaptation)
print('Attributes')
attributes = character['Attributes']
for attribute_name in ['Hit Points', 'Willpower Points', 'Sanity', 'Breaking Point']:
    print('   ', attribute_name + ':', attributes[attribute_name])
print('Stats')
stats = character['Stats']
for stat_name in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Power',
                  'Charisma']:
    print('   ', stat_name + ':', stats[stat_name])
print('Skills')
skills = character['Skills']
for skill in sorted(skills.keys()):
    print('   ', skill + ':', skills[skill])
