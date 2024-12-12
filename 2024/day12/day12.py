def merge_regions(grid, r, c):
    frontier = [(r, c)]
    visited = set()
    while frontier:
        nr, nc = frontier.pop()
        if (nr, nc) in visited:
            continue
        visited.add((nr, nc))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nnr, nnc = nr + dr, nc + dc
            if 0 <= nnr < Y and 0 <= nnc < X and grid[nnr][nnc][0] == grid[r][c][0]:
                frontier.append((nnr, nnc))
                grid[nnr][nnc] = (grid[r][c][0], grid[r][c][1], grid[nnr][nnc][2])


def fence_info(grid):
    areas = {}
    for r in range(Y):
        for c in range(X):
            if grid[r][c][1] not in areas:
                areas[grid[r][c][1]] = [0, 0, 0]
            for dr, dc, (dnr, dnc) in [
                (0, 1, (1, 0)),
                (1, 0, (0, -1)),
                (0, -1, (-1, 0)),
                (-1, 0, (0, 1)),
            ]:
                nr, nc = r + dr, c + dc
                neir, neic = r + dnr, c + dnc
                neior, neioc = r + dnr + dr, c + dnc + dc
                neighbor_places = (
                    0 <= neir < Y
                    and 0 <= neic < X
                    and grid[neir][neic][1] == grid[r][c][1]
                    and (
                        (0 > neior or neior >= Y or 0 > neioc or neioc >= X)
                        or grid[neir][neic][1] != grid[neior][neioc][1]
                    )
                )
                we_place = (0 > nr or nr >= Y or 0 > nc or nc >= X) or grid[nr][nc][
                    1
                ] != grid[r][c][1]
                if we_place and not neighbor_places:
                    areas[grid[r][c][1]][2] += 1
                if we_place:
                    areas[grid[r][c][1]][0] += 1
            areas[grid[r][c][1]][1] += 1
    return areas


f = open("input.txt").read().splitlines()
X, Y = len(f[0]), len(f)
grid = [
    [(char, r * X + c, (r, c)) for c, char in enumerate(row)] for r, row in enumerate(f)
]
[merge_regions(grid, r, c) for r in range(Y) for c in range(X)]
areas = fence_info(grid)
fences = [p * a for p, a, _ in areas.values()]
fences_strait = [ps * a for _, a, ps in areas.values()]
print(sum(fences), sum(fences_strait))
