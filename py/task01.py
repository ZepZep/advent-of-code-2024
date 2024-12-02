from task import Task
import numpy as np
from io import StringIO


def part1(text, timer):
    c = StringIO(text)
    arr = np.loadtxt(c, dtype=int)
    timer.parsed()

    arr.sort(axis=0)
    return np.abs(arr[:,0]-arr[:,1]).sum()

def part2(text, timer):
    c = StringIO(text)
    arr = np.loadtxt(c, dtype=int)
    timer.parsed()

    l,lc = np.unique(arr[:,0], return_counts=True)
    r,rc = np.unique(arr[:,1], return_counts=True)

    total = 0
    li = 0
    ri = 0
    while li < len(l) and ri < len(r):
        if r[ri] < l[li]:
            ri += 1
            continue
        if r[ri] == l[li]:
            total += r[ri] * rc[ri] * lc[li]
            ri += 1
        li += 1

    return total

task = Task(
    1,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

