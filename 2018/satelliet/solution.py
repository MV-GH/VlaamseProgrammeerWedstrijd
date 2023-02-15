from collections import deque

"""
The strategy here is:

A brute force tree, didn't find any smarter method atm
Constructs bread first and each level contains a replaced lettercode
Thus when a solution is found, on has the only complete that depth to find other possible solutions which can come alphabetically first

Not efficient enough for the wedstrijd.invoer, (mostly in space complexity, eats up 12GB before i gotta kill it)

NEW STRATEGY??!

A tree with on each depth a new combination thats replaced, stop at that depth when a solution is found but complete
the depth to find possible other solutions
Start with longest lettercode and replace if possible
if lettercodes with same length, then do em all but swap between but do the letter alphabettically first
(codes with same length must have alphabetically first as solution)
when no solution on that depth is found, backtrack one depth and try an other combination

"""

test_cases = int(input())
codes = []


class Node:
    def __init__(self, name, depth=0):
        self.name = name
        self.children = []
        self.depth = depth

    def __str__(self): return self.name

    def __repr__(self): return self.__str__()

    def make_child(self, name):
        return Node(name, self.depth + 1)


def walk(root: Node, alphabet):
    queue = deque([root])
    solutions = set()

    while len(queue) > 0:
        cur_node = queue.popleft()

        for key in sorted_keys:
            new_code = cur_node.name.replace(alphabet[key], key, 1)
            if new_code != cur_node.name:
                if not ('0' in new_code or '1' in new_code):
                    solutions.add(new_code)
                    while queue and queue[-1].depth == cur_node.depth + 1:  # removes elements from the next depth, found solution at this depth already
                        queue.pop()
                    break

                new_node = cur_node.make_child(new_code)
                cur_node.children.append(new_node)
        if not solutions:  # if it found a solution let it complete that depth so that it may find our solutions that could may be alphabetically be better
            queue.extend(cur_node.children)
            cur_node.children.clear()  # saves memory but destroys the tree structure for so only keep for debuggging, (keeps all the nodes in a tree alive)

    if not solutions:
        return "ONMOGELIJK"

    return sorted(solutions)[0]


for i in range(test_cases):
    code = input()
    alphabet_len = int(input())
    alphabet = {}

    for _ in range(alphabet_len):
        key = input()
        val = input()
        alphabet[key] = val

    sorted_keys = sorted(alphabet)  # sort alphabetically as secondary sort, as we need shortest alphabetically first code
    sorted_keys = sorted(sorted_keys, key=lambda x: len(alphabet[x]), reverse=True)  # sort based on code length, as we need shorted codes

    root = Node(code)
    print(f'{i + 1} {walk(root, alphabet)}')
