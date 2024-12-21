# %%
from itertools import product

from tqdm import tqdm

f = open("input.txt").read().splitlines()
X, Y = len(f[0]), len(f)

grid = [[char for c, char in enumerate(row)] for r, row in enumerate(f)]
start = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == "S"][0]
end = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == "E"][0]
grid, start, end


# %%
def shortest_path(grid, start, end, cheats=False, cheat_set=None):
    frontier = [(start, (start,))]
    visited = set()
    while frontier:
        current, path = frontier.pop(0)
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        for r, c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_r, new_c = current[0] + r, current[1] + c
            if not (0 <= new_r < Y and 0 <= new_c < X):
                continue
            if grid[new_r][new_c] != "#":
                frontier.append(
                    (
                        (new_r, new_c),
                        path + ((new_r, new_c),),
                    )
                )
    return None


path = shortest_path(grid, start, end)

p1 = 0
for r, c in tqdm(path):
    for rr, cc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
        new_r, new_c = r + rr, c + cc
        if (new_r, new_c) in path and path.index((new_r, new_c)) >= path.index(
            (r, c)
        ) + 100 + 2:
            p1 += 1

print(p1)

p2 = 0
for r, c in tqdm(path):
    for rr, cc in product(range(-20, 21), range(-20, 21)):
        new_r, new_c = r + rr, c + cc
        if (new_r, new_c) in path and path.index((new_r, new_c)) >= path.index(
            (r, c)
        ) + 100 + 2:
            p2 += 1

print(p2)

# %%
