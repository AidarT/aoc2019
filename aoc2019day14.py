import math
from functools import reduce
import copy


def ore_calc(ch_search, reactions, quantity, final):
    for_del = []
    for srch in ch_search:
        check = reduce(lambda prev, cur: prev + 1 if ','.join(cur).find(srch) != -1 else prev, reactions.values(), 0)
        if check == 0:
            if "ORE" not in reactions[srch]:
                for ch in reactions[srch]:
                    final[ch] = int(reactions[srch][ch]) * int(math.ceil(int(final[srch]) / int(quantity[srch]))) \
                        if ch not in final \
                        else int(reactions[srch][ch]) * int(math.ceil(int(final[srch]) / int(quantity[srch]))) + final[ch]
                for_del.append(srch)
    if len(for_del) > 0:
        for srch in for_del:
            final.pop(srch, -1)
            reactions.pop(srch, -1)
    return len(for_del), [k for k, v in sorted(final.items(), key=lambda item: item[0])]

with open('C:/Users/User/Documents/input.txt') as f:
    my_input = f.read().split('\n')
f.close()

reactions = {}; quantity = {}; final = {"FUEL": 1}
for line in my_input:
    chemicals = line.split(" => ")
    reactions[chemicals[1].split(" ")[1]] = {}
    quantity[chemicals[1].split(" ")[1]] = chemicals[1].split(" ")[0]
    list = chemicals[0].split(", ")
    for ch in list:
        reactions[chemicals[1].split(" ")[1]][ch.split(" ")[1]] = ch.split(" ")[0]

reactions_orig = copy.deepcopy(reactions); quantity_orig = copy.deepcopy(quantity)
ch_search = ["FUEL"]
while True:
    changed, ch_search = ore_calc(ch_search, reactions, quantity, final)
    if changed == 0:
        break

part1 = reduce(lambda prev, cur: prev + math.ceil(final[cur] / int(quantity[cur])) * int(reactions[cur]["ORE"]), final, 0)

i = math.ceil(1000000000000 / part1)
while True:
    ch_search = ["FUEL"]
    reactions = copy.deepcopy(reactions_orig); quantity = copy.deepcopy(quantity_orig)
    quantity["FUEL"] = int(quantity["FUEL"]) + i
    final = {"FUEL": quantity["FUEL"]}
    for ch in reactions["FUEL"]:
        reactions["FUEL"][ch] = int(reactions["FUEL"][ch]) * quantity["FUEL"]
    while True:
        changed, ch_search = ore_calc(ch_search, reactions, quantity, final)
        if changed == 0:
            break
    new_part2 = reduce(lambda prev, cur: prev + math.ceil(final[cur] / int(quantity[cur])) * int(reactions[cur]["ORE"]),
                   final, 0)
    if new_part2 <= 1000000000000:
        part2 = i + 1
    else:
        break
    i += 1

print(str(part1) + " " + str(part2))
