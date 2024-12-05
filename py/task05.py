from task import Task
from collections import defaultdict


def parse(text):
    graph_text, manuals_text = text.split("\n\n")
    graph = load_graph(graph_text)
    manuals = [
        [int(page) for page in line.split(",")]
        for line in manuals_text.splitlines()
    ]

    return graph, manuals

def load_graph(text):
    graph = defaultdict(list)
    for line in text.splitlines():
        a, b = map(int, line.split("|"))
        graph[a].append(b)
    return graph

def get_starting(graph, subset):
    starting = subset.copy()
    for page in subset:
        for val in graph[page]:
            starting.discard(val)
    return starting

def print_graph(graph, subset):
    print("digraph G {")
    for page in subset:
        print(f"  {page}")
        for after in graph[page]:
            if after in subset:
                print(f"  {page} -> {after}")
    print("}")


def order_ok(graph, manual):
    banned = set([manual[0]])
    for page in manual[1:]:
        for should_be_after in graph[page]:
            # print(f"  {page}|{should_be_after}  {banned=}")
            if should_be_after in banned:
                return False
        banned.add(page)
    return True


def topological_order(graph, cur, subset, status, order):
    status[cur] = 1
    # print("start", cur, subset.intersection(graph[cur]))
    for child in graph[cur]:
        if child not in subset:
            continue
        child_status = status[child]
        if child_status == 1: # cycle
            # print("cycle", subset)
            raise Exception("Cycle in subgraph")
        if child_status == 2: # already visited
            continue
        topological_order(graph, child, subset, status, order)
    order.append(cur)
    status[cur] = 2


def get_correct_order(graph, manual):
    subset = set(manual)
    starting = get_starting(graph, subset)
    if len(starting) != 1:
        raise Exception("Multiple possible orderings: many starts")
    starting = list(starting)[0]

    status = defaultdict(int)
    order = []
    topological_order(graph, starting, subset, status, order)
    order = order[::-1]
    return order


def part1(text, timer):
    graph, manuals = parse(text)
    timer.parsed()

    total = 0
    for manual in manuals:
        if order_ok(graph, manual):
            total += manual[len(manual)//2]
    return total

def part2(text, timer):
    graph, manuals = parse(text)
    timer.parsed()

    for afters in graph.values():
        afters.sort()

    total = 0
    for manual in manuals:
        if not order_ok(graph, manual):
            ordered = get_correct_order(graph, manual)
            # print(ordered)
            total += ordered[len(ordered)//2]
    return total


task = Task(
    5,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

