f = open("ex.txt").read().splitlines()
X, Y = len(f[0]), len(f)
grid = [[char for c, char in enumerate(row)] for r, row in enumerate(f)]
special = [(r, c) for r in range(Y) for c in range(X) if grid[r][c] == 0]
special
