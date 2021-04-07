from math import floor
from functools import reduce

class intcode:
    def __init__(self, instructions, input):
        self.us_input = instructions
        self.input = input
        self.output = []
        self.i = 0
        self.halt = False
        self.run = True
        self.rel_base = 0

    def param_calc(self, i, mode):
        if mode == 1:
            param = self.us_input[i]
        elif mode == 2:
            param = self.us_input[self.us_input[i] + self.rel_base] \
                if self.us_input[i] + self.rel_base in self.us_input else 0
        else:
            param = self.us_input[self.us_input[i]] if self.us_input[i] in self.us_input else 0
        return param


    def instr_cmd(self, optcode, A, B, C):
        if optcode == 9:
            if C == 1:
                self.rel_base = self.rel_base + self.us_input[self.i + 1]
            elif C == 2:
                self.rel_base = self.rel_base + self.us_input[self.us_input[self.i + 1] + self.rel_base] \
                    if self.us_input[self.i + 1] + self.rel_base in self.us_input else self.rel_base
            else:
                self.rel_base = self.rel_base + self.us_input[self.us_input[self.i + 1]] \
                    if self.us_input[self.i + 1] in self.us_input else self.rel_base
        elif optcode <= 2 or optcode >= 7:
            param1 = self.param_calc(self.i + 1, C)
            param2 = self.param_calc(self.i + 2, B)
            addr = self.us_input[self.i + 3] + self.rel_base if A == 2 else self.us_input[self.i + 3]
            self.us_input[addr] = (param1 + param2 if optcode == 1 else param1 * param2) * (1 if optcode <= 2 else 0) \
                                       + (1 if param1 < param2 else 0) * (1 if optcode == 7 else 0) \
                                        + (1 if param1 == param2 else 0) * (1 if optcode == 8 else 0)
        elif optcode == 3:
            if len(self.input) == 0:
                self.halt = True
            else:
                if C == 2:
                    self.us_input[self.us_input[self.i + 1] + self.rel_base] = self.input[0]
                else:
                    self.us_input[self.us_input[self.i + 1]] = self.input[0]
                self.input.pop(0)
        elif optcode == 4:
            self.output.append(self.param_calc(self.i + 1, C))
        if not self.halt:
            if 5 <= optcode <= 6:
                param1 = self.param_calc(self.i + 1, C)
                param2 = self.param_calc(self.i + 2, B)
                self.i = (param2 if param1 != 0 else self.i + 3) * (1 if optcode == 5 else 0) \
                    + (param2 if param1 == 0 else self.i + 3) * (1 if optcode == 6 else 0)
            else:
                self.i = self.i + 4 if optcode <= 2 or (7 <= optcode <= 8) else self.i + 2


    def output_calc(self):
        while self.i < self.us_input.__len__():
            if self.us_input[self.i] == 99:
                self.run = False
                break
            else:
                A = floor(self.us_input[self.i] / 10000) % 10
                B = floor(self.us_input[self.i] / 1000) % 10
                C = floor(self.us_input[self.i] / 100) % 10
                optcode = self.us_input[self.i] % 100
                self.instr_cmd(optcode, A, B, C)
            if self.halt:
                self.halt = False
                break


start_dirs = {"v": 1, "^": 2, ">": 3, "<": 4}
dirs = {1: "D", 2: "U", 3: "R", 4: "L"}
moves = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
backMoves = {1: 2, 2: 1, 3: 4, 4: 3}


def nexMoveChoice(move, cur_coord, map):
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    if new_coord in map and (map[new_coord] == "#" or map[new_coord] == "O"):
        return move
    return 0


def dirChoice(move, dir):
    if (dir == 2 and move == 3) or (dir == 3 and move == 1) or (dir == 1 and move == 4) or (dir == 4 and move == 2):
        return 3
    elif (dir == 2 and move == 4) or (dir == 3 and move == 2) or (dir == 1 and move == 3) or (dir == 4 and move == 1):
        return 4
    return 0


def fullPathCalc(move, cur_coord, map, amount, path, dir):
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    if map[new_coord] == "#" or map[new_coord] == "O":
        while new_coord in map and (map[new_coord] == "#" or map[new_coord] == "O"):
            cur_coord = new_coord
            amount += 1
            new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
        path.append(dirs[dirChoice(move, dir)])
        path.append(amount)
        amount = 0
        old_dir = backMoves[move]
        dir = move
        for i in range(1, 5, 1):
            if i != old_dir:
                move = nexMoveChoice(i, cur_coord, map)
                if move != 0:
                    fullPathCalc(move, cur_coord, map, amount, path, dir)


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input = {i: my_input[i] for i in range(0, len(my_input))}
robot = intcode(my_input.copy(), [])
while robot.run:
        robot.output_calc()

part1 = 0
pic = list(map(lambda line: [char for char in line], ('').join([chr(i) for i in robot.output]).split('\n')))
for j, line in enumerate(pic):
    for i, ch in enumerate(line):
        if j - 1 >= 0 and j + 1 < len(pic) and i - 1 >= 0 and i + 1 < len(line):
            if ch == '#' and pic[j][i - 1] == '#' and pic[j][i + 1] == '#' \
                    and pic[j - 1][i] == '#' and pic[j + 1][i] == '#':
                pic[j][i] = 'O'
                part1 += j * i
    print(('').join(line))

us_map = {(x, y): v for y, line in enumerate(pic) for x, v in enumerate(line)}
start = reduce(lambda prev, cur: cur[0] if cur[1] == "^" or cur[1] == ">" or cur[1] == "<" or cur[1] == "v"
    else prev, us_map.items(), (0, 0))

path = []
for i in range(1, 5, 1):
    start_move = nexMoveChoice(i, start, us_map)
    if start_move != 0:
        break
fullPathCalc(start_move, start, us_map, 0, path, start_dirs[us_map[start]])


def candidatesFound(to_find, ind, path, depth, candidates):
    for i in range(ind + 2, len(path), 2):
        to_find += ',' + (',').join(list(map(str, [path[i], path[i + 1]])))
        amount = len((',').join(list(map(str, path))).split(to_find)) - 1
        if amount > 1 and depth < 3 and i + 3 < len(path):
            candidates[to_find] = amount
            new_path = path_str.replace(to_find, '').replace(',,', ',')
            if new_path[0] == ",":
                new_path = new_path[1:]
            to_find_new = (',').join(list(map(str, [path[i + 2], path[i + 3]])))
            candidatesFound(to_find_new, ind, new_path.split(','), depth + 1, candidates)
        else:
            new_path = path_str
            for j in range(0, 4, 1):
                new_path = new_path.replace(to_find, '').replace(',,', ',')
                if new_path[0] == ",":
                    new_path = new_path[1:]


candidates = {}
path_str = (',').join(list(map(str, path)))
# for j in range(0, len(path), 2):
#     to_find = (',').join(list(map(str, [path[j], path[j + 1]])))
#     for i in range(j + 2, len(path), 2):
#         to_find += ',' + (',').join(list(map(str, [path[i], path[i + 1]])))
#         amount = len(path_str.split(to_find)) - 1
#         if amount > 1:
#             candidates[to_find] = amount

for j in range(0, len(path), 2):
    to_find = (',').join(list(map(str, [path[j], path[j + 1]])))
    candidates = candidatesFound(to_find, j, path, 0, candidates)

my_input[0] = 2
robot = intcode(my_input.copy(), [])

part2 = 0

print(str(part1) + " " + str(part2))
