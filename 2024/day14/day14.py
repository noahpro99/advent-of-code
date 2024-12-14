f = open("input.txt").read().splitlines()
X, Y = 101, 103

robots = [
    (
        [int(x) for x in reversed(row.split("=")[1].split(" ")[0].split(","))],
        [int(x) for x in reversed(row.split("=")[2].split(","))],
    )
    for row in f
]
for t in range(1, 100000):
    for r in range(len(robots)):
        robots[r] = (
            [
                (robots[r][0][0] + robots[r][1][0]) % Y,
                (robots[r][0][1] + robots[r][1][1]) % X,
            ],
            robots[r][1],
        )

    grid = [["." for _ in range(X)] for _ in range(Y)]
    for r in robots:
        grid[r[0][0]][r[0][1]] = "#"
    row_exists = False
    for row in grid:
        if "#" * 10 in "".join(row):
            row_exists = True
            break
    if row_exists:
        print("\033[H\033[J")
        for row in grid:
            print("".join(row))
        print(p1, t)
        exit()

    if t == 100:
        p1 = (
            sum([1 for r in robots if r[0][0] < Y // 2 and r[0][1] < X // 2])
            * sum([1 for r in robots if r[0][0] > Y // 2 and r[0][1] < X // 2])
            * sum([1 for r in robots if r[0][0] < Y // 2 and r[0][1] > X // 2])
            * sum([1 for r in robots if r[0][0] > Y // 2 and r[0][1] > X // 2])
        )
