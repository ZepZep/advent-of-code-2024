from task import Task
from collections import defaultdict

def parse(text):
    sd = defaultdict(int)
    for numstr in text.split(" "):
        sd[int(numstr)] += 1
    return sd

def blink_dict(sd):
    nsd = defaultdict(int)
    for num, count in sd.items():
        if num == 0:
            nsd[1] += count
            continue

        numstr = str(num)
        numlen = len(numstr)
        if numlen % 2 == 0:
            nsd[int(numstr[:numlen//2])] += count
            nsd[int(numstr[numlen//2:])] += count
            continue

        nsd[num*2024] += count
    return nsd


def part1(text, timer):
    sd = parse(text)
    timer.parsed()

    for i in range(25):
        sd = blink_dict(sd)
    return sum(sd.values())


def part2(text, timer):
    sd = parse(text)
    timer.parsed()

    for i in range(75):
        sd = blink_dict(sd)
    return sum(sd.values())

task = Task(
    11,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

