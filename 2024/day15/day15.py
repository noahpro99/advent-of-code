# %%
import sys

sys.setrecursionlimit(int(1e6))


f = open("input.txt").read()


grid = [[c for c in row] for r, row in enumerate(f.split("\n\n")[0].splitlines())]
X, Y = len(grid[0]), len(grid)
x, y = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == "@"][0]
ins_map = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
instructions = [ins_map[c] for c in f.split("\n\n")[1] if c in ins_map]
x, y, instructions


# %%
def move(x, y, dx, dy):
    if grid[x + dx][y + dy] == ".":
        grid[x + dx][y + dy] = grid[x][y]
        grid[x][y] = "."
        return x + dx, y + dy
    elif grid[x + dx][y + dy] == "O":
        if move(x + dx, y + dy, dx, dy) is not None:
            grid[x + dx][y + dy] = grid[x][y]
            grid[x][y] = "."
            return x + dx, y + dy
    return None


for r in grid:
    print("".join(r))
for i, ins in enumerate(instructions):
    # try to move in the direction of the instruction
    print(ins, {(0, 1): ">", (0, -1): "<", (-1, 0): "^", (1, 0): "v"}[ins])
    res = move(x, y, *ins)
    if res is not None:
        x, y = res
    for r in grid:
        print("".join(r))

    # if i == 10:
    #     break
# %%
sum(100 * y + x for x in range(X) for y in range(Y) if grid[y][x] == "O")
# %%
