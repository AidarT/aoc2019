import math
from functools import reduce
import re
import itertools


def newPattern(elNum):
    pattern = [0, 1, 0, -1]
    newPattern = list(itertools.chain.from_iterable(itertools.repeat(a, elNum) for a in pattern))
    return newPattern


def calcFFTphase(input):
    newInput = input.copy()
    for ind in enumerate(input):
        pattern = newPattern(ind[0] + 1)
        newVal = 0; i_pat = 1
        for num in input:
            newVal += num * pattern[i_pat]
            i_pat = i_pat + 1 if i_pat + 1 < len(pattern) else 0
        newVal = abs(newVal) % 10
        newInput[ind[0]] = newVal
    return newInput


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), re.findall(r'-?\d', f.read())))
f.close()

for i in range(0, 100, 1):
    my_input = calcFFTphase(my_input.copy())

part1 = int(''.join(map(str, my_input[0: 8])))

part2 = 0

print(str(part1) + " " + str(part2))
