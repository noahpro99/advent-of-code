# %%
from functools import lru_cache

f = {
    x.split(": ")[0]: x.split(": ")[1].split()
    for x in open("input.txt").read().splitlines()
}


@lru_cache
def paths_through(cur: str) -> dict[str, int]:
    ret: dict[str, int] = {"out": 0, "dac": 0, "fft": 0, "both": 0}
    if cur == "out":
        ret["out"] += 1
        return ret
    for child in f[cur]:
        p = paths_through(child)
        ret = {k: v + p[k] for k, v in ret.items()}
    if cur == "dac":
        ret["dac"] += ret["out"]
        ret["both"] += ret["fft"]
    elif cur == "fft":
        ret["fft"] += ret["out"]
        ret["both"] += ret["dac"]
    return ret


print(paths_through("you")["out"])
print(paths_through("svr")["both"])

# %%
