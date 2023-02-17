from collections import deque, OrderedDict, defaultdict

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


class Node:
    def __init__(self, name, depth=0, letter=""):
        self.name = name
        self.letters = letter
        self.children = []
        self.depth = depth

    def __str__(self): return self.letters

    def __repr__(self): return self.__str__()

    def make_child(self, name, letter):
        return Node(name, self.depth + 1, self.letters + letter)


"""
#TODO:
Converts the given alphabet into a list of lists, which contain the the longest combination
replacer to the shortest combination replacement with each sublist sorted alphabetically, since we 
need to reproduce the alphabetically first shortest combination
"""


def sort_alphabet(alphabet):
    sorted_keys = sorted(alphabet)  # sort alphabetically as secondary sort
    # sort based on code replacement length as primary sort
    sorted_keys = sorted(sorted_keys, key=lambda x: len(alphabet[x]), reverse=True)
    # now we have a list sorted on code replacement length and secondary alphabetically
    # (when same length, sort alphabetically)
    sorted_dict = OrderedDict()
    for key in sorted_keys:
        sorted_dict[key] = alphabet[key]
    return sorted_dict


"""
Efficiently check if a code still possible is to solve
A code is still able to be solved if each subcode (not replaced codes by letters)
still has a possible replacement, we can do this efficiently by having a 
pre computed string containing the possible replacement codes, 
if it is a substring of that string its possible
"""


def gen_blacklist(ordered_alpha: OrderedDict):
    blacklist = defaultdict(list)
    copy_alphabet = ordered_alpha.copy()
    for key in ordered_alpha:
        replacement = ordered_alpha[key]
        if len(replacement) < 2:
            break
        del copy_alphabet[key]  # remove itself, else would return itself as possible solution, and longer codes not possible anyway
        solutions = solve(Node(replacement), copy_alphabet)
        if solutions != ["ONMOGELIJK"]:
            for sol in solutions:
                blacklist[sol[-1]].append(sol[0:-1])  # appends the solution of chars upto the last char to the last char list

    return blacklist


def solve(root: Node, alphabet, blacklist=None):
    queue = deque([root])
    solutions = set()
    while len(queue) > 0:
        cur_node = queue.popleft()
        for key in alphabet:
            replace_code = alphabet[key]
            if replace_code not in cur_node.name or \
                    (not cur_node.name.startswith(replace_code)) or \
                    blacklist and blacklist[key] and any(cur_node.letters.endswith(x) for x in blacklist[key]):
                continue
            new_code = cur_node.name.replace(replace_code, "", 1)
            if new_code == "":
                solutions.add(cur_node.letters + key)
                while queue and queue[-1].depth > cur_node.depth:  # removes elements from the next depth, found solution at this depth already
                    queue.pop()
                break
            new_node = cur_node.make_child(new_code, key)
            if not solutions: # found a solution, so only complete solutions at this depth
                queue.append(new_node)
                #cur_node.children.append(new_node)
    if not solutions:
        return ["ONMOGELIJK"]
    return sorted(solutions)


test_cases = int(input())
for i in range(test_cases):
    code = input()
    alphabet_len = int(input())
    alphabet = {}

    for _ in range(alphabet_len):
        key = input()
        val = input()
        alphabet[key] = val

    sorted_alpha = sort_alphabet(alphabet)
    test = solve(Node(code), sorted_alpha, gen_blacklist(sorted_alpha))
    print(f'{i + 1} {test[0]}')