from task import Task
import numpy as np
from dataclasses import dataclass
from typing import Optional
import time


def get_files(text):
    files = []
    pos = 0
    for i, char in enumerate(text):
        size = int(char)
        if i % 2 == 0:
            files.append(File(pos, size, i//2))
        pos += size
    files[0].r = files[1]
    files[-1].l = files[-2]
    for i in range(1, len(files)-1):
        files[i].l = files[i-1]
        files[i].r = files[i+1]
    return files

def expand(text):
    disk = []
    for i, char in enumerate(text):
        if i % 2 == 0:
            disk.extend([i//2]*int(char))
        else:
            disk.extend([-1]*int(char))
    return disk

def compact(disk):
    l = 0
    r = len(disk) - 1
    while l < r:
        if disk[l] != -1:
            l += 1
            continue
        if disk[r] == -1:
            r -= 1
            continue
        disk[l] = disk[r]
        disk[r] = -1
        l += 1
        r -= 1
    return r+1

def checksum(disk, check_len):
    total = 0
    for i in range(check_len):
        total += i * disk[i]
    return total

@dataclass
class File:
    pos: int
    size: int
    id: int
    is_gapl: int = 0
    l: Optional["File"] = None
    r: Optional["File"] = None


def move_left(f, gaps):
    gapl = gaps[f.size]
    while True:
        if gapl is None or gapl.pos >= f.pos:
            gaps[f.size] = None
            return
        if gapl.r is not None and gapl.r.pos >= gapl.pos + gapl.size + f.size:
            break
        if gapl.is_gapl & 2**f.size:
            gapl.is_gapl -= 2**f.size
        gapl = gapl.r
        if gapl is not None:
            gapl.is_gapl += 2**f.size
    gaps[f.size] = gapl

    gapr = gapl.r
    gapl.r = f
    if gapr is not None:
        gapr.l = f
    if f.l is not None:
        f.l.r = f.r
        if f.r is not None:
            f.r.l = f.l

    f.l = gapl
    f.r = gapr
    f.pos = gapl.pos + gapl.size
    if f.is_gapl:
        for i in range(1, 10):
            if f.is_gapl & 2**i:
                # print(f"moved gapl {f.id}")
                gaps[i] = None
        f.is_gapl = 0

def print_files(files):
    last_pos = 0
    f = files[0]
    while f is not None:
        print(f"."*(f.pos-last_pos), end="")
        print(f"{f.id}"*f.size, end="")
        last_pos = f.pos + f.size
        f = f.r
    print()

def files_checksum(files):
    total = 0
    for f in files:
        for i in range(f.pos, f.pos+f.size):
            total += f.id * i
    return total

def compact_whole(files):
    gaps = [files[0] for i in range(10)]
    for f in reversed(files):
        move_left(f, gaps)

def part1(text, timer):
    disk = expand(text)
    timer.parsed()

    new_len = compact(disk)
    return checksum(disk, new_len)


def part2(text, timer):
    files = get_files(text)
    timer.parsed()

    compact_whole(files)
    return files_checksum(files)

task = Task(
    9,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

