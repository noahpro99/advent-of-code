# %%
f = open("input.txt").read().splitlines()
X, Y = len(f[0]), len(f)
grid = [
    ["0" if char == "." else "1" if char == "S" else char for char in row] for row in f
]
p1 = 0
for i in range(len(grid) - 1):
    for j in range(len(grid[i])):
        if grid[i][j].isdigit():
            if grid[i + 1][j] == "^":
                grid[i + 1][j - 1] = str(int(grid[i + 1][j - 1]) + int(grid[i][j]))
                grid[i + 1][j + 1] = str(int(grid[i + 1][j + 1]) + int(grid[i][j]))
                p1 += 1
            else:
                grid[i + 1][j] = str(int(grid[i + 1][j]) + int(grid[i][j]))
print(p1, sum([int(x) for x in grid[-1] if x.isdigit()]))
