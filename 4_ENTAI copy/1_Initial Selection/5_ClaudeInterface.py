#Mustafa Mumtaz
#ENT Project 1
#Natural Language Processing in Otolaryngology

import pandas as pd
import time
import os.path
from anthropic import Anthropic

#---------- CLAUDE API INTEGRATION ----------#
print("\n\nStarting Claude API integration...")

#Set up Claude API Client and set criteria for paper inclusion
client = Anthropic(api_key="redacted")

def should_include_paper(title, abstract):
    # Construct the prompt for Claude
    prompt = f"""
    I'm conducting a systematic review specifically focused on natural language processing and language models in the field of otolaryngology (ENT).

    Please review the following paper and determine if it meets BOTH of these criteria:
    1. It must focus specifically on natural language processing, NLP, or language models (not just general AI, machine learning, or other AI applications). Of note, as long as it does primarily utilize a language based AI model, I am fine with including a very large range of applications. 
    2. It must be directly relevant to otolaryngology/ENT (ear, nose, throat) practice or research. If the article primarily seems to be about other fields, it should not be included. 
    
    Title: {title}
    Abstract: {abstract}

    Based solely on the title and abstract, should this paper be included in my systematic review?
    Respond with ONLY "1" if it meets BOTH criteria, or "0" if it fails to meet either criterion.
    """
    
    # Call the Claude API
    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=5,
            temperature=0,
            system="You are helping a medical student conduct a systematic review of natural language processing in otolaryngology. Respond only with '1' for papers that meet ALL inclusion criteria or '0' for papers that fail to meet any criterion.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response
        answer = response.content[0].text.strip()
        
        # Convert to binary (default to 0 if anything unexpected)
        return 1 if answer == "1" else 0
    except Exception as e:
        print(f"Error with API call: {e}")
        return 0

# Read the Claude input CSV again to ensure we have the latest data
df_claude_input = pd.read_csv("4_ClaudeInput.csv")

# Add a new column for inclusion decision if it doesn't exist
if 'include' not in df_claude_input.columns:
    df_claude_input['include'] = 0

checkpoint_file = "5_ClaudeOutput_checkpoint.csv"
start_index = 0

if os.path.exists(checkpoint_file):
    print(f"Found checkpoint file. Resuming from previous run...")
    df_checkpoint = pd.read_csv(checkpoint_file)
    # Find the last processed row
    processed_rows = df_checkpoint['include'].notna().sum()
    if processed_rows > 0:
        # Copy already processed decisions
        df_claude_input.iloc[:processed_rows, -1] = df_checkpoint.iloc[:processed_rows, -1]
        start_index = processed_rows
        print(f"Resuming from paper {start_index + 1}")

# Get column names for safer referencing
columns = df_claude_input.columns.tolist()
title_col = columns[1]  # Title is the 2nd column
abstract_col = columns[3]  # Abstract is the 4th column

# Process each row
print("Processing papers with Claude API...")
for i in range(start_index, len(df_claude_input)):
    row = df_claude_input.iloc[i]
    title = row[title_col]
    abstract = row[abstract_col]
    
    # Handle missing abstracts
    if pd.isna(abstract):
        abstract = "No abstract available."
    
    # Print progress
    print(f"Processing paper {i+1}/{len(df_claude_input)}: {title[:50]}...")
    
    # Get Claude's decision
    include = should_include_paper(title, abstract)
    
    # Update the DataFrame
    df_claude_input.at[i, 'include'] = include
    
    # Save checkpoint after each paper
    df_claude_input.to_csv(checkpoint_file, index=False)
    
    # Add a small delay to avoid hitting API rate limits
    time.sleep(0.5)

# Save the final updated DataFrame
df_claude_input.to_csv("6_ClaudeOutput.csv", index=False)
print("\nProcessing complete! Results saved to 6_ClaudeOutput.csv")

# Print a summary of results
included_count = df_claude_input['include'].sum()
print(f"\nSummary:")
print(f"Total papers: {len(df_claude_input)}")
print(f"Papers to include: {included_count}")
print(f"Papers to exclude: {len(df_claude_input) - included_count}")
