from task import Task
from multiprocessing import Pool

def parse(text):
    equations = []
    for line in text.splitlines():
        l = line.split(": ")
        target = int(l[0])
        values = [int(x) for x in l[1].split(" ")]
        equations.append((target, values))

    return equations

def concat(a, b):
    return int(str(a)+str(b))

def is_posible(target, cur, values, index, concat_op=False):
    if index >= len(values):
        return target == cur
    if cur > target:
        return False
    return (
        is_posible(target, cur*values[index], values, index+1, concat_op) or
        is_posible(target, cur+values[index], values, index+1, concat_op) or
        (concat_op and is_posible(target, concat(cur, values[index]), values, index+1, concat_op))
    )

def is_posible_mp(args):
    return is_posible(*args)


def part1(text, timer):
    equations = parse(text)
    timer.parsed()
    total = 0
    args = [(target, values[0], values, 1) for target, values in equations]
    with Pool(8) as p:
        for ok, (target, values) in zip(p.imap(is_posible_mp, args, chunksize=10), equations):
            if ok:
                total += target
    return total

def part2(text, timer):
    equations = parse(text)
    timer.parsed()
    total = 0
    args = [(target, values[0], values, 1, True) for target, values in equations]
    with Pool(8) as p:
        for ok, (target, values) in zip(p.imap(is_posible_mp, args, chunksize=10), equations):
            if ok:
                total += target
    return total

task = Task(
    7,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

