from functools import lru_cache

f = open("input.txt").read().splitlines()

dir_pad = [
    [None, "^", "A"],
    ["<", "v", ">"],
]

num_pad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]


def all_best_paths(start, end, grid):
    queue, visited = [(start, ())], {}
    all_best_paths = []
    while queue:
        cur, path = queue.pop(0)
        if cur in visited and len(path) > visited[cur]:
            continue
        visited[cur] = len(path)
        if cur == end:
            if len(all_best_paths) == 0 or len(path) <= len(all_best_paths[0]):
                all_best_paths.append(path)
            continue
        x, y = cur
        for dx, dy, ds in [(0, 1, ">"), (1, 0, "v"), (0, -1, "<"), (-1, 0, "^")]:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(grid)
                and 0 <= new_y < len(grid[new_x])
                and grid[new_x][new_y] is not None
            ):
                queue.append(((new_x, new_y), (*path, ds)))
    return tuple(all_best_paths)


def shortest_paths(pad):
    paths = {}
    for i, row in enumerate(pad):
        for j, cell in enumerate(row):
            if cell is None:
                continue
            for i2, row2 in enumerate(pad):
                for j2, cell2 in enumerate(row2):
                    if cell2 is None:
                        continue
                    path = all_best_paths((i, j), (i2, j2), pad)
                    if path is not None:
                        paths[cell + cell2] = path
    return paths


def min_presses_num_pad(number):
    @lru_cache
    def min_to_go_and_press(depth, path):
        if depth == 0:
            return len(path) + 1
        tot = 0
        for d, d2 in zip(("A", *path), (*path, "A")):
            all_d_paths = d_paths[d + d2]
            tot += min([min_to_go_and_press(depth - 1, p) for p in all_d_paths])
        return tot

    n_paths = shortest_paths(num_pad)
    d_paths = shortest_paths(dir_pad)
    total = 0
    for code in f:
        presses = 0
        for n, n2 in zip("A" + code, code):
            all_n_paths = n_paths[n + n2]
            new = min([min_to_go_and_press(number, p) for p in all_n_paths])
            presses += new
        total += presses * int("".join([d for d in code if d.isdigit()]))
    return total


print(min_presses_num_pad(2))
print(min_presses_num_pad(25))
