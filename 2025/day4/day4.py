# %%
f = open("input.txt").read().splitlines()
X, Y = len(f[0]), len(f)

grid = [[char for char in row] for row in f]
dir = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
p2 = 0
while True:
    removed = []
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
                removed.append((r, c))

    for r, c in removed:
        grid[r][c] = "."
    if len(removed) == 0:
        break
    if p2 == 0:
        print(len(removed))
    p2 += len(removed)

print(p2)
