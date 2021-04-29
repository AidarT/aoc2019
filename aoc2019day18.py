import re
from functools import reduce


def mapBuild(my_input):
    map = {}; start = 0, 0; keys = {}; doors = {}
    for y, line in enumerate(my_input):
        if y != 0 and y != len(my_input) - 1:
            for x, ch in enumerate(line):
                if ch != '#':
                    map[x, y] = ch
                    if ch.islower():
                        keys[ch] = x, y
                    elif ch.isupper():
                        doors[ch] = x, y
                if ch == "@":
                    start = x, y
    return map, start, keys, doors

moves = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
backMoves = {1: 2, 2: 1, 3: 4, 4: 3}


def collectKeys(move, cur_coord, map, amount, max, collected):
    if amount < max and collected < len(keys):
        new_map = map.copy()
        new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
        if new_coord in new_map and not new_map[new_coord].isupper():
            amount += 1; old_collected = collected
            if new_map[new_coord].islower():
                if new_map[new_coord].upper() in doors:
                    collected += 1
                    if collected == len(keys):
                        new_map[new_coord] = '.'
                        return amount, collected
                    new_map[doors[new_map[new_coord].upper()]] = '.'
                    new_map[new_coord] = '.'
                else:
                    return max, collected
            iters = 0
            for i in range(1, 5, 1):
                iters += 1
                if i != backMoves[move]:
                    max, collected = collectKeys(i, new_coord, new_map, amount, max, collected)
            if iters == 4 and old_collected != collected:
                max, collected = collectKeys(backMoves[move], new_coord, new_map, amount, max, collected)
    return max, collected

with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

map, start, keys, doors = mapBuild(my_input)
part1 = float('inf')

for i in range(1, 5, 1):
    part1, collected = collectKeys(i, start, map.copy(), 0, part1, 0)



part2 = 0

print(str(part1) + " " + str(part2))
