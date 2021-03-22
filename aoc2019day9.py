def param_calc(us_input, i, rel_base, mode):
    if mode == 1:
        param = us_input[i]
    elif mode == 2:
        param = us_input[us_input[i] + rel_base] if us_input[i] + rel_base in us_input else 0
    else:
        param = us_input[us_input[i]] if us_input[i] in us_input else 0
    return param


def instr_cmd(optcode, us_input, i, inp_val, B, C, rel_base):
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
        us_input[us_input[i + 3]] = (param1 + param2 if optcode == 1 else param1 * param2) * (1 if optcode <= 2 else 0) \
                                   + (1 if param1 < param2 else 0) * (1 if optcode == 7 else 0) \
                                    + (1 if param1 == param2 else 0) * (1 if optcode == 8 else 0)
    elif optcode == 3:
        if C == 1:
            us_input[i + 1] = inp_val
        elif C == 2:
            us_input[us_input[i + 1] + rel_base] = inp_val
        else:
            us_input[us_input[i + 1]] = inp_val
    elif optcode == 4:
        inp_val = param_calc(us_input, i + 1, rel_base, C)
    if 5 <= optcode <= 6:
        param1 = param_calc(us_input, i + 1, rel_base, C)
        param2 = param_calc(us_input, i + 2, rel_base, B)
        i = (param2 if param1 != 0 else i + 3) * (1 if optcode == 5 else 0) \
            + (param2 if param1 == 0 else i + 3) * (1 if optcode == 6 else 0)
    else:
        i = i + 4 if optcode <= 2 or (7 <= optcode <= 8) else i + 2
    return i, inp_val, rel_base


def output_calc(us_input, inp_val):
    i = 0; rel_base = 0
    while i < us_input.__len__():
        if us_input[i] < 99:
            i, inp_val, rel_base = instr_cmd(us_input[i], us_input, i, inp_val, 0, 0, rel_base)
        elif us_input[i] == 99:
            break
        else:
            B = int(str(us_input[i])[0]) if str(us_input[i]).__len__() > 3 else 0
            C = int(str(us_input[i])[1]) if str(us_input[i]).__len__() > 3 else int(str(us_input[i])[0])
            optcode = int(str(us_input[i])[str(us_input[i]).__len__() - 2]
                        + str(us_input[i])[str(us_input[i]).__len__() - 1])
            i, inp_val, rel_base = instr_cmd(optcode, us_input, i, inp_val, B, C, rel_base)
    return inp_val


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input = {i: my_input[i] for i in range(0, len(my_input))}
my_input_orig = my_input.copy()
part1 = output_calc(my_input, 1)

my_input = my_input_orig.copy()
part2 = output_calc(my_input, 5)

print(str(part1) + " " + str(part2))
