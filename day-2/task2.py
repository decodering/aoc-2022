from os.path import join
from pathlib import Path

parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"

with open(join(parent_dir, input_fname)) as file:
    lines = file.read().splitlines()

"""
If draw:
 + 3
 and base on oponent

If lose:
    If paper + x
    if ..
    if ..

If win:
    +6
    if paper 
"""

total_score = 0
for line in lines:
    a, b = line.split(" ")

    # Draw scenario
    if b == "Y":
        total_score += 3

        if a == "A":
            total_score += 1
        elif a == "B":
            total_score += 2
        else:
            total_score += 3

    # Win scenario
    elif b == "Z":
        total_score += 6

        if a == "A":
            total_score += 2
        elif a == "B":
            total_score += 3
        else:
            total_score += 1

    # Lose scenario/s
    elif line == "A X":
        total_score += 3
    elif line == "B X":
        total_score += 1
    elif line == "C X":
        total_score += 2
    else:
        raise ValueError

print(total_score)
