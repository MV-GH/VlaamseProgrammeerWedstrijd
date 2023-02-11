"""
The strategy here is:

We convert the input into a graph structure,
and using this structure we can easily count the neighbors
as a connection between two nodes

The hard part is turning the input into a graph structure,
for that I use a, top-left approach,  I check each letter,
then its left/top neighbor, if they are same, they be put in the same node
else considered as bordering neighbor
"""


class Node:
    __id = 0

    def __init__(self, land):
        self.land = land
        self.neighbors = set()

        self.id = Node.__id
        Node.__id += 1

    def __str__(self): return self.land

    def __repr__(self): return self.__str__()


def make_2d_list(w, h):
    base = []
    for _ in range(h):
        base.append([None] * w)
    return base


def gen_graph(map, w, h):
    coords2nodes = make_2d_list(w, h)

    for row in range(h):
        for col in range(w):
            land = map[row][col]
            cur_node = None
            has_top_neighbor = False
            has_left_neighbor = False

            if row > 0:
                top_land = map[row - 1][col]
                top_node = coords2nodes[row - 1][col]

                if top_land == land:
                    cur_node = top_node
                else:
                    has_top_neighbor = True

            if col > 0:
                left_land = map[row][col - 1]
                left_node = coords2nodes[row][col - 1]

                if left_land == land:
                    cur_node = left_node
                else:
                    has_left_neighbor = True

            if cur_node is None:
                cur_node = Node(land)
            if has_top_neighbor:
                top_node = coords2nodes[row - 1][col]
                cur_node.neighbors.add(top_node)
                top_node.neighbors.add(cur_node)
            if has_left_neighbor:
                left_node = coords2nodes[row][col - 1]
                cur_node.neighbors.add(left_node)
                left_node.neighbors.add(cur_node)

            coords2nodes[row][col] = cur_node
    return coords2nodes


test_cases = int(input())

for i in range(test_cases):
    w, h = map(int, input().split())
    land_map = []

    for _ in range(h):
        land_map.append(list(input()))

    node_map = gen_graph(land_map, w, h)

    for h_i in range(h):
        print(f"{i + 1} {' '.join(str(len(x.neighbors)) for x in node_map[h_i])}")
