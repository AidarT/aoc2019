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


def nexMoveChoice(move, cur_coord, map):
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    if new_coord in map and (map[new_coord] == "#" or map[new_coord] == "O"):
        return move
    return 0


def collectKeys(move, cur_coord, map, amount):
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    if new_coord in map:
        amount += 1



with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

map, start, keys, doors = mapBuild(my_input)



part1 = 0

part2 = 0

print(str(part1) + " " + str(part2))
