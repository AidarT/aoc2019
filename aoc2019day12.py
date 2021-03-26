from functools import reduce
import re
import copy


def sim_cycle(position, velocity):
    for moon in position:
        for paired in position:
            if moon != paired:
                for i in range(0, 3, 1):
                    if moon[i] < paired[i]:
                        velocity[position.index(moon)][i] += 1
                    elif moon[i] > paired[i]:
                        velocity[position.index(moon)][i] -= 1
    for moon in position:
        for i in range(0, 3, 1):
            moon[i] += velocity[position.index(moon)][i]


with open('C:/Users/User/Documents/input.txt') as f:
    position = list(map(lambda a: list(map(lambda a: int(a), re.findall(r'-?\d+', a))), f.read().split('\n')))
f.close()

velocity = [[0, 0, 0] for a in range(0, 4, 1)]
pos_orig = copy.deepcopy(position); vel_orig = copy.deepcopy(velocity)
for i in range(0, 1000, 1):
    sim_cycle(position, velocity)

part1 = reduce(lambda prev, cur: prev + (abs(cur[0]) + abs(cur[1]) + abs(cur[2])) *
                (abs(velocity[position.index(cur)][0]) + abs(velocity[position.index(cur)][1]) +
                 abs(velocity[position.index(cur)][2])), position, 0)

position = copy.deepcopy(pos_orig); velocity = copy.deepcopy(vel_orig)
part2 = 0; states = set()
states.add((', ').join(map(str, position)).replace('[', '').replace(']', '') +
           (', ').join(map(str, velocity)).replace('[', '').replace(']', ''))
while True:
    part2 += 1
    sim_cycle(position, velocity)
    if part2 == 4686774924:
        tmp = 1
    saved = (', ').join(map(str, position)).replace('[', '').replace(']', '') + \
            (', ').join(map(str, velocity)).replace('[', '').replace(']', '')
    if saved in states:
        break
    else:
        states.add(saved)

print(str(part1) + " " + str(part2))
