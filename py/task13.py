from task import Task
import re
from decimal import Decimal

# a * ax + b * bx = cx
# a * ay + b * by = cy
#
# b = (cx - a * ax) / bx
#
# a * ay + (cx - a * ax) / bx * by = cy
# a * ay + cx/bx*by - a*ax/bx*by = cy
# a * (ay - ax/bx*by) = cy - cx/bx*by
# a = (cy - cx/bx*by) / (ay - ax/bx*by)

def parse(text):
    machines = []
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    for m in re.finditer(pattern, text):
        machines.append([int(x) for x in m.groups()])
    return machines


def solve(machine):
    ax, ay, bx, by, cx, cy = machine
    a = round((cy - cx/bx*by) / (ay - ax/bx*by))
    b = round((cx - a * ax) / bx)
    if a * ax + b * bx != cx:
        return None, None
    if a * ay + b * by != cy:
        return None, None
    return a, b

def part1(text, timer):
    machines = parse(text)
    timer.parsed()

    tickets = 0
    for machine in machines:
        a, b = solve(machine)
        if a is None:
            continue
        tickets += 3*a + b

    return tickets

def part2(text, timer):
    machines = parse(text)
    timer.parsed()

    tickets = 0
    for machine in machines:
        # machine = [Decimal(x) for x in machine]
        machine[-2] += 10000000000000
        machine[-1] += 10000000000000
        a, b = solve(machine)
        # print(a, b)
        if a is None:
            continue
        tickets += 3*a + b

    return tickets


task = Task(
    13,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

