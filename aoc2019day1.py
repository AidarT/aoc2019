import math
from functools import reduce


def fuel_calc(mass):
    fuel = math.floor(mass / 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + fuel_calc(fuel)


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split('\n')))
f.close()

part1 = reduce(lambda prev, cur: prev + cur, list(map(lambda a: math.floor(a / 3) - 2, my_input)), 0)

part2 = reduce(lambda prev, cur: prev + cur, list(map(lambda a: fuel_calc(a), my_input)), 0)

print(str(part1) + " " + str(part2))
