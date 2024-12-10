line = open("input.txt").read()
new_line, entries, id, bi, enabled = [], [], 0, 0, True
for i, c in enumerate(line):
    n = int(c)
    entries.append({"block": bi, "id": id, "is_file": enabled, "size": n})
    for j in range(n):
        new_line.append(id if enabled else ".")
        bi += 1
    id += 1 if enabled else 0
    enabled = not enabled
new_line2 = new_line.copy()
p1, i = 0, 0
end_point = len(new_line) - 1
while i < end_point + 1:
    if new_line[i] != ".":
        p1 += i * int(new_line[i])
    else:
        while new_line[end_point] == ".":
            end_point -= 1
        if i > end_point:
            break
        p1 += i * int(new_line[end_point])
        end_point -= 1
    i += 1
print(p1)

files = [x for x in entries if x["is_file"]]
gaps = [x for x in entries if not x["is_file"]]
for i, entry in enumerate(reversed(files)):
    for gi in range(len(gaps)):
        if gaps[gi]["block"] >= entry["block"]:
            break
        if gaps[gi]["size"] >= entry["size"]:
            for j in range(entry["size"]):
                new_line2[gaps[gi]["block"] + j] = entry["id"]
                new_line2[entry["block"] + j] = "."
            gaps[gi]["block"] += entry["size"]
            gaps[gi]["size"] -= entry["size"]
            break
p2 = 0
for i, c in enumerate(new_line2):
    if c != ".":
        p2 += i * int(c)

print(p2)
# 6201130364722
# 6221662795602
