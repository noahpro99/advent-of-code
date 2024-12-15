f = (
    open("input.txt")
    .read()
    .replace("#", "##")
    .replace("O", "[]")
    .replace(".", "..")
    .replace("@", "@.")
)

grid = [[c for c in row] for r, row in enumerate(f.split("\n\n")[0].splitlines())]
X, Y = len(grid[0]), len(grid)
x, y = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == "@"][0]
ins_map = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
instructions = [ins_map[c] for c in f.split("\n\n")[1] if c in ins_map]


def other_half(x, y, c):
    if c == "[":
        return x, y + 1
    elif c == "]":
        return x, y - 1


def move(x, y, dx, dy, actually_move=True):
    if grid[x + dx][y + dy] == ".":
        if actually_move:
            grid[x + dx][y + dy] = grid[x][y]
            grid[x][y] = "."
        return x + dx, y + dy
    elif grid[x + dx][y + dy] in ["[", "]"]:
        if dx == 0:
            if move(x + dx, y + dy, dx, dy, actually_move) is not None:
                if actually_move:
                    grid[x + dx][y + dy] = grid[x][y]
                    grid[x][y] = "."
                return x + dx, y + dy
        else:
            other_x, other_y = other_half(x + dx, y + dy, grid[x + dx][y + dy])
            if (
                move(other_x, other_y, dx, dy, actually_move=False) is not None
                and move(x + dx, y + dy, dx, dy, actually_move=False) is not None
            ):
                move(other_x, other_y, dx, dy, actually_move)
                move(x + dx, y + dy, dx, dy, actually_move)
                if actually_move:
                    grid[x + dx][y + dy] = grid[x][y]
                    grid[x][y] = "."
                return x + dx, y + dy

    return None


for i, ins in enumerate(instructions):
    res = move(x, y, *ins, False)
    if res is not None:
        move(x, y, *ins, True)
        x, y = res
for r in grid:
    print("".join(r))
print(sum(100 * y + x for x in range(X) for y in range(Y) if grid[y][x] == "["))
