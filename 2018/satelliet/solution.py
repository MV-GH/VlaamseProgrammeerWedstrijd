from collections import deque

test_cases = int(input())
codes = []


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def __str__(self): return self.name

    def __repr__(self): return self.__str__()


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
                    break

                new_node = Node(new_code)
                cur_node.children.append(new_node)
        if not solutions:  # if it found a solution let it complete that depth so that it may find our solutions that could may be alphabetically be better
            queue.extend(cur_node.children)
            cur_node.children.clear() # saves memory but destroys the tree structure for so only keep for debuggging, (keeps all the nodes in a tree alive)

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
