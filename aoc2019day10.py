from functools import reduce
import math


def sign(num):
    if num == 0:
        return 0
    return -1 if num < 0 else 1


def checkUpDown(j, x0, y0, my_input, catches):
    for i in range(0, len(my_input[y0]), 1):
        if my_input[j][i] == '#':
            appendable = True
            for x, y in catches[x0, y0]:
                if i == x and x0 == i and ((y0 < y < j) or (y0 > y > j)):
                    appendable = False
                    break
                x_dif, y_dif = catches[x0, y0][x, y]
                if x_dif != 0 and y_dif != 0:
                    NOD = math.gcd(x_dif, y_dif)
                    if NOD > 1:
                        x_dif, y_dif = x_dif / NOD, y_dif / NOD
                    x_check = (x0 - i) % x_dif == 0 and sign(x0 - i) == sign(x_dif)
                    y_check = (y0 - j) % y_dif == 0 and sign(y0 - j) == sign(y_dif)
                    line_check = (x0 - i) / x_dif == (y0 - j) / y_dif and sign(x0 - i) == sign(x_dif)
                    diag_check = abs(x0 - i) == abs(y0 - j) and abs(x - i) == abs(y - j)
                    if ((x_check and y_check) or diag_check) and line_check:
                        appendable = False
                        break
            if appendable:
                catches[x0, y0][i, j] = x0 - i, y0 - j


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

catches = {}
for y in range(0, len(my_input)):
    for x in range(0, len(my_input[0])):
        if my_input[y][x] == '#':
            catches[x, y] = {}
            if x + 1 < len(my_input[0]):
                try:
                    if my_input[y].index('#', x + 1) > 0:
                        catches[x, y][my_input[y].index('#', x + 1), y] = x - my_input[y].index('#', x + 1), 0
                except:
                    continue
            if x - 1 >= 0:
                for i in range(x - 1, -1, -1):
                    if my_input[y][i] == '#':
                        catches[x, y][i, y] = x - i, 0
                        break
            if y - 1 >= 0:
                for j in range(y - 1, -1, -1):
                    checkUpDown(j, x, y, my_input, catches)
            if y + 1 < len(my_input):
                for j in range(y + 1, len(my_input), 1):
                    checkUpDown(j, x, y, my_input, catches)
x0, y0 = reduce(lambda prev, cur: cur if len(catches[cur]) > len(catches[prev]) else prev, catches)
part1 = len(catches[x0, y0])

part2 = catches[x0, y0]
circle = {}
for catch in part2:
    x_dif, y_dif = part2[catch]
    angle = math.atan2(-x_dif, y_dif)
    angle = angle + math.pi * 2 if angle < 0 else angle
    circle[angle] = catch
circle = {k: v for k, v in sorted(circle.items(), key=lambda item: item[0])}
part2 = [v for k, v in circle.items()][199]
part2 = part2[0] * 100 + part2[1]

print(str(part1) + " " + str(part2))
