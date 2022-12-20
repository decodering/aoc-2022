"""
Pathfinding problem of a Euclidean space

PSUEDO:

- Find the starting point and get the list of possible moves (up, down, left, right)
- For each possible, determine which ones are valid and take the first
- Check if this move already exists in current list, if not append
- Basically trying to build up the moves_dict library below

moves_dict = {
    1: [x]
    2: [[x,y],[x,a],[x,b]]
    3: [[x,y,q],[x,a,c],[x,b,h]]
    4: [[x,a,c,q],[x,b,h,e]]
}

Iteration 1
===
- x x x   x -> Not yet explored
S - x x   S -> (0, Node, hash)
- x x x   - -> Added to queue

Iteration 2
===
S - x x   . -> Popped from queue and analysed
. - x x   S -> (1, Node, hash)
- x x x

Iteration 3
===
. - x x
. S - x
- - x x

"""

from os.path import join
from pathlib import Path
import numpy as np


def get_score(char: str):
    if char == "S":
        return -1
    elif char == "E":
        return 0
    else:
        return ord(char)


parent_dir = Path(__file__).parent.resolve()
input_fname = "input_small.txt"

with open(join(parent_dir, input_fname)) as file:
    lines = file.read().splitlines()

# Initialise and create heightmap
heightmap = []
for line in lines:
    newline = [get_score(char) for char in line]
    heightmap.append(newline)
heightmap = np.array(heightmap)
starting_point = tuple(l[0] for l in np.where(heightmap == -1))
destination = tuple(l[0] for l in np.where(heightmap == 0))
heightmap[starting_point] = ord("a")
heightmap[destination] = ord("z")

# Get some stats and print out
num_rows, num_cols = heightmap.shape
print(f"Here is the heightmap")
print(heightmap)
print(starting_point, destination)

moves_dict = {0: [[starting_point]]}

steps = 0
brk_flag = False
print("")
while not brk_flag and (steps <= 20):
    print(
        f"\rProcessing step {steps}... {len(moves_dict[steps])} entries so far\t\t",
        end="",
    )
    steps += 1

    moves_dict[steps] = []

    # Build the next step for each path
    for previous_path in moves_dict[steps - 1]:
        current_point = previous_path[-1]
        y, x = current_point
        current_point_value = heightmap[current_point]
        next_points = []
        if y != 0:
            next_points.append(((y - 1), x))
        if y != (num_rows - 1):
            next_points.append(((y + 1), x))
        if x != 0:
            next_points.append((y, (x - 1)))
        if x != (num_rows - 1):
            next_points.append((y, (x + 1)))

        if steps == 17:
            $$ # Investigate possible paths -> Why not continue?
            """
            The issue is that some paths might converge, i.e. 5 steps lead to same point, and this will create exploding scenarios, rather than...
            """

        for next_point in next_points:
            next_point_value = heightmap[next_point]
            if (next_point_value <= (current_point_value + 1)) and (
                next_point not in previous_path
            ):
                moves_dict[steps].append(previous_path + [next_point])
                if next_point == destination:
                    final_path = previous_path + [next_point]
                    brk_flag = True
                    break
        if brk_flag:
            break
print("")

_ = [print(p) for p in moves_dict[16]]
_ = [print(e) for e in moves_dict[list(moves_dict.keys())[-2]][-10:]]
print(
    f"Are there non unique values?: {any([True for e in moves_dict[list(moves_dict.keys())[-2]] if len(e) != len(set(e))])}"
)
print(steps)
if brk_flag:
    print(final_path)
