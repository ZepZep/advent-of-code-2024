from task import Task
import numpy as np
from numba import njit, prange


MARK = ord("X")
WALL = ord("#")

def parse(text):
    a = np.frombuffer(bytes(text, "ascii"), dtype=np.uint8)
    a = np.append(a, [10]) # add missing newline
    width = a.argmin()
    return a.reshape((width, a.shape[0]//width))[:, :-1]

# row, col
deltas = np.array([
    [-1, 0], # up
    [0, 1], # right
    [1, 0], # down
    [0, -1], # left
])

def printlab(lab):
    print("\n".join(
        "".join(chr(c) for c in row) for row in lab
    ))

@njit
def is_in(lab, pos):
    return 0 <= pos[0] < lab.shape[0] and 0 <= pos[1] < lab.shape[1]

@njit
def go(lab, pos):
    dir = 0
    while True:
        lab[pos[0], pos[1]] = MARK
        new_pos = pos + deltas[dir]
        if not is_in(lab, new_pos):
            return
        if lab[new_pos[0], new_pos[1]] == WALL:
            dir = (dir + 1) % 4
            continue
        pos = new_pos

@njit(parallel=True)
def count_loops(lab, start_pos):
    path_lab = lab.copy()
    go(lab, start_pos)
    positions = (np.argwhere(lab == MARK))
    total = 0
    for i in prange(len(positions)):
        if check_loop(lab, positions[i], start_pos):
            # print(i)
            total += 1
    return total

@njit
def check_loop(lab, wall_pos, pos):
    if wall_pos[0] == pos[0] and wall_pos[1] == pos[1]:
        return False

    visited = np.zeros_like(lab, dtype=np.uint8)
    lab = lab.copy()
    lab[wall_pos[0], wall_pos[1]] = WALL

    dir = 0
    while True:
        # print(pos, visited[pos[0], pos[1]])
        if visited[pos[0], pos[1]] & 2**dir:
            return True
        visited[pos[0], pos[1]] |= 2**dir
        new_pos = pos + deltas[dir]
        if not is_in(lab, new_pos):
            return False
        if lab[new_pos[0], new_pos[1]] == WALL:
            dir = (dir + 1) % 4
            continue
        pos = new_pos


def part1(text, timer):
    lab = parse(text)
    timer.parsed()
    # printlab(lab)
    # print()
    pos = np.argwhere(lab == ord("^"))[0]
    go(lab, pos)
    # printlab(lab)
    return (lab == MARK).sum()

def part2(text, timer):
    lab = parse(text)
    timer.parsed()
    pos = np.argwhere(lab == ord("^"))[0]
    return count_loops(lab, pos)

task = Task(
    6,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

