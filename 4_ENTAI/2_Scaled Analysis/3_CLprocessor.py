#Mustafa Mumtaz
#Literature Processor

import pandas as pd
import sys

print("Processing Clinical Literature CSV file...")
print("-" * 50)

# Read the CSV file
input_file = "2_CL.csv"
output_file = "4_APIinput.csv"

try:
    # Read CSV with progress indicator
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    total_rows = len(df)
    total_cols = len(df.columns)
    
    print(f"✓ Loaded {total_rows:,} rows and {total_cols} columns")
    
    # Display original columns for reference
    print("\nOriginal columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}: {col}")
    
    # Columns to KEEP (using 1-based indexing as specified)
    # Keep columns 3, 5, 6, 11
    columns_to_keep = [2, 4, 5, 10]  # 0-based indices
    
    # Check if all columns exist
    if max(columns_to_keep) >= len(df.columns):
        print(f"\nError: CSV only has {len(df.columns)} columns, but trying to access column {max(columns_to_keep)+1}")
        sys.exit(1)
    
    # Select only the columns we want to keep
    print(f"\nKeeping columns {[i+1 for i in columns_to_keep]}: ", end="")
    selected_columns = [df.columns[i] for i in columns_to_keep]
    print(f"{selected_columns}")
    
    df_filtered = df.iloc[:, columns_to_keep]
    
    # Show sample of filtered data
    print("\nSample of filtered data (first 3 rows):")
    print(df_filtered.head(3).to_string(max_colwidth=50))
    
    # Save to new CSV with progress
    print(f"\nSaving to {output_file}...")
    
    # For large files, we can save in chunks to show progress
    chunk_size = 1000
    chunks_written = 0
    
    # Write header first
    df_filtered.iloc[:0].to_csv(output_file, index=False)
    
    # Write in chunks with progress updates
    for start_idx in range(0, total_rows, chunk_size):
        end_idx = min(start_idx + chunk_size, total_rows)
        df_filtered.iloc[start_idx:end_idx].to_csv(
            output_file, 
            mode='a', 
            header=False, 
            index=False
        )
        chunks_written += (end_idx - start_idx)
        
        # Progress bar
        progress = chunks_written / total_rows
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\rProgress: |{bar}| {progress*100:.1f}% ({chunks_written:,}/{total_rows:,} rows)', 
              end='', flush=True)
    
    print()  # New line after progress bar
    
    # Summary statistics
    print(f"\n✓ Successfully processed {total_rows:,} rows")
    print(f"✓ Reduced from {total_cols} to {len(df_filtered.columns)} columns")
    print(f"✓ Output saved to {output_file}")
    
    # File size comparison
    import os
    if os.path.exists(input_file) and os.path.exists(output_file):
        input_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
        output_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        reduction = (1 - output_size/input_size) * 100
        print(f"\nFile size: {input_size:.1f}MB → {output_size:.1f}MB ({reduction:.1f}% reduction)")
    
except FileNotFoundError:
    print(f"\nError: Could not find {input_file}")
    print("Please ensure the file exists in the current directory")
    sys.exit(1)
    
except Exception as e:
    print(f"\nError processing file: {str(e)}")
    sys.exit(1)

print("\nProcessing complete!")
print("Next step: Use 4_APIinput.csv for GPT API processing")
