from os.path import join
from pathlib import Path

from time import time
import numpy as np

source_url = "https://adventofcode.com/2022/day/1/input"
parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"
num_iter = 500

with open(join(parent_dir, input_fname), mode="r") as file:
    # SLOWER
    # lines = [line.rstrip() for line in file]
    # lines = np.array([line.rstrip() for line in file])

    lines = file.read().splitlines()

for i in range(num_iter):
    calories_list = [0]  # Faster to use normal list here, than reassigning with numpy!!
    for line in lines:  # Faster to iterate in normal list!
        if line == "":
            calories_list.append(0)
            continue
        calories_list[-1] += int(line)

print(np.max(calories_list))
