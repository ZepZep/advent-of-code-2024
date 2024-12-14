from task import Task
import re
import numpy as np
from PIL import Image


TEST = False
# TEST = True
W = 11 if TEST else 101
H =  7 if TEST else 103

def parse(text):
    robots = []
    pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
    for m in re.finditer(pattern, text):
        robots.append([int(x) for x in m.groups()])
    return np.array(robots)


def predict(robots, seconds):
    robots[:, :2] += seconds * robots[:, 2:]
    robots[:, 0] %= W
    robots[:, 1] %= H

def count_quadrants(robots):
    wc = W//2
    hc = H//2

    mul = 1
    mul *= np.logical_and(robots[:,0] < wc, robots[:,1] < hc).sum()
    mul *= np.logical_and(robots[:,0] > wc, robots[:,1] < hc).sum()
    mul *= np.logical_and(robots[:,0] < wc, robots[:,1] > hc).sum()
    mul *= np.logical_and(robots[:,0] > wc, robots[:,1] > hc).sum()

    return mul

def save_img(robots, step):
    img = np.ones((W, H), dtype=np.uint8)*255
    img[robots[:,0], robots[:,1]] = 0
    Image.fromarray(img.T, mode="L").save(f"img/14/{step}.png")

def save_grid(robots, n, step):
    img = np.ones((W*n, H*n), dtype=np.uint8)*255
    for r in range(n):
        for c in range(n):
            img[robots[:,0]+c*W, robots[:,1]+r*H] = 0
            predict(robots, 1)
    Image.fromarray(img.T, mode="L").save(f"img/14/grid_{n}_{step}.png")

def center_treeness(robots, r):
    return (
        (W//2-r <= robots[:,0]) * (robots[:,0] < W//2+r)*
        (H//2-r <= robots[:,1]) * (robots[:,1] < H//2+r)
    ).sum()

def part1(text, timer):
    robots = parse(text)
    timer.parsed()
    predict(robots, 100)
    return count_quadrants(robots)

def part2(text, timer):
    robots = parse(text)
    timer.parsed()
    second = 0
    while center_treeness(robots, 2) < 10:
        second += 1
        predict(robots, 1)
    return second

    # predict(robots, 7585)
    # save_grid(robots, 10, 75)
    # save_img(robots, 7585)

task = Task(
    14,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    test=TEST,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

