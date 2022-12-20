from os.path import join
from pathlib import Path
import numpy as np

parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"

with open(join(parent_dir, input_fname)) as file:
    lines = file.read().splitlines()

num_overlapped = 0
for line in lines:
    a, b = [e.strip() for e in line.split(",")]
    a_min, a_max = [int(e) for e in a.split("-")]
    b_min, b_max = [int(e) for e in b.split("-")]
    if not ((b_min > a_max) or (b_max < a_min)):
        num_overlapped += 1

print(num_overlapped)
