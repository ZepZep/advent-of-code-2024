from task import Task
from collections import defaultdict
from itertools import permutations, combinations

class Pos:
    __slots__ = "r", "c"
    def __init__(self, r, c):
        self.r = r
        self.c = c

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

    def __str__(self):
        return f"Pos({self.r}, {self.c})"

    def __repr__(self):
        return f"Pos({self.r}, {self.c})"

    def __hash__(self):
        return hash((self.r, self.c))

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

def get_antenas(city):
    antenas = defaultdict(list)
    for r, line in enumerate(city):
        for c, char in enumerate(line):
            if char != ".":
                antenas[char].append(Pos(r, c))
    return antenas

def get_hotspots(city, antenas):
    hotspots = set()
    for freq, positions in  antenas.items():
        for p1, p2 in permutations(positions, 2):
            hpos = p1 + (p1-p2)
            if hpos.inside(city):
                hotspots.add(hpos)
    return hotspots

def get_hotspots_grid(city, antenas):
    hotspots = set()
    for freq, positions in  antenas.items():
        for p1, p2 in combinations(positions, 2):
            cur = p1
            delta = p2 - p1
            while cur.inside(city):
                hotspots.add(cur)
                cur += delta
            cur = p2
            delta = p1 - p2
            while cur.inside(city):
                hotspots.add(cur)
                cur += delta
    return hotspots

def part1(text, timer):
    city = text.splitlines()
    timer.parsed()
    antenas = get_antenas(city)
    hotspots = get_hotspots(city, antenas)
    return len(hotspots)


def part2(text, timer):
    city = text.splitlines()
    timer.parsed()
    antenas = get_antenas(city)
    hotspots = get_hotspots_grid(city, antenas)
    return len(hotspots)

task = Task(
    8,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

