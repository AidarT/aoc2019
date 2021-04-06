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

with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input = {i: my_input[i] for i in range(0, len(my_input))}
part1 = intcode(my_input.copy(), [])

while part1.run:
        part1.output_calc()

amount = 0
pic = list(map(lambda line: [char for char in line], ('').join([chr(i) for i in part1.output]).split('\n')))
for j, line in enumerate(pic):
    for i, ch in enumerate(line):
        if j - 1 >= 0 and j + 1 < len(pic) and i - 1 >= 0 and i + 1 < len(line):
            if ch == '#' and pic[j][i - 1] == '#' and pic[j][i + 1] == '#' \
                    and pic[j - 1][i] == '#' and pic[j + 1][i] == '#':
                pic[j][i] = 'O'
                amount += j * i
    print(('').join(line[1]))


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
