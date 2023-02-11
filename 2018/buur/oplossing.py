from collections import deque

"""
The strategy here is:

We convert the input into a graph structure,
and using this structure we can easily count the neighbors
as a connection between two nodes

The hard part is turning the input into a graph structure,
for that, I keep a position to node map for O(1) look up
I loop over every undefined position in that node map, each not defined is a new node
which i then expand as much as possible to discover its size and define it then in the map, 
all the other neighbor nodes it finds the in the process will be added 
"""


class Node:
    __id = 0

    def __init__(self, land):
        self.land = land
        self.neighbors = set()  # set bc it ignore duplicates

        self.id = Node.__id
        Node.__id += 1

    def __str__(self): return self.land

    def __repr__(self): return self.__str__()


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Point:
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y

    # add two points but having them be bound by the third point, offset since arrays start at 0
    def add_but_bound(self, other, upperbound, offset=-1):
        return Point(clamp(self.X + other.X, 0, upperbound.X + offset), clamp(self.Y + other.Y, 0, upperbound.Y + offset))

    def get(self, array2d: [[]]):
        return array2d[self.Y][self.X]

    def set(self, array2d: [[]], value):
        array2d[self.Y][self.X] = value

    def __add__(self, other):
        return Point(self.X + other.X, self.Y + other.Y)

    def __str__(self):
        return f'{{X:{self.X} Y:{self.Y}}}'

    def __repr__(self):
        return self.__str__()


directions = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]


def make_2d_list(size):
    base = []
    for _ in range(size.Y):
        base.append([None] * size.X)
    return base


def gen_graph(map, mapsize):
    coords2nodes = make_2d_list(mapsize)

    for row in range(mapsize.Y):
        for col in range(mapsize.X):
            if coords2nodes[row][col] is not None: continue  # skip defined positions

            cur_node = Node(map[row][col])
            coords2nodes[row][col] = cur_node
            queue = deque([Point(col, row)])

            while queue:
                cur_pos = queue.popleft()
                for direction in directions:
                    next_pos = cur_pos.add_but_bound(direction, mapsize)
                    next_node = next_pos.get(coords2nodes)
                    if next_node is None and next_pos.get(map) == cur_node.land:
                        next_pos.set(coords2nodes, cur_node)
                        queue.append(next_pos)
                    elif next_node is not None and next_node != cur_node:  # become neighbors
                        next_node.neighbors.add(cur_node)
                        cur_node.neighbors.add(next_node)

    return coords2nodes


test_cases = int(input())

for i in range(test_cases):
    w, h = map(int, input().split())
    land_map = []

    for _ in range(h):
        land_map.append(list(input()))

    node_map = gen_graph(land_map, Point(w, h))

    for h_i in range(h):
        print(f"{i + 1} {' '.join(str(len(x.neighbors)) for x in node_map[h_i])}")
