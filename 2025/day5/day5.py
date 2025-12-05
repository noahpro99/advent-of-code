# %%
ranges, ids = [x.splitlines() for x in open("input.txt").read().split("\n\n")]
ranges = [tuple(map(int, x.split("-"))) for x in ranges]
ranges.sort()
ids = list(map(int, ids))

p1 = 0
for id in ids:
    for r in ranges:
        if id >= r[0] and id <= r[1]:
            p1 += 1
            break

changed = True
while changed:
    i = 0
    changed = False
    while i < len(ranges) - 1:
        if ranges[i][1] >= ranges[i + 1][0]:
            ranges[i] = (ranges[i][0], max(ranges[i][1], ranges[i + 1][1]))
            ranges.pop(i + 1)
            changed = True
        i += 1

print(p1, sum([r[1] - r[0] + 1 for r in ranges]))
