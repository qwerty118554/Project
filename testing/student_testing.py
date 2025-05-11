#!/usr/bin/env python
# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Testing for the maze solver.
#
# __author__ = 'Imesh Ekanyake'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------

import subprocess
import sys
import json
import os
import time
import csv
import filecmp


def run_maze_tester(config_file):
    """
    Run mazeRunner.py with the given configuration file.
    Uses 'python' on Windows and 'python3' on Unix-like systems.
    """
    if sys.platform.startswith("win"):
        cmd = ["python", "mazeRunner.py", config_file]
    else:
        cmd = ["python3", "mazeRunner.py", config_file]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Error: mazeRunner.py failed with return code", e.returncode)
        sys.exit(e.returncode)


def read_config_file(config_file):
    """
    Read and parse the JSON configuration file.
    """
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print("Error reading config file:", e)
        sys.exit(1)


def write_config_file(config, filename):
    """
    Write the provided configuration dictionary to a JSON file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print("Error writing config file:", e)
        sys.exit(1)


def create_swapped_config(original_config_file):
    """
    Create a new config with knapsackSolver swapped between 'recur' and 'dynamic'.
    """
    config = read_config_file(original_config_file)
    solver = config.get("knapsackSolver")
    if solver == "recur":
        config["knapsackSolver"] = "dynamic"
    elif solver == "dynamic":
        config["knapsackSolver"] = "recur"
    else:
        print("Error: Unknown knapsackSolver value:", solver)
        sys.exit(1)

    base, ext = os.path.splitext(original_config_file)
    new_config_file = base + "_swapped" + ext
    write_config_file(config, new_config_file)
    print(f"Created swapped config file: {new_config_file}")
    return new_config_file


def read_csv_to_list(filename):
    """
    Read a CSV file and return the content as a list of rows (each row is a list of strings).
    """
    if not os.path.exists(filename):
        print("Error: file not found:", filename)
        sys.exit(1)
    try:
        with open(filename, newline='') as csvfile:
            return list(csv.reader(csvfile))
    except Exception as e:
        print("Error reading CSV file", filename, e)
        sys.exit(1)


def sort_csv_rows(data):
    """
    Sort CSV content (list of rows) based on the first column.
    Assumes the first row is a header and doesn't sort it.
    """
    header, rows = data[0], data[1:]
    rows_sorted = sorted(rows, key=lambda row: row[0])
    return [header] + rows_sorted

def get_last_line(file_path):
    with open(file_path, 'rb') as f:
        f.seek(-2, 2)  # Move to the second last byte
        while f.read(1) != b'\n':
            f.seek(-2, 1)  # Move back two bytes
        last_line = f.readline().decode()
    return last_line.strip()


def main():
    original_config_file = "testing/testingConfig.json"
    config = read_config_file(original_config_file)
    swapped_config_file = create_swapped_config(original_config_file)

    print("Running mazeRunner with original configuration:", original_config_file)
    run_maze_tester(original_config_file)

    print("Running mazeRunner with swapped configuration:", swapped_config_file)
    run_maze_tester(swapped_config_file)

    time.sleep(1)

    dynamic_csv = "Knapsack_dynamic_items.csv"
    recur_csv = "Knapsack_recur_items.csv"

    print("Reading CSV files for consistency check...")
    dynamic_data = sort_csv_rows(read_csv_to_list(dynamic_csv))
    recur_data = sort_csv_rows(read_csv_to_list(recur_csv))

    # colours for testing
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    print("---- TESTING RECURSIVE KNAPSACK FUNCTION ----")
    print("Testing behaviour...")
    recurTest = filecmp.cmp('testing.txt', 'testing/expected_outputs/recurTest.txt')
    if recurTest:
        print(f'{GREEN}PASS{RESET}: Behaviour of recursive knapsack is as expected.')
    else:
        print(f'{RED}FAIL{RESET}: recursive knapsack behaviour is not as expected.')

    print("---- TESTING DYNAMIC KNAPSACK FUNCTION ----")
    print("Testing behaviour...")
    dynamicTest = filecmp.cmp('testing.csv', 'testing/expected_outputs/dynamicTest.csv')
    if dynamicTest:
        print(f'{GREEN}PASS{RESET}: Behaviour of dynamic knapsack is as expected.')
    else:
        print(f'{RED}FAIL{RESET}: dynamic knapsack behaviour is not as expected.')

    print("---- TESTING DYNAMIC KNAPSACK OUTPUT AGAINST RECURSIVE KNAPSACK OUTPUT ----")
    if dynamic_data == recur_data:
        print(f"{GREEN}PASS{RESET}: Consistency in dynamic and recur (Items and values are the same)")
    else:
        last_line1 = get_last_line(dynamic_csv)
        last_line2 = get_last_line(recur_csv)
        if last_line1 == last_line2:
            print(f"{GREEN}PASS{RESET}: Semi-consistency in dynamic and recur (Items are different, but values are "
                  f"the same)")
        else:
            print(f"{RED}FAIL{RESET}: Inconsistencies in solutions")

    # Cleanup
    for file in [
        "testing.csv",
        "testing.txt",
        "Knapsack_dynamic_items.csv",
        "Knapsack_recur_items.csv",
        "testing/testingConfig_swapped.json"
    ]:
        if os.path.exists(file):
            os.remove(file)


if __name__ == "__main__":
    main()