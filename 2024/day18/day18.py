from heapq import heappop, heappush

from tqdm import tqdm

f = open("input.txt").read().splitlines()
X, Y = 71, 71

grid = [[char for char in range(X)] for row in range(Y)]
coords = [[int(x) for x in line.split(",")] for line in f]


def shortest_path(grid):
    frontier = [(0, 0, 0)]
    visited = set()
    while frontier:
        steps, x, y = heappop(frontier)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if x == X - 1 and y == Y - 1:
            return steps
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= x + dx < X and 0 <= y + dy < Y:
                if grid[y + dy][x + dx] == "#":
                    continue
                heappush(frontier, (steps + 1, x + dx, y + dy))
    return -1


def p1(grid):
    grid = [row[:] for row in grid]
    for c in coords[:1024]:
        grid[c[0]][c[1]] = "#"
    return shortest_path(grid)


def blocking_coord(grid):
    for c in tqdm(coords):
        grid[c[0]][c[1]] = "#"
        if shortest_path(grid) == -1:
            return ",".join(map(str, c))


print(p1(grid))
print(blocking_coord(grid))
