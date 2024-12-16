from heapq import heappop, heappush

f = open("input.txt").read().splitlines()
X, Y = len(f[0]), len(f)
grid = [[char for c, char in enumerate(row)] for r, row in enumerate(f)]
special = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == "S"][0]
opposite = {"R": "L", "L": "R", "U": "D", "D": "U"}


def best_path(special, grid):
    frontier = [(0, special, ((*special, "R"),))]
    visited = {}
    best_score = None
    tiles = set()
    while frontier:
        score, (r, c), path = heappop(frontier)
        if (r, c, path[-1][2]) in visited and visited[(r, c, path[-1][2])] < score:
            continue
        visited[(r, c, path[-1][2])] = score
        if grid[r][c] == "E":
            if best_score is not None and score > best_score:
                return len(tiles), best_score, path
            best_score = score
            path_coords = [(rr, cc) for rr, cc, _ in path]
            for rr, cc in path_coords:
                tiles.add((rr, cc))
        possible_new_directions = [
            x
            for x in [(0, 1, "R"), (0, -1, "L"), (1, 0, "D"), (-1, 0, "U")]
            if x[2] != opposite[path[-1][2]]
        ]
        for dr, dc, direction in possible_new_directions:
            new_r, new_c = r + dr, c + dc
            new_path = (*path, (new_r, new_c, direction))
            new_score = (
                score + 1000 if path and path[-1][2] != direction else score
            ) + 1
            if 0 <= new_r < Y and 0 <= new_c < X and grid[new_r][new_c] != "#":
                heappush(frontier, (new_score, (new_r, new_c), new_path))
    return len(tiles), best_score, path


tiles_in_all_best_paths, best_score, path = best_path(special, grid)
print(best_score, tiles_in_all_best_paths)
