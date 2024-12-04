from task import Task
# from numba import njit, int32
# from numba.experimental import jitclass
#
# @jitclass([
#     ("r", int32),
#     ("c", int32)
# ])
class Pos:
    __slots__ = "r", "c"
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __add__(self, other):
        return Pos(self.r+other.r, self.c+other.c)


directions = [
    Pos(0, 1),
    Pos(1, 0),
    Pos(0, -1),
    Pos(-1, 0),
    Pos(1, 1),
    Pos(-1, 1),
    Pos(1, -1),
    Pos(-1, -1),
]

# @njit
def is_in(pos, lines):
    if pos.r < 0 or pos.r >= len(lines):
        return False
    if pos.c < 0 or pos.c >= len(lines[0]):
        return False
    return True

# @njit
def check_from(lines, pos, pattern, dir):
    start_pos = pos
    for char in pattern:
        if not is_in(pos, lines):
            return False
        if lines[pos.r][pos.c] != char:
            return False
        pos = pos + dir
    # found.append((start_pos.r, start_pos.c, dir.r, dir.c))
    return True

# @njit
def count_at_each(lines, pattern):
    count = 0
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            for dir in directions:
                if check_from(lines, Pos(r, c), pattern, dir):
                    count += 1
    return count

# @njit
def check_x_form(lines, pos, pattern, apattern):
    leg1 = check_from(lines, pos, pattern, Pos(1,1)) or check_from(lines, pos, apattern, Pos(1,1))
    leg2 = check_from(lines, pos+Pos(0, 2), pattern, Pos(1,-1)) or check_from(lines, pos+Pos(0, 2), apattern, Pos(1,-1))
    return leg1 and leg2

# @njit
def count_at_each_x(lines, pattern):
    count = 0
    apattern = pattern[::-1]
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if check_x_form(lines, Pos(r, c), pattern, apattern):
                count += 1
    return count

def part1(text, timer):
    lines = text.splitlines()
    timer.parsed()
    count = count_at_each(lines, "XMAS")
    return count

def part2(text, timer):
    lines = text.splitlines()
    timer.parsed()
    count = count_at_each_x(lines, "MAS")
    return count

task = Task(
    4,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

