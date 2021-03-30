from math import floor
from functools import reduce

class intcode:
    def __init__(self, instructions, input):
        self.us_input = instructions
        self.input = input
        self.output = []
        self.i = 0
        self.halt = False
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


    def newPosAndDir(self, pos, dir, angle):
        dirs = {0: [0, 1], 90: [1, 0], 180: [0, -1], 270: [-1, 0]}
        dir = dir + 90 * (2 * angle - 1)
        if dir < 0:
            dir += 360
        elif dir > 270:
            dir -= 360
        pos[0] += dirs[dir][0]
        pos[1] += dirs[dir][1]
        return pos, dir


    def output_calc(self):
        panels = {}; pos = [0, 0]; dir = 0
        while self.i < self.us_input.__len__():
            if self.us_input[self.i] == 99:
                break
            else:
                A = floor(self.us_input[self.i] / 10000) % 10
                B = floor(self.us_input[self.i] / 1000) % 10
                C = floor(self.us_input[self.i] / 100) % 10
                optcode = self.us_input[self.i] % 100
                self.instr_cmd(optcode, A, B, C)
            if self.halt:
                panels[tuple(pos)] = self.output[0]
                pos, dir = self.newPosAndDir(pos, dir, self.output[1])
                self.output = []
                self.input.append(0 if tuple(pos) not in panels else panels[tuple(pos)])
                self.halt = False
        self.output = panels


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input = {i: my_input[i] for i in range(0, len(my_input))}
part1 = intcode(my_input.copy(), [0])
part1.output_calc()
part1 = len(part1.output)

part2 = intcode(my_input.copy(), [1])
part2.output_calc()
coords = [k for k, v in sorted(part2.output.items(), key=lambda item: item[0])]
maxs = reduce(lambda prev, cur: [cur[0] if cur[0] > prev[0] else prev[0], cur[1] if cur[1] > prev[1] else prev[1]], coords, [0, 0])
mins = reduce(lambda prev, cur: [cur[0] if cur[0] < prev[0] else prev[0], cur[1] if cur[1] < prev[1] else prev[1]], coords, [0, 0])

pic = []
for j in range(maxs[1], mins[1] - 1, -1):
    pic.append([])
    for i in range(mins[0], maxs[0] + 1, 1):
        pic[len(pic) - 1].append(0 if (i, j) not in part2.output else part2.output[(i, j)])

print(str(part1))
for line in pic:
    print(('').join(map(str, line)).replace('1', '#').replace('0', '_'))
