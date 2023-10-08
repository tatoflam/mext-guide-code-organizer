import pandas as pd
import glob

# Path pattern to match your CSV files
path_pattern = 'data/20231008/*_out_externaloutcomes_utf8.csv'

# Use glob to list all files matching the pattern
all_files = glob.glob(path_pattern)

# Read and concatenate all CSV files into a single dataframe
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# Save the concatenated dataframe to a new CSV file
df.to_csv('MEXT_JAPAN_outcomes.csv', index=False)
