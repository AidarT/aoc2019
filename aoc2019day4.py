import re

my_input = list(map(lambda a: int(a), re.findall(r'\d+', '256310-732736')))

passwords_p1 = set()
passwords_p2 = set()
for num in range(my_input[0], my_input[1] + 1, 1):
    key = True
    prev_dig = 0
    same_count = []
    for dig in str(num):
        if int(dig) > prev_dig:
            prev_dig = int(dig)
        elif int(dig) == prev_dig:
            same_count.append(prev_dig)
            same_count.append(prev_dig)
        else:
            key = False
            break
    if same_count.__len__() < 1:
        key = False
    if key:
        passwords_p1.add(num)
        if same_count.__len__() >= 2:
            for dig in same_count:
                if same_count.count(dig) == 2:
                    passwords_p2.add(num)
                    break

part1 = passwords_p1.__len__()
part2 = passwords_p2.__len__()

print(str(part1) + " " + str(part2))
