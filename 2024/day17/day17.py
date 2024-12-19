f = open("input.txt").read()
reg = {
    l.split(" ")[1].split(":")[0]: int(l.split(": ")[1])
    for l in f.split("\n\n")[0].split("\n")
}
inst = [
    int(x) for l in f.split("\n\n")[1].split("\n") for x in l.split(": ")[1].split(",")
]
reg, inst


def run(reg, ins, p2=False) -> list | None:
    def combo(op):
        if op <= 3:
            return op
        elif op == 4:
            return reg["A"]
        elif op == 5:
            return reg["B"]
        elif op == 6:
            return reg["C"]
        elif op == 7:
            raise Exception("Invalid operation")
        raise Exception("Invalid operation")

    i = 0
    out = []
    while i < len(ins):
        # if not p2:
        #     print(i, [oct(x) for x in reg.values()])
        if ins[i] == 0:
            reg["A"] = int(reg["A"] / (2 ** combo(ins[i + 1])))
        elif ins[i] == 1:
            reg["B"] = reg["B"] ^ ins[i + 1]
        elif ins[i] == 2:
            reg["B"] = combo(ins[i + 1]) % 8
        elif ins[i] == 3:
            if reg["A"] != 0:
                i = ins[i + 1]
                i -= 2
        elif ins[i] == 4:
            reg["B"] = reg["B"] ^ reg["C"]
        elif ins[i] == 5:
            out.append(combo(ins[i + 1]) % 8)
            if p2:
                return out[-1]
        elif ins[i] == 6:
            reg["B"] = int(reg["A"] / (2 ** combo(ins[i + 1])))
        elif ins[i] == 7:
            reg["C"] = int(reg["A"] / (2 ** combo(ins[i + 1])))

        i += 2
    return out


print(",".join(str(x) for x in run(reg.copy(), inst)))

frontier = [(i * 8 ** (len(inst) - 1), len(inst) - 1) for i in range(8)]
a, b, c = 0, 0, 0
while frontier:
    guess_a, idx = frontier.pop(0)
    must_match = inst[idx:]
    out = run({"A": guess_a, "B": b, "C": c}, inst)
    out_section = out[idx:]
    if out_section == must_match:
        if idx == 0:
            a = guess_a
            break
        for i in range(8):
            frontier.append((guess_a + i * 8 ** (idx - 1), idx - 1))
print(a)
assert (
    ",".join(str(x) for x in run({"A": a, "B": b, "C": c}, inst))
    == "2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0"
)

# 2,4 # B = A % 8
# 1,2 # B ^= 2
# 7,5 # C = A
# 0,3 # A = A // 2^3
# 1,7 # B ^= 7
# 4,1 # B ^= C
# 5,5 # out(B%8)
# 3,0 # jmp 0 if A != 0
