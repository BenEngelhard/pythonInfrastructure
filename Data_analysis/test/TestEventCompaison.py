import os
import pandas as pd
import numpy as np
from Data_analysis.EventComparison import *
# Function definitions would go here (same as previously defined)

# Ask user for the path to the directory containing comparison CSV files
directory = input("Please enter the path to the directory with CSV files: ").strip()

# Ask user for the path to the latest CSV file
latest_csv_path = input("Please enter the full path to the latest CSV file: ").strip()

# Ensure the provided paths are valid
if not os.path.isdir(directory):
    print("The provided directory path does not exist.")
elif not os.path.isfile(latest_csv_path):
    print("The provided latest CSV file path does not exist.")
else:
    # If both paths are valid, perform the comparison and print Jaccard scores
    scores = compare_with_all(latest_csv_path, directory)

    # Output the Jaccard scores
    for file, score in scores.items():
        print(f"Average Jaccard similarity score for {file}: {score}")
