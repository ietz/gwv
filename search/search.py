import copy
import time


world = [[]]
goals = []
portals = {}


def main():
    global world, goals, portals

    f = open("blatt3_environment.txt", "r")
    world = [list(line.rstrip()) for line in f]
    start = find("s")[0]
    goals = find('g')
    portals = find_portals()

    # Uncomment first line for breadth first or second line for depth first
    search(start, QueueFrontier, multiple_path_pruning)
    # search(start, StackFrontier, circle_checking)


def output(visited, path, neighbours=None):
    if neighbours is None:
        neighbours = {}

    display = copy.deepcopy(world)

    put(display, '-', visited)
    put(display, '+', path)
    put(display, '#', neighbours)

    print_colorized(display)


def put(matrix, value, positions):
    height = len(matrix)
    width = len(matrix[1])
    for (x, y) in positions:
        if x in range(width) and y in range(height):
            matrix[y][x] = value


def print_colorized(matrix):
    colors = {
        '-': '\033[34m',
        '+': '\033[33m',
        '#': '\033[31m',
        'x': '\033[37m'
    }

    for row in matrix:
        for cell in row:
            if cell in colors:
                print(colors[cell] + cell + '\033[0m', end='')
            else:
                print(cell, end='')

        print()


def in_frontier(position, frontier):
    for path in frontier:
        if position in path:
            return True

    return False


def search(start, frontier_class, pruning_method):
    frontier = frontier_class(start)
    visited = {start}

    while not frontier.is_empty():
        time.sleep(1)

        path = frontier.get_next()
        (x, y) = current = path[len(path) - 1]

        if current in goals:
            output(world, visited, path)
            return path

        else:
            pruned_neighbours = pruning_method(path, get_free_neighbours(x, y), visited)

            output(visited, path, pruned_neighbours)

            frontier.add(path, pruned_neighbours)

            for n in pruned_neighbours:
                visited.add(n)


def circle_checking(path, neighbours, visited):
    return [n for n in neighbours if n not in path]


def multiple_path_pruning(path, neighbours, visited):
    return [n for n in neighbours if n not in visited]


def find(value):
    results = list()

    for y in range(len(world)):
        line = world[y]
        for x in range(len(line)):
            field = line[x]

            if field == value:
                results.append((x, y))

    return results


def find_portals():
    result = {}

    for n in range(10):
        portal = find(str(n))

        if len(portal) == 0:
            continue

        [a, b] = portal

        result[a] = b
        result[b] = a

    return result


def teleport(position):
    if position in portals:
        return portals[position]
    else:
        return position


def get_free_neighbours(x, y):
    direct_neighbours = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]  # l,o,r,u
    neighbours = [teleport(p) for p in direct_neighbours]  # portals

    return [n for n in neighbours if get_field(n[0], n[1]) != 'x']


def get_field(x, y):
    if y < 0 or y >= len(world) or x < 0 or x >= len(world[0]):
        return ' '
    else:
        return world[y][x]


class Frontier:
    def is_empty(self):
        return False

    def get_next(self):
        return []

    def add(self, path, extensions):
        return


class QueueFrontier(Frontier):
    def __init__(self, start):
        self.content = [[start]]

    def is_empty(self):
        return len(self.content) == 0

    def get_next(self):
        return self.content.pop(0)

    def add(self, path, extensions):
        for extension in extensions:
            new_path = path[:]
            new_path.append(extension)
            self.content.append(new_path)


class StackFrontier(Frontier):
    def __init__(self, start):
        self.content = [[start]]

    def is_empty(self):
        return len(self.content) == 0

    def get_next(self):
        return self.content.pop(0)

    def add(self, path, extensions):
        for extension in reversed(extensions):
            new_path = path[:]
            new_path.append(extension)
            self.content.insert(0, new_path)


if __name__ == "__main__":
    main()
