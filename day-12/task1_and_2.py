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
S - x x   S -> (0, Node, (prev,after))
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

For a more complete visualisation of how this will look like, refer to --> input_analyses.txt
"""

from os.path import join
from pathlib import Path
from collections import deque
import numpy as np
from textwrap import dedent
from typing import Tuple


def read_text_file(input_file_path: str) -> list:
    with open(input_file_path) as file:
        lines = file.read().splitlines()
    return lines


def get_score(char: str):
    if char == "S":
        return -1
    elif char == "E":
        return 0
    else:
        return ord(char)


def generate_heatmap_from_file(
    input_file_path: str,
) -> Tuple[np.array, Tuple[int], Tuple[int]]:
    lines = read_text_file(input_file_path)

    heightmap = []
    for line in lines:
        newline = [get_score(char) for char in line]
        heightmap.append(newline)
    heightmap = np.array(heightmap)
    starting_point = tuple(l[0] for l in np.where(heightmap == -1))
    destination = tuple(l[0] for l in np.where(heightmap == 0))
    heightmap[starting_point] = ord("a")
    heightmap[destination] = ord("z")
    return heightmap, starting_point, destination


def calculate_min_steps(
    heightmap: np.array,
    starting_point: Tuple[int, int],
    final_point: Tuple[int, int],
    silent: bool = False,
) -> Tuple:
    def _print(string: str, silent: bool, end: str = None) -> None:
        if not silent and end is None:
            print(string)
        elif not silent:
            print(string, end=end)

    visited = [starting_point]
    queue = deque([(0, starting_point)])
    paths_list = deque(
        [(0, starting_point, None, ord("a"))]
    )  # [(step_num, current_point, prev_point, current_point_value),(...),...]

    cnt = 0
    brk_flag = False
    shortest_path_numsteps = None
    _print("", silent=silent)
    # Build the next step for each path
    while queue and not brk_flag:
        cnt += 1
        steps, current_point = queue.popleft()
        y, x = current_point
        current_point_value = heightmap[current_point]
        next_points = []
        if y != 0:
            next_points.append(((y - 1), x))
        if y != (num_rows - 1):
            next_points.append(((y + 1), x))
        if x != 0:
            next_points.append((y, (x - 1)))
        if x != (num_cols - 1):
            next_points.append((y, (x + 1)))

        for next_point in next_points:
            next_point_value = heightmap[next_point]
            if (next_point not in visited) and (
                next_point_value <= (current_point_value + 1)
            ):
                visited.append(next_point)
                queue.append((steps + 1, next_point))
                paths_list.append(
                    (steps + 1, next_point, current_point, next_point_value)
                )

                if next_point == final_point:
                    shortest_path_numsteps = steps + 1
                    brk_flag = True
                    break

        _print(
            f"\rProcessed step {steps}... {len(visited)},{len(queue)} entries so far\t\t",
            end="",
            silent=silent,
        )
    _print("", silent=silent)
    return shortest_path_numsteps, paths_list, visited, cnt


def calculate_shortest_path(
    paths_list: list,
    steps_taken: int,
    starting_point: Tuple[int, int],
    final_point: Tuple[int, int],
) -> list:
    ind = steps_taken - 1
    current_point = final_point
    shortest_path = deque([final_point])
    _, _, prev_point, _ = paths_list[-1]
    while ind != 0:
        num_possible_prev_points_in_current_step = 0
        for steps, point_2, point_1, _ in list(paths_list)[:-1]:
            if (steps == ind) and (prev_point == point_2):
                current_point = point_2
                prev_point = point_1

                shortest_path.appendleft(current_point)
                num_possible_prev_points_in_current_step += 1

        # This will conveniently be 1 as for each step, there should only be 1 unique movement (non-circular!)
        assert (
            num_possible_prev_points_in_current_step == 1
        ), f"{num_possible_prev_points_in_current_step, current_point, ind}\n"
        ind -= 1
    shortest_path.appendleft(starting_point)
    return shortest_path


# Initialise and create heightmap
parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"
heightmap, starting_point, destination = generate_heatmap_from_file(
    join(parent_dir, input_fname)
)

# Get some stats and print out
num_rows, num_cols = heightmap.shape
print(
    dedent(
        f"""
Here is the heightmap:

{heightmap}

Starting point -> {starting_point}
Destination point -> {destination}
"""
    )
)

# Task 1: Calculate the minimum steps, given a specified start point, and then for multiple start points
shortest_path_numsteps, paths_list, visited, cnt = calculate_min_steps(
    heightmap=heightmap, starting_point=starting_point, final_point=destination
)

# Build and trace back the path backwards
shortest_path = calculate_shortest_path(
    paths_list=paths_list,
    steps_taken=shortest_path_numsteps,
    starting_point=starting_point,
    final_point=destination,
)

# Task 2: Get other possible starting points
other_possible_starting_coords = [
    (y, x) for y, x in zip(*np.where(heightmap == ord("a")))
]
other_possible_starting_coords.remove(starting_point)
shortest_path_numsteps_overall = None
cnt_overall = cnt
num_coords = len(other_possible_starting_coords)
for ind, starting_coord in enumerate(other_possible_starting_coords, 1):
    print(
        f"\rProcessing other path for other starting points ({ind} / {num_coords})...",
        end="" if (ind != num_coords) else "\n",
    )
    numsteps, _, _, cnt_local = calculate_min_steps(
        heightmap=heightmap,
        starting_point=starting_coord,
        final_point=destination,
        silent=True,
    )
    cnt_overall += cnt_local
    # If numsteps is None -> There is no possible pathway, skip this
    if (numsteps is not None) and (
        (shortest_path_numsteps_overall is None)
        or (numsteps < shortest_path_numsteps_overall)
    ):
        shortest_path_numsteps_overall = numsteps

# Print out some information about the calculation if not too big
if shortest_path_numsteps < 50:
    for i in range(shortest_path_numsteps + 1):
        current_step_paths = []
        for steps, point_2, point_1, point_2_value in paths_list:
            if i == steps:
                current_step_paths.append([point_2, point_1, point_2_value])
        print(f"{i}: {current_step_paths}")
    print(visited)

# Print out final summary
print(
    dedent(
        f"""\n====\n
Shortest path: {shortest_path}

start and destination: {starting_point,destination}
last entry in paths_list: {paths_list[-1]}

Task 1: Min num steps w given starting point \t\t ==> {shortest_path_numsteps} ({cnt} iterations to find solution) <==
Task 2: Min num steps w variable starting point \t ==> {shortest_path_numsteps_overall} ({cnt_overall} iterations to find solution) <==
"""
    )
)
