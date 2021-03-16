import re
from functools import reduce


def calc_coord(my_input):
    last = [0, 0]
    coord = []
    for inst in my_input:
        dir1, step = re.findall(r'[A-Z]|\d+', inst)
        if dir1 == "R":
            for i in range(1, int(step) + 1, 1):
                coord.append([last[0] + i, last[1]])
        elif dir1 == "L":
            for i in range(-1, -int(step) - 1, -1):
                coord.append([last[0] + i, last[1]])
        elif dir1 == "U":
            for i in range(1, int(step) + 1, 1):
                coord.append([last[0], last[1] + i])
        elif dir1 == "D":
            for i in range(-1, -int(step) - 1, -1):
                coord.append([last[0], last[1] + i])
        last = coord[coord.__len__() - 1]
    return coord


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

my_input[0] = my_input[0].split(',')
my_input[1] = my_input[1].split(',')

wire1_coord = calc_coord(my_input[0])
wire2_coord = calc_coord(my_input[1])

cross = set(map(tuple, wire1_coord)) & set(map(tuple, wire2_coord))

part1 = reduce(lambda prev, cur: cur if abs(cur[0]) + abs(cur[1]) < abs(prev[0]) + abs(prev[1]) else prev, cross)
part1 = reduce(lambda prev, cur: abs(prev) + abs(cur), part1)

cross_moves = set(map(lambda a: wire1_coord.index(list(a)) + wire2_coord.index(list(a)) + 2, cross))
part2 = min(cross_moves)

print(str(part1) + " " + str(part2))
