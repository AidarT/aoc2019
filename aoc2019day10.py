from functools import reduce
import math

def sign(num):
    if num == 0:
        return 0
    return -1 if num < 0 else 1


def checkUpDown(j, x, y, my_input, catches):
    for i in range(0, len(my_input[y]), 1):
        if my_input[j][i] == '#':
            appendable = True
            for catch in catches[x, y]:
                if i == catch[0] and x == i and ((y < catch[1] < j) or (y > catch[1] > j)):
                    appendable = False
                    break
                x_dif, y_dif = catches[x, y][catch]
                if x_dif != 0 and y_dif != 0:
                    NOD = math.gcd(x_dif, y_dif)
                    if NOD > 1:
                        x_dif, y_dif = x_dif / NOD, y_dif / NOD
                    x_check = (x - i) % x_dif == 0 and sign(x - i) == sign(x_dif)
                    y_check = (y - j) % y_dif == 0 and sign(y - j) == sign(y_dif)
                    line_check = (x - i) / x_dif == (y - j) / y_dif and sign(x - i) == sign(x_dif)
                    diag_check = abs(x - i) == abs(y - j) and abs(catch[0] - i) == abs(catch[1] - j)
                    if ((x_check and y_check) or diag_check) and line_check:
                        appendable = False
                        break
            if appendable:
                catches[x, y][i, j] = x - i, y - j


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

catches = {};
errors = 0
for y in range(0, len(my_input)):
    for x in range(0, len(my_input[0])):
        if my_input[y][x] == '#':
            catches[x, y] = {}
            if x + 1 < len(my_input[0]):
                try:
                    if my_input[y].index('#', x + 1) > 0:
                        catches[x, y][my_input[y].index('#', x + 1), y] = x - my_input[y].index('#', x + 1), 0
                except:
                    errors += 1
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
part1 = reduce(lambda prev, cur: len(catches[cur]) if len(catches[cur]) > prev else prev, catches, 0)

part2 = 0

print(str(part1) + " " + str(part2))
