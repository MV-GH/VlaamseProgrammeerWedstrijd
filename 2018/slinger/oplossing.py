from collections import defaultdict
import math


def get_predict_interval(slinger):
    amounts_slinger = defaultdict(lambda: 0)
    for period in slinger.split("*"):
        amounts_slinger[len(period)] += 1
    return max(amounts_slinger, key=lambda key: amounts_slinger[key])  # return highest amount of interval


def fix_slinger(slinger, correct_amount):
    found_seq_pos = math.ceil(len(slinger) / 2)  # if it doesn't contain stars then the middle is the only star possible
    star_dist = correct_amount + 1

    for i, c in enumerate(slinger):  # find the start position of a sequence
        if c == '*' and i + star_dist < len(slinger) and slinger[i + star_dist] == '*':
            found_seq_pos = i

    start_pos = found_seq_pos % star_dist  # find first position for star
    base_slinger = ['.'] * len(slinger)
    for i in range(start_pos, len(slinger), star_dist):
        base_slinger[i] = '*'

    return "".join(base_slinger)


test_cases = int(input())
slingers = []

for _ in range(test_cases):
    input()  # skip amount chars not needed
    slingers.append(input())

for idx, slinger in enumerate(slingers):
    interval = get_predict_interval(slinger)
    new_slinger = fix_slinger(list(slinger), interval)
    print(f"{idx + 1} {new_slinger}")
