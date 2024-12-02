"""Harness for all AOC days."""
import importlib
import re
from os import listdir, path
from utils import abstract_day

# This file is just a disposable test harness for my own use,
# so I didn't write it with cleanliness in mind.
# TODO: Rewrite to add an argument for sample only
max_day = 0
day_num = 0
for filename in listdir("days"):
    match = re.search(r"day_(\d*)\.py", filename)
    if match is not None:
        matched_val = int(match.group(1))
        max_day = matched_val if matched_val > max_day else max_day

while day_num < 1 or day_num > max_day:
    day_input: str = input("Please enter an integer for the day of code to run, "
                           f"from 1 to {max_day}\n"
                        f"(or press Enter for day {max_day}):\n").strip()

    try:
        day_num = int(day_input) if day_input else max_day
    except ValueError:
        print(f"You entered \"{day_input}\", which couldn't be parsed into an integer. "
              "Please enter an integer.\n")
        continue

    if day_num < 1 or day_num > 25:
        print(f"No problem exists for day {day_num}. AoC 2024 only has 25 days of problems.\n")
        continue

    # Find the associated module by name and run it.
    try:
        day_module = importlib.import_module("days.day_" + str(day_num))
        day_code: abstract_day = day_module.DayCode
    except ModuleNotFoundError:
        print(f"Sorry, it looks like I haven't yet written a solution to day {day_num}. "
              "Check back later for a solution to that day.\n")
        continue
try:
    with open("sample.txt", "r", encoding="utf-8") as f:
        test_str = f.read()
    print("Part 1 Sample Output: ", day_code.part_1(test_str))
    print("Part 2 Sample Output: ", day_code.part_2(test_str))
except FileNotFoundError:
    print("No sample.txt file was found, skipping sample runs...\n"
          "If you'd like to run the smaller input samples provided by AoC separately from the main "
          "problem input, create a file called `sample.txt` and place it in the AOC2024 "
          "directory, then paste the sample input into that file.\n")

try:
    with open("input.txt", "r", encoding="utf-8") as f:
        in_str = f.read()
except FileNotFoundError:
    print("No input.txt file was found, defaulting to archived inputs...\n"
          "If you'd like to run this code on a custom input, please create a file "
          "with your desired input text called `input.txt` and place it in the "
          "AOC2024 directory.\n")
    with open(path.join("inputs",f"day_{day_num}.txt"), "r", encoding="utf-8") as f:
        in_str = f.read()
print("Part 1 Full Output:   ", day_code.part_1(in_str))
print("Part 2 Full Output:   ", day_code.part_2(in_str))
