from math import floor


def findAllComb(array, new_arr, base, level):
    if level < array.__len__() - 1:
        for memb in array:
            if base.count(memb) == 0:
                base.append(memb)
                new_arr = findAllComb(array, new_arr, base, level + 1)
                base.pop()
    else:
        for memb in array:
            if base.count(memb) == 0:
                base.append(memb)
                new_arr.append(base.copy())
                base.pop()
    return new_arr


def param_calc(us_input, i, mode):
    if mode == 1:
        param = us_input[i]
    else:
        param = us_input[us_input[i]] if us_input[i] in us_input else 0
    return param


def instr_cmd(optcode, us_input, i, inp_val, B, C):
    if optcode <= 2 or optcode >= 7:
        param1 = param_calc(us_input, i + 1, C)
        param2 = param_calc(us_input, i + 2, B)
        us_input[us_input[i + 3]] = (param1 + param2 if optcode == 1 else param1 * param2) * (1 if optcode <= 2 else 0) \
                         + (1 if param1 < param2 else 0) * (1 if optcode == 7 else 0) \
                         + (1 if param1 == param2 else 0) * (1 if optcode == 8 else 0)
    elif optcode == 3:
        us_input[us_input[i + 1]] = inp_val
    elif optcode == 4:
        inp_val = param_calc(us_input, i + 1, C)
    if 5 <= optcode <= 6:
        param1 = param_calc(us_input, i + 1, C)
        param2 = param_calc(us_input, i + 2, B)
        i = (param2 if param1 != 0 else i + 3) * (1 if optcode == 5 else 0) \
            + (param2 if param1 == 0 else i + 3) * (1 if optcode == 6 else 0)
    else:
        i = i + 4 if optcode <= 2 or (7 <= optcode <= 8) else i + 2
    return i, inp_val


def output_calc(us_input, inp_val, phase, feedback_on):
    i = 0; inp_iter = 0; inp_val_temp = inp_val
    while i < us_input.__len__():
        if us_input[i] < 99:
            # if us_input[i] == 3 or (feedback_on and us_input[i] == 4):
            if us_input[i] == 3:
                inp_iter += 1
            if inp_iter > 2 and feedback_on:
                break
            if inp_iter == 1:
                i, inp_val = instr_cmd(us_input[i], us_input, i, phase, 0, 0)
            elif inp_iter == 2:
                i, inp_val = instr_cmd(us_input[i], us_input, i, inp_val_temp, 0, 0)
                inp_val_temp = inp_val
            else:
                i, inp_val = instr_cmd(us_input[i], us_input, i, inp_val, 0, 0)
        elif us_input[i] == 99:
            break
        else:
            B = floor(us_input[i] / 1000) % 10
            C = floor(us_input[i] / 100) % 10
            optcode = us_input[i] % 100
            if optcode == 3:
                inp_iter += 1
            if inp_iter > 2 and feedback_on:
                break
            if inp_iter == 1:
                i, inp_val = instr_cmd(optcode, us_input, i, phase, B, C)
            elif inp_iter == 2:
                i, inp_val = instr_cmd(optcode, us_input, i, inp_val_temp, B, C)
                inp_val_temp = inp_val
            else:
                i, inp_val = instr_cmd(optcode, us_input, i, inp_val, B, C)
    return inp_val


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input_orig = my_input.copy()
phases = [0, 1, 2, 3, 4]
part1 = 0
comb_arr = findAllComb(phases, [], [], 0)
for comb in comb_arr:
    thrusters = 0
    for phase in comb:
        thrusters = output_calc(my_input, thrusters, phase, 0)
        my_input = my_input_orig.copy()
    if thrusters > part1:
        part1 = thrusters

phases = [5, 6, 7, 8, 9]
phases = [9, 8, 7, 6, 5]
part2 = 0
comb_arr = findAllComb(phases, [], [], 0)

for comb in comb_arr:
    thrusters = 0
    for phase in comb:
        thrusters = output_calc(my_input, thrusters, phase, 1)
    if thrusters > part2:
        part2 = thrusters

print(str(part1) + " " + str(part2))
