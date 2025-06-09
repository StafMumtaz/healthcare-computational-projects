#Mustafa Mumtaz
#ENT Project 1
#Natural Language Processing in Otolaryngology
#Script 3: Create Final Inclusion List

import pandas as pd
print("Starting to process Claude's output to create final inclusion list...")

input_filename = "6_ClaudeOutput.csv"
df = pd.read_csv(input_filename)

print(f"Read {input_filename} with {len(df)} rows")
print(f"Original columns: {df.columns.tolist()}")

# Count papers before filtering
include_count = df.iloc[:, -1].sum()
exclude_count = len(df) - include_count
print(f"Papers marked for inclusion: {include_count}")
print(f"Papers marked for exclusion: {exclude_count}")

# Filter to keep only rows where last column is 1
df_included = df[df.iloc[:, -1] == 1].copy()
print(f"Keeping {len(df_included)} papers for inclusion")

# Remove last column (inclusion indicator)
df_included = df_included.iloc[:, :-1]
print(f"Removed inclusion column. Final columns: {df_included.columns.tolist()}")

# Save the filtered DataFrame to a new CSV
output_filename = "7_StudyInclusion.csv"
df_included.to_csv(output_filename, index=False)

print(f"\nProcessing complete!")
print(f"Final inclusion list saved to {output_filename}")
print(f"Total papers included: {len(df_included)}")
