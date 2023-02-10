from collections import Counter, defaultdict, deque
from collections.abc import Callable

"""
The strategy here is as follows:

It does these swaps in the stated order:

* smart swap: swaps two bad characters (char which doesn't match with the correct instruction) 
    which then both are correct, it does this from most left possible first
* half smart swap: swap two bad chars in such way that it creates a new possible future smart swap
* swaps two bad characters so that it doesnt remove a smart swap
* bad swap, does a swap so that it removes a smart swap

the order of the individual swaps matters even though this wasn't mentioned else it wont match the output, 
thus the left to right requirement

another indirect requirement is that it needs to swap the most left bad letter with the best possible swap its most left letter,
else we produce a sequence that would not be alphabetically first, since lower indexes are earlier letters in the alphabet
should reduce the need of a brute force tree


BUT

a brute force tree is much easier to implement and since the input size is limited to 26 chars, it will be sufficient fast enough


"""

ASCII_OFFSET = 65

"""
Remnants of the smarter implementation

# returns a map from a good letter to a list of bad/wrong letter positions
def get_mapping(bad_instr, good_instr):
    good2bad_map = defaultdict(lambda _: defaultdict(list))  # love these things
    for idx, c in enumerate(good_instr):
        if c == bad_instr[idx]: continue
        good2bad_map[c][bad_instr[idx]].append(idx)  #
    return good2bad_map

smart_map = get_mapping(bad_instruction, good_instruction)
char_list = list(bad_instruction)
for idx, c in enumerate(char_list):
    if c == good_instruction[idx]: continue
    if c in smart_map and good_instruction[idx] in smart_map[c]:  # can do a smart swap
        smart_pos = smart_map[c][good_instruction[idx]].pop(0)
        output += chr(ASCII_OFFSET + idx) + chr(ASCII_OFFSET + smart_pos)
        char_list[idx], char_list[smart_pos] = char_list[smart_pos], char_list[idx]
    # todo impl half smart swap: swaps a char with a char that original could not be used for a smart swap but now with is new position can
    else
"""


def is_possible(bad_instruction, good_instruction):
    count_bad = Counter(bad_instruction)
    count_good = Counter(good_instruction)
    return count_bad == count_good


def swap_return(string, from_pos, to_pos):
    instr = list(string)
    instr[from_pos], instr[to_pos] = instr[to_pos], instr[from_pos]
    return "".join(instr)


def first_nonmatching_char_pos(to, target):
    for idx, c in enumerate(to):
        if c != target[idx]:
            return idx
    return -1  # matches perfectly


class Node:
    def __init__(self, instruction, sequence, depth=0):
        self.instruction = instruction
        self.sequence = sequence
        self.children = []
        self.depth = depth

    def __str__(self): return self.instruction

    def __repr__(self): return self.__str__()

    def make_child(self, instruction, subsequence):
        return Node(instruction, self.sequence + subsequence, self.depth + 1)


def walk(root: Node, target):
    queue = deque([root])
    solutions = set()

    while len(queue) > 0:
        cur_node = queue.popleft()

        idx = first_nonmatching_char_pos(cur_node.instruction, target)
        for replace_idx in range(idx + 1, len(target)):  # swap range
            if cur_node.instruction[replace_idx] == target[replace_idx]: continue  # cant swap an already correct letter
            if target[idx] != cur_node.instruction[replace_idx]: continue  # needs to swap with a correct letter
            new_node = cur_node.make_child(swap_return(cur_node.instruction, idx, replace_idx),
                                           chr(ASCII_OFFSET + idx) + chr(ASCII_OFFSET + replace_idx))
            cur_node.children.append(new_node)
            if new_node.instruction == target:
                solutions.add(new_node.sequence)
                while queue and queue[-1].depth == new_node.depth:  # removes elements from the next depth, found solution at this depth already
                    queue.pop()
        if not solutions:  # if it found a solution let it complete that depth so that it may find our solutions that could maybe alphabetically be better
            queue.extend(cur_node.children)
            cur_node.children.clear()  # saves memory but destroys the tree structure for so only keep for debuggging, (keeps all the nodes in a tree alive)

    if not solutions:  # shouldn't be possible, but in case
        return "onmogelijk"

    return sorted(solutions)[0]


test_cases = int(input())

for i in range(test_cases):
    bad_instruction = input()
    good_instruction = input()

    output = ""
    if bad_instruction == good_instruction:
        output = "correct"
    elif not is_possible(bad_instruction, good_instruction):
        output = "onmogelijk"
    else:
        output = walk(Node(bad_instruction, ""), good_instruction)
    print(f"{i + 1} {output}")
