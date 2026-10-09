# phase_check.py
import glob
import os
import pandas as pd

print("folder:", os.getcwd())
files = sorted(glob.glob("metrics_*.csv"))
print("found", len(files), "csv files")
if not files:
    print("no metrics_*.csv here. Move into the results folder or copy the files in.")

def green_stats(path):
    df = pd.read_csv(path)
    changes = df["phase"].ne(df["phase"].shift()).cumsum()
    runs = df.groupby(changes).agg(phase=("phase", "first"), length=("phase", "size"))
    greens = runs[runs["phase"].isin([0, 3])]
    return len(runs), greens["length"].mean()

for path in files:
    n, g = green_stats(path)
    print(f"{path}: phase runs={n}, mean green={g:.1f}s")
