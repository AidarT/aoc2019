from functools import reduce
import re
import copy


def lcm(a, b):
    import math
    return (a * b) // math.gcd(a, b)


def sim_cycle(position, velocity):
    for moon in enumerate(position):
        for paired in position:
            if moon[1] != paired:
                for i in range(0, 3, 1):
                    if position[moon[0]][i] < paired[i]:
                        velocity[moon[0]][i] += 1
                    elif position[moon[0]][i] > paired[i]:
                        velocity[moon[0]][i] -= 1
    for moon in enumerate(position):
        for i in range(0, 3, 1):
            position[moon[0]][i] += velocity[moon[0]][i]


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

dimensions = []
for i in range(0, 3, 1):
    position = copy.deepcopy(pos_orig); velocity = copy.deepcopy(vel_orig)
    part2 = 0; states = set()
    while True:
        saved = reduce(lambda prev, cur: prev + str(cur[i]) + ", ", position, "")
        saved += reduce(lambda prev, cur: prev + str(cur[i]) + ", ", velocity, "")
        saved = saved[:-2]
        if saved in states:
            dimensions.append(part2)
            break
        else:
            states.add(saved)
        part2 += 1
        sim_cycle(position, velocity)

part2 = lcm(dimensions[0], dimensions[1])
part2 = lcm(part2, dimensions[2])

print(str(part1) + " " + str(part2))
