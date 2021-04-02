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


moves = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
backMoves = {1: 2, 2: 1, 3: 4, 4: 3}
objects = {0: "#", 1: ".", 2: "X"}


def nexMoveChoice(move, cur_coord, map):
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    if new_coord not in map:
        return move
    return 0


def mapBuild(robot, move, cur_coord, map, key, amount):
    robot.input.append(move)
    robot.output_calc()
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    map[new_coord] = objects[robot.output[0]]
    if robot.output[0] >= 1:
        cur_coord = new_coord
        key = False if robot.output[0] == 2 else key
        amount = amount + 1 if key else amount
    if robot.output[0] == 0:
        robot.output = []
        return 0, key, amount
    robot.output = []
    for i in range(1, 5, 1):
        move = nexMoveChoice(i, cur_coord, map)
        if move != 0:
            wallCheck, key, amount = mapBuild(robot, move, cur_coord, map, key, amount)
            if wallCheck != 0:
                robot.input.append(backMoves[move])
                robot.output_calc()
                robot.output = []
                amount = amount - 1 if key else amount
    return 1, key, amount


def oxygenCalc(move, cur_coord, map, amount, oxygenMap, max):
    new_coord = cur_coord[0] + moves[move][0], cur_coord[1] + moves[move][1]
    if map[new_coord] != "#":
        cur_coord = new_coord
        amount += 1
        oxygenMap[cur_coord] = amount
        max = amount if amount > max else max
        for i in range(1, 5, 1):
            move = nexMoveChoice(i, cur_coord, oxygenMap)
            if move != 0:
                max = oxygenCalc(move, cur_coord, map, amount, oxygenMap, max)
    return max

with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input = {i: my_input[i] for i in range(0, len(my_input))}
part1 = intcode(my_input.copy(), [])

map = {(0, 0): 'O'}
key = True; amount = 1
for i in range(1, 5, 1):
    wallCheck, key, amount = mapBuild(part1, i, (0, 0), map, key, amount)
    if wallCheck != 0:
        part1.input.append(backMoves[i])
        part1.output_calc()
        part1.output = []
        if key:
            amount -= 1

coords = [k for k, v in sorted(map.items(), key=lambda item: item[0])]
maxs = reduce(lambda prev, cur: [cur[0] if cur[0] > prev[0] else prev[0], cur[1] if cur[1] > prev[1] else prev[1]], coords, [0, 0])
mins = reduce(lambda prev, cur: [cur[0] if cur[0] < prev[0] else prev[0], cur[1] if cur[1] < prev[1] else prev[1]], coords, [0, 0])

pic = []
for j in range(maxs[1], mins[1] - 1, -1):
    pic.append([])
    for i in range(mins[0], maxs[0] + 1, 1):
        pic[len(pic) - 1].append('?' if (i, j) not in map else map[(i, j)])
for line in pic:
    print((' ').join(line).replace(',', ''))

start = list(filter(lambda elem: elem[1] == 'X', map.items()))[0][0]
oxygenMap = {start: 0}
part2 = 0
for i in range(1, 5, 1):
    part2 = oxygenCalc(i, start, map, 0, oxygenMap, part2)

print(str(amount) + " " + str(part2))
