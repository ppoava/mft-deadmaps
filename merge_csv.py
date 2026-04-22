import os
import pandas as pd

base_dir = "all_runs"

# Create master dataframe with chip index. Will be used as left-most column in the master file
df_master = pd.DataFrame({"chip": range(1, 936)})

# Loop over runs (folders are named with runname)
for run in sorted(os.listdir(base_dir)):
    run_path = os.path.join(base_dir, run)

    if not os.path.isdir(run_path):
        continue

    csv_file = os.path.join(run_path, f"{run}_dead_all.csv")

    if not os.path.exists(csv_file):
        print(f"Skipping {run}: file not found")
        continue

    # Read individual CSV file (2 columns: chip, percentage)
    df = pd.read_csv(csv_file, header=None, names=["chip", run])

    # Merge columns into master (left join keeps all chips 1–935)
    df_master = df_master.merge(df, on="chip", how="left")

# Save master as CSV
df_master.to_csv("merged_deadmaps.csv", index=False)

print("Done. Output: merged_deadmaps.csv")
