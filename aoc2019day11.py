from math import floor
from functools import reduce


def param_calc(us_input, i, rel_base, mode):
    if mode == 1:
        param = us_input[i]
    elif mode == 2:
        param = us_input[us_input[i] + rel_base] if us_input[i] + rel_base in us_input else 0
    else:
        param = us_input[us_input[i]] if us_input[i] in us_input else 0
    return param


def instr_cmd(optcode, us_input, i, inp_val, outp_val, A, B, C, rel_base, halt):
    if optcode == 9:
        if C == 1:
            rel_base = rel_base + us_input[i + 1]
        elif C == 2:
            rel_base = rel_base + us_input[us_input[i + 1] + rel_base] if us_input[i + 1] + rel_base in us_input \
                else rel_base
        else:
            rel_base = rel_base + us_input[us_input[i + 1]] if us_input[i + 1] in us_input else rel_base
    elif optcode <= 2 or optcode >= 7:
        param1 = param_calc(us_input, i + 1, rel_base, C)
        param2 = param_calc(us_input, i + 2, rel_base, B)
        addr = us_input[i + 3] + rel_base if A == 2 else us_input[i + 3]
        us_input[addr] = (param1 + param2 if optcode == 1 else param1 * param2) * (1 if optcode <= 2 else 0) \
                                   + (1 if param1 < param2 else 0) * (1 if optcode == 7 else 0) \
                                    + (1 if param1 == param2 else 0) * (1 if optcode == 8 else 0)
    elif optcode == 3:
        if len(inp_val) == 0:
            halt = True
        else:
            if C == 2:
                us_input[us_input[i + 1] + rel_base] = inp_val[0]
            else:
                us_input[us_input[i + 1]] = inp_val[0]
            inp_val.pop(0)
    elif optcode == 4:
        outp_val.append(param_calc(us_input, i + 1, rel_base, C))
    if not halt:
        if 5 <= optcode <= 6:
            param1 = param_calc(us_input, i + 1, rel_base, C)
            param2 = param_calc(us_input, i + 2, rel_base, B)
            i = (param2 if param1 != 0 else i + 3) * (1 if optcode == 5 else 0) \
                + (param2 if param1 == 0 else i + 3) * (1 if optcode == 6 else 0)
        else:
            i = i + 4 if optcode <= 2 or (7 <= optcode <= 8) else i + 2
    return i, inp_val, rel_base, halt


def newPosAndDir(pos, dir, angle):
    dir = dir + 90 * (2 * angle - 1)
    if dir < 0:
        dir += 360
    elif dir > 270:
        dir -= 360
    if dir == 0:
        pos[1] += 1
    elif dir == 90:
        pos[0] += 1
    elif dir == 180:
        pos[1] -= 1
    elif dir == 270:
        pos[0] -= 1
    return pos, dir


def output_calc(us_input, inp_val):
    i = 0; rel_base = 0; outp_val = []; panels = {}; pos = [0, 0]; dir = 0; halt = False
    while i < us_input.__len__():
        if us_input[i] < 99:
            i, inp_val, rel_base, halt = instr_cmd(us_input[i], us_input, i, inp_val, outp_val, 0, 0, 0, rel_base, halt)
        elif us_input[i] == 99:
            break
        else:
            A = floor(us_input[i] / 10000) % 10
            B = floor(us_input[i] / 1000) % 10
            C = floor(us_input[i] / 100) % 10
            optcode = us_input[i] % 100
            i, inp_val, rel_base, halt = instr_cmd(optcode, us_input, i, inp_val, outp_val, A, B, C, rel_base, halt)
        if halt:
            panels[tuple(pos)] = outp_val[0]
            pos, dir = newPosAndDir(pos, dir, outp_val[1])
            outp_val = []
            inp_val.append(0 if tuple(pos) not in panels else panels[tuple(pos)])
            halt = False
    return panels


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input = {i: my_input[i] for i in range(0, len(my_input))}
my_input_orig = my_input.copy()
part1 = len(output_calc(my_input, [0]))

my_input = my_input_orig.copy()
part2 = output_calc(my_input, [1])
coords = [k for k, v in sorted(part2.items(), key=lambda item: item[0])]
maxs = reduce(lambda prev, cur: [cur[0] if cur[0] > prev[0] else prev[0], cur[1] if cur[1] > prev[1] else prev[1]], coords, [0, 0])
mins = reduce(lambda prev, cur: [cur[0] if cur[0] < prev[0] else prev[0], cur[1] if cur[1] < prev[1] else prev[1]], coords, [0, 0])

pic = []
for j in range(maxs[1], mins[1] - 1, -1):
    pic.append([])
    for i in range(mins[0], maxs[0] + 1, 1):
        pic[len(pic) - 1].append(0 if (i, j) not in part2 else part2[(i, j)])

print(str(part1))
for line in pic:
    print(('').join(map(str, line)).replace('1', '#').replace('0', '_'))
