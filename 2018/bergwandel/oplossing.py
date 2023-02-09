# HELPER CLASS

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

# STAGE 1: TURN INTO DATA STRUCTURES


test_cases = int(input())
height_cards = []
for _ in range(test_cases):
    cols, rows = map(int, input().split())
    height_card = {"card": [], "size": Point(cols, rows), "path": [], "walk_idx": 0}
    for _ in range(rows):
        col = [int(num) for num in input().split()]
        height_card["card"].append(col)
    height_cards.append(height_card)
print(height_cards, len(height_cards))

# STAGE 2: MODIFY DATA

# find the lowest number positions
for height_card in height_cards:
    position = Point()
    lowest_val = float('inf')  # start at highest number
    for i, col in enumerate(height_card["card"]):
        for j, val in enumerate(col):
            if val < lowest_val:
                position = Point(j, i)
                lowest_val = val
    height_card["lowest_val_position"] = position
    height_card["path"].append(position)


# generate path
def walk_path(height_card):
    next_pos = None
    curr_pos = height_card["path"][height_card["walk_idx"]]
    curr_val = curr_pos.get(height_card["card"])
    curr_lowest = float('inf')

    for direction in directions:
        new_poss = curr_pos.add_but_bound(direction, height_card["size"])
        new_val = new_poss.get(height_card["card"])
        if curr_val < new_val < curr_lowest:  # minst steile stijgende
            curr_lowest = new_val
            next_pos = new_poss

    if next_pos is None:  # hit end of path
        return False
    else:
        height_card["walk_idx"] += 1
        height_card["path"].append(next_pos)
        return True


for height_card in height_cards:
    while walk_path(height_card):
        pass

# STAGE 3: OUTPUT
ASCII_OFFSET = 65

for idx, height_card in enumerate(height_cards):
    size = height_card["size"]
    base_output = [['.'] * size.X for _ in range(size.Y)]

    for i, pos in enumerate(height_card["path"]):  # fill output
        pos.set(base_output, chr(ASCII_OFFSET + i))

    for row in base_output:  # print output
        print(f'{idx + 1} {"".join(row)}')
