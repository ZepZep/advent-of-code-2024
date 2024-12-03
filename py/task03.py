from task import Task
import re


def part1(text, timer):
    timer.parsed()
    total = 0
    for m in re.finditer(r"mul\((\d+),(\d+)\)", text):
        a = int(m.group(1))
        b = int(m.group(2))
        total += a*b

    return total

def part2(text, timer):
    timer.parsed()
    total = 0
    enabled = True
    for m in re.finditer(r"(do)\(\)|(don't)\(\)|(mul)\((\d+),(\d+)\)", text):
        if m.group(1):
            enabled = True
        elif m.group(2):
            enabled = False
        elif enabled:
            a = int(m.group(4))
            b = int(m.group(5))
            total += a*b
    return total

task = Task(
    3,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True, testnum=2,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

