# %%
f = open("input.txt").read()
reg = {
    l.split(" ")[1].split(":")[0]: int(l.split(": ")[1])
    for l in f.split("\n\n")[0].split("\n")
}
inst = [
    int(x) for l in f.split("\n\n")[1].split("\n") for x in l.split(": ")[1].split(",")
]
reg, inst

# %%


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

# %%
ans = 0
b, c = 0, 0
for i, ins in enumerate(inst):
    a = 0
    while True:
        trial_reg = {"A": a, "B": b, "C": c}
        out = run(trial_reg, inst, p2=True)
        if isinstance(out, int) and out == ins:
            print(i, a, b, c, out)
            b = a
            b ^= 2
            c = a
            b ^= 7
            b ^= c
            ans = 8 * ans + a
            break
        a += 1
    # if i == 2:
    #     break
# convert back to decimal
print(ans, oct(ans))
test_reg = reg.copy()
test_reg["A"] = 0o5325644676236017
print(",".join(str(x) for x in run(test_reg, inst)))
# 190615597431823 0o5325644676236017
# %%

# 2,4 # B = A
# 1,2 # B ^= 2
# 7,5 # C = A
# 0,3 # A = A // 2^3
# 1,7 # B ^= 7
# 4,1 # B ^= C
# 5,5 # out(B%8)
# 3,0 # jmp 0 if A != 0


def recreation(a, b, c):
    out = []
    while a != 0:
        b = a
        b ^= 2
        c = a
        a = a // 8
        b ^= 7
        b ^= c
        out.append(b % 8)
    return a, b, c, out


recreation(0o7, 0, 0)
