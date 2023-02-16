from collections import deque, OrderedDict
import re

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


def is_path_possible(code, alphabet):
    subcodes = re.split("[^01]+", code)
    for subcode in subcodes:
        if subcode == '':
            continue
        found = False
        for replace_code in alphabet.values():
            if replace_code in subcode:
                found = True
        if not found:
            return False
    return True


def rec_walk(code: str, alphabet):
    for key in alphabet:  # TODO possible unneeded work
        if alphabet[key] in code:
            new_code = code.replace(alphabet[key], key, 1)
            if not ('0' in new_code or '1' in new_code):
                return new_code
            test = is_path_possible(new_code, alphabet)
            if test:
                found = rec_walk(new_code, alphabet)
                if found is not None:
                    return found


def walkv2(root: str, alphabet):
    found = rec_walk(root, alphabet)
    return found or "ONMOGELIJK"


def replacer(code: str, alphabet: {}):
    new_code = ""
    while code != "":
        found  = False
        for key in alphabet:
            replace_code = alphabet[key]
            if code.startswith(replace_code):
                new_code += key
                code = code.replace(replace_code, "", 1)
                found = True
                break
        if not found:
            return "ONMOGELIJK"
    return new_code


for i in range(test_cases):
    code = input()
    alphabet_len = int(input())
    alphabet = {}

    for _ in range(alphabet_len):
        key = input()
        val = input()
        alphabet[key] = val

    test = replacer(code, sort_alphabet(alphabet))
    print(f'{i + 1} {test}')
