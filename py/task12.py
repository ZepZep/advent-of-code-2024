from task import Task
import numpy as np
from numba import njit, prange

dirs = np.array([
    [0,1],
    [1,0],
    [0,-1],
    [-1,0],
])


def parse(text):
    a = np.frombuffer(bytes(text, "ascii"), dtype=np.uint8)
    a = np.append(a, [10]) # add missing newline
    width = a.argmin()
    return a.reshape((width, a.shape[0]//width))[:, :-1]


@njit
def is_in(arr, pos):
    return 0 <= pos[0] < arr.shape[0] and 0 <= pos[1] < arr.shape[1]

@njit
def find_fences(arr, mul_1, mul_2):
    visited = np.zeros_like(arr)
    total = 0
    results = np.array([0,0,0]) # area, fences, fence_segments
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            if not visited[r, c]:
                pos = np.array([r, c])
                results[:] = 0
                search_plot(arr, pos, visited, results)
                total += results[mul_1]*results[mul_2]
                # print(chr(arr[r,c]), results)

    return total

@njit
def search_plot(arr, pos, visited, results):
    results[0] += 1
    visited[pos[0], pos[1]] = 1
    results[2] += segment_count(arr, pos)
    cur_val = arr[pos[0], pos[1]]
    for dir in dirs:
        new_pos = pos + dir
        if not is_in(arr, new_pos):
            results[1] += 1
            continue
        if cur_val != arr[new_pos[0], new_pos[1]]:
            results[1] += 1
            continue
        if not visited[new_pos[0], new_pos[1]]:
            search_plot(arr, new_pos, visited, results)

@njit
def get_adir(arr, r, c):
    if 0 <= r < arr.shape[0] and 0 <= c < arr.shape[1]:
        return arr[r, c]
    return 0

@njit
def segment_count(arr, pos):
    count = 0
    tl = get_adir(arr, pos[0]-1, pos[1]-1)
    t  = get_adir(arr, pos[0]-1, pos[1]  )
    # tr = get_adir(arr, pos[0]-1, pos[1]+1)
    r  = get_adir(arr, pos[0],   pos[1]+1)
    br = get_adir(arr, pos[0]+1, pos[1]+1)
    b  = get_adir(arr, pos[0]+1, pos[1]  )
    # bl = get_adir(arr, pos[0]+1, pos[1]-1)
    l  = get_adir(arr, pos[0],   pos[1]-1)
    cur = arr[pos[0], pos[1]]

    if t != cur and l != cur:
        count += 2
    elif tl == cur and (t != cur or l != cur):
        count += 1

    if r != cur and b != cur:
        count += 2
    elif br == cur and (r != cur or b != cur):
        count += 1

    return count


def part1(text, timer):
    arr = parse(text)
    timer.parsed()
    return find_fences(arr, 0, 1)


def part2(text, timer):
    arr = parse(text)
    timer.parsed()
    return find_fences(arr, 0, 2)

task = Task(
    12,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

