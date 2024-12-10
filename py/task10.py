from task import Task
from dataclasses import dataclass

@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r+other.r, self.c+other.c)

    def __sub__(self, other):
        return Pos(self.r-other.r, self.c-other.c)

    def inside(self, city):
        if self.r < 0 or self.r >= len(city):
            return False
        if self.c < 0 or self.c >= len(city[0]):
            return False
        return True

class AddList(list):
    def add(self, x):
        self.append(x)

deltas = [
    Pos(0, 1),
    Pos(1, 0),
    Pos(0, -1),
    Pos(-1, 0),
]

def parse(text):
    return [[int(x) for x in line] for line in text.splitlines()]

def get_score(arr, pos):
    found = set()
    _get_score(arr, pos, found)
    return len(found)

def get_score_trails(arr, pos):
    found = AddList()
    _get_score(arr, pos, found)
    return len(found)

def _get_score(arr, pos, found):
    h = arr[pos.r][pos.c]
    for delta in deltas:
        new_pos = pos + delta
        if not new_pos.inside(arr):
            continue
        new_h = arr[new_pos.r][new_pos.c]
        if new_h != h+1:
            continue
        if new_h == 9:
            found.add(new_pos)
            continue
        _get_score(arr, new_pos, found)

def part1(text, timer):
    arr = parse(text)
    timer.parsed()

    total = 0
    for r, line in enumerate(arr):
        for c, h  in enumerate(line):
            if h == 0:
                total += get_score(arr, Pos(r, c))
    return total

def part2(text, timer):
    arr = parse(text)
    timer.parsed()

    total = 0
    for r, line in enumerate(arr):
        for c, h  in enumerate(line):
            if h == 0:
                total += get_score_trails(arr, Pos(r, c))
    return total

task = Task(
    10,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

