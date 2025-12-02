# %%
f = [
    (int(x.split("-")[0]), int(x.split("-")[1]))
    for x in open("input.txt").read().split(",")
]

p1, p2 = 0, 0


def is_sym(x):
    d = str(x)
    if len(d) % 2 != 0:
        return False
    for i in range(len(d) // 2):
        if d[i] != d[len(d) // 2 + i]:
            return False
    return True


def is_sym_2(x):
    d = str(x)
    for l in range(1, (len(d) // 2) + 1):
        works = True
        for i in range(1, len(d) // l):
            if len(d) % l != 0 or d[0:l] != d[l * i : l * (i + 1)]:
                works = False
                break
        if works:
            return True
    return False


for x in f:
    for i in range(x[0], x[1] + 1):
        if is_sym(i):
            p1 += i
        if is_sym_2(i):
            p2 += i

print(p1, p2)
