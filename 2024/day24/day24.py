# %%
from itertools import product

from tqdm import tqdm

fr, fg = open("input.txt").read().split("\n\n")

wires = {name: int(value) for name, value in [x.split(": ") for x in fr.splitlines()]}
gates = [
    {
        "inputs": [x for i, x in enumerate(line.split(" ")) if i in [0, 2]],
        "gate": line.split(" ")[1],
        "output": line.split(" ")[-1],
    }
    for line in fg.splitlines()
]
wires, gates


# %%
ops = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}


def get_value(wire):
    if wire in wires:
        return wires[wire]
    gate = [x for x in gates if x["output"] == wire][0]
    inputs = [get_value(x) for x in gate["inputs"]]
    wires[wire] = ops[gate["gate"]](*inputs)
    return wires[wire]


all_wires = set([x["output"] for x in gates]) | set(wires.keys())
z_wires = tuple(sorted(set([x for x in all_wires if x[0] == "z"]), reverse=True))
p1 = int("".join([str(get_value(x)) for x in z_wires]), 2)
print(p1)
# %%


def get_name(letter, place):
    return letter + ("0" if place < 10 else "") + str(place)


def verify_tree(root, tree, gates, depth=0):
    matching_gate = [x for x in gates if x["output"] == root]
    if not matching_gate:
        return False
    matching_gate = matching_gate[0]
    if matching_gate["gate"] != tree[0]:
        return False
    for sub_tree in tree[1]:
        if type(sub_tree) == str:
            if sub_tree not in matching_gate["inputs"]:
                return False
        else:
            sides = [
                verify_tree(matching_gate["inputs"][x], sub_tree, gates, depth + 1)
                for x in range(2)
            ]
            if not any(sides):
                return False
    return True


def try_gates(gates):
    prev_carry_tree = None
    for place in range(45):
        x_name, y_name, z_name = (
            get_name("x", place),
            get_name("y", place),
            get_name("z", place),
        )
        if place == 0:
            res = verify_tree(z_name, ["XOR", [x_name, y_name]], gates)
            prev_carry_tree = ["AND", [x_name, y_name]]
        else:
            res = verify_tree(
                z_name, ["XOR", [["XOR", [x_name, y_name]], prev_carry_tree]], gates
            )
            prev_carry_tree = [
                "OR",
                [
                    ["AND", [x_name, y_name]],
                    ["AND", [prev_carry_tree, ["XOR", [x_name, y_name]]]],
                ],
            ]
            if not res:
                return place
    return place


swaps = []
output_wires = set(x["output"] for x in gates)
place = try_gates(gates)
for _ in range(4):
    for o1, o2 in tqdm(list(product(output_wires, output_wires))):
        if o1 == o2 or o1 in swaps or o2 in swaps:
            continue
        new_gates = [x.copy() for x in gates]
        g1, g2 = [x for x in new_gates if x["output"] in [o1, o2]]
        g1["output"], g2["output"] = g2["output"], g1["output"]
        new_place = try_gates(new_gates)
        if new_place > place:
            [swaps.append(x) for x in [o1, o2]]
            place = new_place
            gates = [x.copy() for x in new_gates]
            break
print(",".join(sorted(swaps)))


# %%
