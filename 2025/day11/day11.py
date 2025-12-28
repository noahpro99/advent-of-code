# %%
from functools import lru_cache

f = {
    x.split(": ")[0]: x.split(": ")[1].split()
    for x in open("input.txt").read().splitlines()
}


@lru_cache
def paths_through(cur: str) -> dict[str, int]:
    ret: dict[str, int] = {"none": 0, "dac": 0, "fft": 0, "both": 0}
    if cur == "out":
        ret["none"] += 1
        return ret
    for child in f[cur]:
        p = paths_through(child)
        ret = {k: v + p[k] for k, v in ret.items()}
    if cur == "dac":
        ret["dac"] += ret["none"]
        ret["none"] = 0
        ret["both"] += ret["fft"]
        ret["fft"] = 0
    elif cur == "fft":
        ret["fft"] += ret["none"]
        ret["none"] = 0
        ret["both"] += ret["dac"]
        ret["dac"] = 0
    return ret


print(sum(paths_through("you").values()))
print(paths_through("svr")["both"])
