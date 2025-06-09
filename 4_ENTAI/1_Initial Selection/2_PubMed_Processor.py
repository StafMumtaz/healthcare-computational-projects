#Mustafa Mumtaz
#ENT Project 1
#Natural Language Processing in Otolaryngology
# Import the pandas library for working with data
import pandas as pd

# Import file and display for confirmation
input_filename = "1_PubMed_Sources.csv"
df = pd.read_csv(input_filename)
print("DataFrame shape (rows, columns):", df.shape)
print(f"Original DataFrame has {len(df.columns)} columns")

print("\nColumn names:")
for i, column in enumerate(df.columns):
    print(f"{i}: {column}")

print("\nFirst 5 rows:")
print(df.head(5))
df_modified = df.iloc[:, :40]

# Verify the column reduction worked
print(f"\nModified DataFrame has {len(df_modified.columns)} columns")

# Print the remaining column names to verify
print("\nRemaining columns in modified DataFrame:")
for i, column in enumerate(df_modified.columns):
    print(f"{i}: {column}")

#Create function to save df_modified to a csv and html and then execute it
def save_dataframe(df, base_filename="3_PubMed_Sources_Modified"):
    """Save the dataframe to both CSV and HTML files"""
    csv_filename = f"{base_filename}.csv"
    html_filename = f"{base_filename}.html"
    
    df.to_csv(csv_filename, index=False)
    df.to_html(html_filename, index=False)
    
    print(f"\nDataFrame saved to {csv_filename} and {html_filename}")
save_dataframe(df_modified)
print("\nFiles saved successfully!")

#Remove superfluous columns
cols_to_remove = [
    1, 6, 9, 14, 16, 19, 
    *range(21, 28),  # 21 to 27
    *range(30, 35), # 30 to 34
    *range(36, 39)  # 36 to 38
]

df_modified.drop(df_modified.columns[cols_to_remove], axis=1, inplace=True)


# Print info about removed columns, remaining columns to verify
print(f"Removed {len(cols_to_remove)} columns: {cols_to_remove}")
print(f"Modified DataFrame now has {len(df_modified.columns)} columns")
print("\nRemaining columns in modified DataFrame:")
for i, column in enumerate(df_modified.columns):
    print(f"{i}: {column}")
save_dataframe(df_modified)

#Create dataframe for Claude API interaction and give info about it 
df_claude_input = df_modified.iloc[:, [1, 3, 4, 7]]
print(f"Claude input DataFrame has {len(df_claude_input.columns)} columns")

# Print the column names to verify
print("\nColumns in Claude input DataFrame:")
for i, column in enumerate(df_claude_input.columns):
    print(f"{i}: {column}")

# Display the first few rows to verify content
print("\nFirst 3 rows of Claude input DataFrame:")
print(df_claude_input.head(3))

# Save to csv
df_claude_input.to_csv("4_ClaudeInput.csv", index=False)
print("\nSaved Claude input DataFrame to 4_ClaudeInput.csv")
