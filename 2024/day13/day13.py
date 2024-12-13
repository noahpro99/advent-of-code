f = open("input.txt").read()
mach = [x for x in f.split("\n\n")]
machines = []
for m in mach:
    machines.append(
        {
            "A": [
                float((m.split("\n")[0].split("+")[1].split(",")[0])),
                float(m.split("\n")[0].split("+")[2]),
            ],
            "B": [
                float(m.split("\n")[1].split("+")[1].split(",")[0]),
                float(m.split("\n")[1].split("+")[2]),
            ],
            "Prize": [
                float(
                    10000000000000 + int(m.split("\n")[2].split("=")[1].split(",")[0])
                ),
                float(10000000000000 + int(m.split("\n")[2].split("=")[2])),
            ],
        }
    )


def least_tokens(machine):
    px, py = machine["Prize"]
    slope_a = machine["A"][1] / machine["A"][0]
    slope_b = machine["B"][1] / machine["B"][0]
    b_b = py - slope_b * px
    x = b_b / (slope_a - slope_b)
    y = slope_a * x
    a_presses = x / machine["A"][0]
    b_presses = abs((px - x) / machine["B"][0])

    # other way around
    a_a = px - slope_a * py
    x2 = a_a / (slope_b - slope_a)
    y2 = slope_b * x2
    a_presses2 = (px - x2) / machine["A"][0]
    b_presses2 = abs(x2 / machine["B"][0])

    candidates = [
        (int(round(a_presses)), int(round(b_presses))),
        (int(round(a_presses2)), int(round(b_presses2))),
    ]
    options = [
        3 * x[0] + x[1]
        for x in candidates
        if x[0] * machine["A"][0] + x[1] * machine["B"][0] == px
        and x[0] * machine["A"][1] + x[1] * machine["B"][1] == py
    ]
    return min(options) if options else 0


print(sum([least_tokens(m) for m in machines]))
# 31589 98080815200063
