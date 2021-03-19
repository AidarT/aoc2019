import re
from functools import reduce


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), re.findall(r'.', f.read())))
f.close()

layers = []
for i in range(0, my_input.__len__(), 25 * 6):
    layers.append(my_input[i: i + 25 * 6])

part1 = reduce(lambda cur, prev: cur if cur.count(0) < prev.count(0) else prev, layers)
part1 = part1.count(1) * part1.count(2)

layers = []
for i in range(0, my_input.__len__(), 25 * 6):
    layers.append([])
    part = my_input[i: i + 25 * 6]
    for j in range(0, 25 * 6, 25):
        layers[layers.__len__()-1].append(part[j: j + 25])

part2 = layers[0].copy()
for j in range(0, layers[0].__len__(), 1):
    for i in range(0, layers[0][0].__len__(), 1):
        part2[j][i] = 2
        for layer in layers:
            if part2[j][i] == 2:
                if layer[j][i] != 2:
                    part2[j][i] = "_" if layer[j][i] == 0 else "#"
            else:
                break

print(str(part1))
for line in part2:
    print(('').join(map(str, line)).replace('[', '').replace(']', '').replace(', ', ''))
