from functools import reduce


def calcOrbits(orbit_map, obj, amount):
    if orbit_map[obj] == 'COM':
        amount += 1
    else:
        amount = calcOrbits(orbit_map, orbit_map[obj], amount + 1)
    return amount


def calcPathYOU_Left(orbit_map, curOrb, amount):
    if curOrb == 'COM':
        amount += 1
    else:
        orbit_map[curOrb]['moves'] = amount
        amount = calcPathYOU_Left(orbit_map, orbit_map[curOrb]['orb'], amount + 1)
    return amount


def calcPathSAN_Left(orbit_map, curOrb):
    if orbit_map[orbit_map[curOrb]['orb']]['moves'] != 0:
        orbit_map[curOrb]['moves'] = orbit_map[orbit_map[curOrb]['orb']]['moves'] + 1
    else:
        orbit_map[curOrb]['moves'] = calcPathSAN_Left(orbit_map, orbit_map[curOrb]['orb']) + 1
    return orbit_map[curOrb]['moves']


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

orbit_map = {}
obj_map = {}
for line in my_input:
    obj, orb = line.split(")")
    if orb in orbit_map:
        orbit_map[orb] = orbit_map[orb], obj
    else:
        orbit_map[orb] = obj
    if obj in obj_map:
        obj_map[obj] = obj_map[obj], orb
    else:
        obj_map[obj] = orb

part1 = reduce(lambda prev, cur: prev + calcOrbits(orbit_map, cur, 0), orbit_map, 0)

for orb in orbit_map:
    orbit_map[orb] = {'orb': orbit_map[orb], 'moves': 0}

calcPathYOU_Left(orbit_map, orbit_map['YOU']['orb'], 0)
calcPathSAN_Left(orbit_map, 'SAN')

part2 = orbit_map['SAN']['moves'] - 1

print(str(part1) + " " + str(part2))
