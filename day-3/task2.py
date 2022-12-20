from os.path import join
from pathlib import Path
import numpy as np

parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"

with open(join(parent_dir, input_fname)) as file:
    lines = file.read().splitlines()

score_mapping = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    "A": 27,
    "B": 28,
    "C": 29,
    "D": 30,
    "E": 31,
    "F": 32,
    "G": 33,
    "H": 34,
    "I": 35,
    "J": 36,
    "K": 37,
    "L": 38,
    "M": 39,
    "N": 40,
    "O": 41,
    "P": 42,
    "Q": 43,
    "R": 44,
    "S": 45,
    "T": 46,
    "U": 47,
    "V": 48,
    "W": 49,
    "X": 50,
    "Y": 51,
    "Z": 52,
}

elf_groups_list = []
if len(lines) % 3:
    raise ValueError
for i in range(len(lines) // 3):
    elf_groups_list.append(lines[(i * 3) : (3 * (i + 1))])

total_score = 0
for group in elf_groups_list:
    print(group)
    elf1, elf2, elf3 = group

    common_items = np.unique([item for item in elf1 if item in elf2 and item in elf3])
    for item in common_items:
        total_score += score_mapping[item]

print(total_score)
