f = open("input.txt").read().splitlines()
grid = [[int(char) for c, char in enumerate(row)] for r, row in enumerate(f)]
X, Y = len(grid[0]), len(grid)
trail_heads = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == 0]


def score(trail_head):
    frontier = [(trail_head, (trail_head))]
    visited = set()
    tops, tops2 = 0, set()
    while frontier:
        (r, c), path = frontier.pop(0)
        if grid[r][c] == 9:
            if (r, c) not in visited:
                tops += 1
            tops2.add(((r, c), path))
        visited.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_r, new_c = r + dr, c + dc
            if (
                0 <= new_r < Y
                and 0 <= new_c < X
                and grid[new_r][new_c] == grid[r][c] + 1
                and (new_r, new_c) not in visited
            ):
                frontier.append(((new_r, new_c), (*path, (new_r, new_c))))
    return tops, len(tops2)


scores = [score(trail_head)[0] for trail_head in trail_heads]
ratings = [score(trail_head)[1] for trail_head in trail_heads]
print(sum(scores), sum(ratings))

# 482 1094
