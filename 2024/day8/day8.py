import itertools
from collections import defaultdict

filename = "input.txt"
f = open(filename).read().splitlines()
X, Y = len(f[0]), len(f)
antis = defaultdict(list)
[
    [antis[col].append((r, c)) for c, col in enumerate(row) if row[c] != "."]
    for r, row in enumerate(f)
]
anodes = set()


def anti_nodes(p1):
    anodes = set()
    for coords in antis.values():
        for combo in itertools.combinations(coords, 2):
            r = range(1, 1000) if p1 else range(2, 3)
            for i in r:
                new = [0, 0]
                new2 = [0, 0]
                new[0] = combo[0][0] + i * (combo[1][0] - combo[0][0])
                new[1] = combo[0][1] + i * (combo[1][1] - combo[0][1])
                new2[0] = combo[1][0] + i * (combo[0][0] - combo[1][0])
                new2[1] = combo[1][1] + i * (combo[0][1] - combo[1][1])
                if new[0] >= 0 and new[0] < Y and new[1] >= 0 and new[1] < X:
                    anodes.add(tuple(new))

                if new2[0] >= 0 and new2[0] < Y and new2[1] >= 0 and new2[1] < X:
                    anodes.add(tuple(new2))

    return len(anodes)


print(anti_nodes(False))
print(anti_nodes(True))
# 323 1077
