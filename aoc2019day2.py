def output_calc(us_input):
    for i in range(0, us_input.__len__(), 4):
        if us_input[i] == 1:
            us_input[us_input[i + 3]] = us_input[us_input[i + 1]] + us_input[us_input[i + 2]]
        elif us_input[i] == 2:
            us_input[us_input[i + 3]] = us_input[us_input[i + 1]] * us_input[us_input[i + 2]]
        elif us_input[i] == 99:
            break
    return us_input[0]


with open('C:/Users/User/Documents/input.txt') as f:
    my_input = list(map(lambda a: int(a), f.read().split(',')))
f.close()

my_input_orig = my_input.copy()
my_input[1] = 12
my_input[2] = 2
part1 = output_calc(my_input)

ans = 0
for i in range(0, 99, 1):
    for j in range(0, 99, 1):
        my_input = my_input_orig.copy()
        my_input[1] = i
        my_input[2] = j
        ans = output_calc(my_input)
        if ans == 19690720:
            break
    if ans == 19690720:
        break

part2 = 100 * my_input[1] + my_input[2]

print(str(part1) + " " + str(part2))
