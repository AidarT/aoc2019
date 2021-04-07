import re
from functools import reduce


def calcPattern(num, length):
    pattern = [0, 1, 0, -1]
    newPattern = []; iter = 0; ind = 0
    for i in range (0, length + 1, 1):
        if iter == num + 1:
            iter = 0
            ind = ind + 1 if ind + 1 < len(pattern) else 0
        newPattern.append(pattern[ind])
        iter += 1
    newPattern.pop(0)
    return newPattern

# def calcFFTphase(input):
#     newInput = input.copy()
#     for ind in range(0, len(input), 1):
#         newVal = 0; pat = 1; iter = 0; i = ind
#         while i < len(input):
#             newVal += input[i] * pat
#             iter += 1
#             if iter >= ind + 1:
#                 iter = 0
#                 pat *= -1
#                 i = i + (ind + 1)
#             i += 1
#         newInput[ind] = abs(newVal) % 10
#     return newInput


def calcFFTphase(input):
    newInput = input.copy()
    for ind in range(0, len(input), 1):
        pattern = calcPattern(ind, len(input))
        newVal = reduce(lambda prev, cur: prev + input[cur[1]] * pattern[cur[0]], enumerate(input), 0)
        newInput[ind] = abs(newVal) % 10
    return newInput

with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), re.findall(r'\d', f.read())))
f.close()

orig_input = my_input.copy()
offset = int(('').join(map(str, my_input[0: 7])))
my_input = {i: my_input[i] for i in range(0, len(my_input))}

for i in range(0, 100, 1):
    my_input = calcFFTphase(my_input)

part1 = int(('').join(map(str, [my_input[0], my_input[1], my_input[2], my_input[3], my_input[4], my_input[5],
                               my_input[6], my_input[7]])))

my_input = orig_input.copy()
my_input = {i: my_input[i % len(my_input)] for i in range(0, len(my_input) * 10000)}

for i in range(0, 100, 1):
    my_input = calcFFTphase(my_input)

part2 = int(''.join(map(str, [my_input[offset % len(my_input)], my_input[(offset + 1) % len(my_input)],
                              my_input[(offset + 2) % len(my_input)], my_input[(offset + 3) % len(my_input)],
                              my_input[(offset + 4) % len(my_input)], my_input[(offset + 5) % len(my_input)],
                              my_input[(offset + 6) % len(my_input)], my_input[(offset + 7) % len(my_input)]])))

print(str(part1) + " " + str(part2))
