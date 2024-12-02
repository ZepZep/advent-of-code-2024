from task import Task
import numpy as np

from numba import njit

def parse(text):
    arrs = []
    for line in text.splitlines():
        arrs.append(np.array([int(x) for x in line.split()]))
    return arrs

# @njit
def get_safe_1(arrs):
    safe = 0
    for arr in arrs:
        if is_safe(arr):
            safe += 1

    return safe

@njit
def is_safe(arr):
    diffs = np.diff(arr)
    l = diffs.min()
    r = diffs.max()
    if l * r < 0:
        return False

    l = abs(l)
    r = abs(r)
    if l > r:
        l, r = r, l

    if l < 1:
        return False
    if r > 3:
        return False

    return True

@njit
def test_one_error(arr):
    for to_skip in range(len(arr)):
        indexer = np.delete(np.arange(len(arr)), to_skip)
        # indexer = [i  for i in range(len(arr)) if i != to_skip]
        if is_safe(arr[indexer]):
            return True
    return False

def part1(text, timer):
    arrs = parse(text)
    timer.parsed()
    return get_safe_1(arrs)


def part2(text, timer):
    arrs = parse(text)
    timer.parsed()

    safe = 0
    for arr in arrs:
        if is_safe(arr):
            safe += 1
            continue
        if test_one_error(arr):
            safe += 1
            continue

    return safe



# def is_ok(l, r, dir):
#     if dir == 1 and l > r:
#         return False
#     return 1 <= abs(l-r) <= 3

# def part2(text, timer):
#     arrs = parse(text)
#     timer.parsed()
#
#     max_errors = 1
#     safe = 0
#     for arr in arrs:
#         if len(arr) <= 2:
#             safe += 1
#             continue
#
#         dir = 1 if arr[0] < arr[1] else -1
#         last_val = arr[0]
#         errors = 0
#         for val in arr[1:]:
#             if not is_ok(last_val, val, dir):
#                 errors += 1
#             if errors > max_errors:
#                 break
#             last_val = val
#         if errors <= max_errors:
#             safe += 1
#
#     return safe

#
# a b c d
# ^ - ^
#   ^ - ^

task = Task(
    2,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

