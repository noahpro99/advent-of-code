# %%
f = open("input.txt").read().splitlines()
X, Y = len(f[0]), len(f)

grid = [[char for c, char in enumerate(row)] for r, row in enumerate(f)]
dir = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
p1 = 0
for r in range(X):
    for c in range(Y):
        pc = 0
        if grid[r][c] == ".":
            continue
        for dr, dc in dir:
            rr, cc = r + dr, c + dc
            if rr < 0 or rr >= X or cc < 0 or cc >= Y:
                continue
            if grid[rr][cc] == "@":
                pc += 1
        if pc < 4:
            p1 += 1

print(p1)
# %%
