# %%
filename = "input.txt"
ins = [(x[0], int(x[1:])) for x in open(filename).read().splitlines()]

loc = 50
count = 0
count2 = 0

for x in ins:
    count2 += x[1] // 100
    dir = -1 if x[0] == "L" else +1
    new = loc + dir * (x[1] % 100)
    count2a = 1 if new > 100 or new < 0 else 0
    if loc == 0 and dir < 0 and count2a > 0:
        count2a -= 1
    count2 += count2a
    loc = new % 100
    if loc == 0:
        count += 1
print(count, count2 + count)
