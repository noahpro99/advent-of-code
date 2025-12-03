# %%
f = [[int(i) for i in list(x)] for x in open("input.txt").read().splitlines()]
def joltage(f, digits):
    ans = 0
    for x in f:
        digs = []
        for i in range(digits):
            digs.append(max(x[: -digits + i + 1 if -digits + i + 1 != 0 else None]))
            idx = x.index(digs[i])
            x = x[idx + 1 :]
        ans += int("".join([str(d) for d in digs]))
    return ans
print(joltage(f, 2), joltage(f, 12))
