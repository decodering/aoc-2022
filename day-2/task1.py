from os.path import join
from pathlib import Path

parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"

with open(join(parent_dir, input_fname)) as file:
    lines = file.read().splitlines()

total_score = 0
for line in lines:

    # Draw scenarios
    if line in ["A X", "B Y", "C Z"]:
        total_score += 3
    # win scenario
    elif line in ["A Y", "B Z", "C X"]:
        total_score += 6
    elif line not in ["A Z", "B X", "C Y"]:
        print(line)
        raise ValueError

    b = line[-1]
    if b == "X":
        total_score += 1
    elif b == "Y":
        total_score += 2
    else:
        total_score += 3

print(total_score)
