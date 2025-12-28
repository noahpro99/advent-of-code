# %%
import numpy as np
import scipy

f = [
    [
        x.split()[0][1:-1],
        [list(map(int, i[1:-1].split(","))) for i in x.split()[1:-1]],
        tuple(map(int, (x.split()[-1][1:-1].split(",")))),
    ]
    for x in open("input.txt").read().splitlines()
]
print(f)
# %%


def flip(x):
    return "#" if x == "." else "."


def shortest(d: str, p: list[list[int]]):
    cache = set()
    h = [("".join(["." for _ in d]), 0)]
    while True:
        cur, s = h.pop(0)
        if (cur, s) in cache:
            continue
        cache.add((cur, s))
        if cur == d:
            return s
        for b in p:
            h.append(
                ("".join([flip(x) if i in b else x for i, x in enumerate(cur)]), s + 1)
            )


def shortest2(d: tuple[int], p: list[list[int]]):
    da = np.array(d)
    pm = np.zeros((len(d), len(p)))
    for i in range(len(p)):
        for j in p[i]:
            pm[j][i] = 1
    res = scipy.optimize.linprog(
        np.ones(len(p)),
        A_eq=pm,
        b_eq=da,
        bounds=[(0, None) for _ in range(len(p))],
        method="highs",
        integrality=1,
    )
    return int(res.x.sum())


print(sum(shortest(b, p) for b, p, _ in f))
print(sum(shortest2(b, p) for _, p, b in f))
# %%
