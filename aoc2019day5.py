def instr_cmd(optcode, us_input, i, inp_val, B, C):
    if optcode <= 2 or optcode >= 7:
        param1 = us_input[i + 1] if C else us_input[us_input[i + 1]]
        param2 = us_input[i + 2] if B else us_input[us_input[i + 2]]
        us_input[us_input[i + 3]] = (param1 + param2 if optcode == 1 else param1 * param2) * (1 if optcode <= 2 else 0) \
                                   + (1 if param1 < param2 else 0) * (1 if optcode == 7 else 0) \
                                    + (1 if param1 == param2 else 0) * (1 if optcode == 8 else 0)
    elif optcode == 3:
        if C:
            us_input[i + 1] = inp_val
        else:
            us_input[us_input[i + 1]] = inp_val
    elif optcode == 4:
        inp_val = us_input[i + 1] if C else us_input[us_input[i + 1]]
    if 5 <= optcode <= 6:
        param1 = us_input[i + 1] if C else us_input[us_input[i + 1]]
        param2 = us_input[i + 2] if B else us_input[us_input[i + 2]]
        i = (param2 if param1 != 0 else i + 3) * (1 if optcode == 5 else 0) \
            + (param2 if param1 == 0 else i + 3) * (1 if optcode == 6 else 0)
    else:
        i = i + 4 if optcode <= 2 or optcode >= 7 else i + 2
    return i, inp_val


def output_calc(us_input, inp_val):
    i = 0
    while i < us_input.__len__():
        if us_input[i] < 99:
            i, inp_val = instr_cmd(us_input[i], us_input, i, inp_val, 0, 0)
        elif us_input[i] == 99:
            break
        else:
            if str(us_input[i]).__len__() > 3:
                B = int(str(us_input[i])[0])
                C = int(str(us_input[i])[1])
            elif str(us_input[i]).__len__() > 2:
                B = 0
                C = int(str(us_input[i])[0])
            optcode = int(str(us_input[i])[str(us_input[i]).__len__() - 2]
                        + str(us_input[i])[str(us_input[i]).__len__() - 1])
            i, inp_val = instr_cmd(optcode, us_input, i, inp_val, B, C)
    return inp_val


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input_orig = my_input.copy()
part1 = output_calc(my_input, 1)

my_input = my_input_orig.copy()
part2 = output_calc(my_input, 5)

print(str(part1) + " " + str(part2))
