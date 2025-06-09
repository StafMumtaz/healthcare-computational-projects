#Mustafa Mumtaz
#Systematic Review Multi-Criteria Evaluation
#Script 5: Test OpenAI API on first 5 papers with retry logic

import pandas as pd
import requests
import json
import time
import os
from datetime import datetime

# Configuration
API_KEY = os.environ.get('redacted', 'redacted')
API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4.1-mini"
TEST_ROWS = 5
MAX_RETRIES = 10
BASE_WAIT_TIME = 1  # Start with 1 second wait

# Check for API key
if API_KEY == 'YOUR_API_KEY_HERE':
    print("Please set your OpenAI API key!")
    print("Either:")
    print("1. Set environment variable: export OPENAI_API_KEY='your-key-here'")
    print("2. Or edit the API_KEY variable in this script")
    exit(1)

def create_evaluation_prompts(title, abstract):
    """Create all evaluation prompts for a single paper"""
    
    prompts = {
        'nlp_ent_relevant': f"""I'm conducting a systematic review specifically focused on natural language processing and language models in the field of otolaryngology (ENT). Please review the following paper and determine if it meets BOTH of these criteria:

1. It must focus specifically on natural language processing, NLP, or language models (not just general AI, machine learning, or other AI applications). Of note, as long as it does primarily utilize a language based AI model, I am fine with including a very large range of applications.
2. It must be directly relevant to otolaryngology/ENT (ear, nose, throat) practice or research. If the article primarily seems to be about other fields, it should not be included.

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, should this paper be included in my systematic review? Respond with ONLY "1" if it meets BOTH criteria, or "0" if it fails to meet either criterion.""",

        'real_world_app': f"""I need to assess whether this study demonstrates real-world applicability of NLP/language models or merely tests their general performance. Please evaluate based on these criteria:

ASSIGN "0" if the study primarily:
- Tests knowledge or accuracy of AI models against question banks
- Compares model outputs to expert panels without practical implementation
- Evaluates readability or other output quality metrics in isolation
- Benchmarks model performance without demonstrating practical use cases
- Focuses on theoretical capabilities without real-world application

ASSIGN "1" if the study demonstrates:
- Integration into actual clinical workflows or EMR systems
- Use for generating research insights or hypotheses
- Application in administrative or operational healthcare tasks
- Implementation in real clinical decision-making scenarios
- Practical deployment beyond mere performance testing

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, respond with ONLY "1" for real-world applicability or "0" for performance testing only.""",

        'substantive_study': f"""I need to determine if this publication represents a substantive research study. Please evaluate:

ASSIGN "0" if the publication is:
- A case report about a single patient
- An opinion piece, editorial, or commentary
- A journal entry or personal reflection
- A letter to the editor
- A single-person study or individual experience report

ASSIGN "1" if the publication is:
- A research study with multiple subjects or data points
- A systematic evaluation or implementation study
- A population-based analysis
- A clinical trial or cohort study
- Any multi-patient or system-wide investigation

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, respond with ONLY "1" for substantive research study or "0" for excluded publication type.""",

        'research_tool': f"""I need to determine if this study uses NLP/language models as tools to facilitate academic research. Please evaluate:

ASSIGN "1" if the NLP/language model is used for:
- Literature review automation or systematic review assistance
- Research hypothesis generation
- Academic writing assistance or manuscript preparation
- Citation analysis or bibliometric studies
- Research data extraction or synthesis
- Grant writing or research proposal development

ASSIGN "0" if the study does not demonstrate use as an academic research tool.

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, respond with ONLY "1" if used as academic research tool or "0" if not.""",

        'data_insights': f"""I need to determine if this study uses NLP/language models to generate new insights from large-scale data analysis. Please evaluate:

ASSIGN "1" if the study demonstrates:
- Pattern recognition across large clinical datasets
- Mining insights from extensive medical records
- Analyzing trends in population health data
- Discovering associations in big data that would be impractical manually
- Extracting knowledge from large corpora of medical literature
- Identifying previously unknown relationships in healthcare data

ASSIGN "0" if the study does not involve generating insights from large-scale data analysis.

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, respond with ONLY "1" if generating insights from large data or "0" if not.""",

        'clinical_decision': f"""I need to determine if this study implements NLP/language models for clinical decision-making support. Please evaluate:

ASSIGN "1" if the NLP/language model is used for:
- Diagnostic assistance or differential diagnosis generation
- Treatment recommendation systems
- Risk stratification or prognostication
- Clinical guideline implementation
- Real-time clinical alerts or warnings
- Patient triage or prioritization
- Surgical planning assistance

ASSIGN "0" if the study does not involve clinical decision support applications.

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, respond with ONLY "1" if used for clinical decision support or "0" if not.""",

        'emr_integration': f"""I need to determine if this study involves integration of NLP/language models with Electronic Medical Records (EMR) systems. Please evaluate:

ASSIGN "1" if the study demonstrates:
- Direct integration with EMR/EHR systems
- Automated clinical note generation or documentation
- EMR data extraction and processing
- Clinical workflow integration within EMR interfaces
- Automated coding or billing integration
- EMR-based alert systems using NLP
- Voice-to-text documentation in EMR systems

ASSIGN "0" if the study does not involve EMR integration.

Title: {title}
Abstract: {abstract}

Based solely on the title and abstract, respond with ONLY "1" if EMR integration is demonstrated or "0" if not."""
    }
    
    return prompts

def call_openai_api(prompt, criterion_name=""):
    """Make a single API call to OpenAI with retry logic"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a systematic review assistant. Respond only with '1' or '0' as instructed."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 10,
        "stream": False
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            
            # If successful, return result
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Extract just the digit if there's extra text
                if '1' in content:
                    return 1
                else:
                    return 0
            
            # If rate limited, retry with exponential backoff
            elif response.status_code == 429:
                wait_time = BASE_WAIT_TIME * (2 ** attempt)  # Exponential backoff
                
                # Try to parse retry-after header
                retry_after = response.headers.get('retry-after')
                if retry_after:
                    wait_time = max(wait_time, int(retry_after))
                
                if attempt < MAX_RETRIES - 1:
                    print(f"\n    Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{MAX_RETRIES}...", 
                          end='', flush=True)
                    time.sleep(wait_time)
                else:
                    print(f"\n    Rate limit persists after {MAX_RETRIES} attempts.")
                    return -1
            
            # For other errors, log and retry
            else:
                print(f"\n    API Error {response.status_code}: {response.text[:100]}")
                if attempt < MAX_RETRIES - 1:
                    wait_time = BASE_WAIT_TIME * (2 ** attempt)
                    print(f"    Waiting {wait_time}s before retry {attempt + 1}/{MAX_RETRIES}...", 
                          end='', flush=True)
                    time.sleep(wait_time)
                else:
                    return -1
                    
        except requests.exceptions.RequestException as e:
            print(f"\n    Network error: {e}")
            if attempt < MAX_RETRIES - 1:
                wait_time = BASE_WAIT_TIME * (2 ** attempt)
                print(f"    Waiting {wait_time}s before retry {attempt + 1}/{MAX_RETRIES}...", 
                      end='', flush=True)
                time.sleep(wait_time)
            else:
                return -1
        except Exception as e:
            print(f"\n    Unexpected error: {e}")
            return -1
    
    return -1  # Should never reach here

def main():
    print("=" * 60)
    print("Multi-Criteria Paper Evaluation using OpenAI GPT-4.1-mini")
    print("With automatic retry logic for rate limits")
    print("=" * 60)
    
    # Read input file
    try:
        df = pd.read_csv("4_APIinput.csv")
        print(f"✓ Loaded {len(df)} papers from 4_APIinput.csv")
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
    
    # Get column indices (0-based)
    # Column 2 is title (index 1), Column 4 is abstract (index 3)
    title_col = df.columns[1]
    abstract_col = df.columns[3]
    
    # Take first 5 rows for testing
    test_df = df.head(TEST_ROWS).copy()
    print(f"✓ Testing first {TEST_ROWS} papers")
    
    # Initialize result columns
    criteria = ['nlp_ent_relevant', 'real_world_app', 'substantive_study', 
                'research_tool', 'data_insights', 'clinical_decision', 'emr_integration']
    
    for criterion in criteria:
        test_df[criterion] = -1  # Initialize with -1 (not processed)
    
    # Track API usage and failures
    total_tokens = 0
    api_calls = 0
    successful_calls = 0
    failed_criteria = []
    start_time = datetime.now()
    
    # Process each paper
    for idx, row in test_df.iterrows():
        print(f"\nProcessing paper {idx + 1}/{TEST_ROWS}")
        title = row[title_col]
        abstract = row[abstract_col] if pd.notna(row[abstract_col]) else "No abstract available"
        
        print(f"Title: {title[:60]}...")
        
        # Get all prompts for this paper
        prompts = create_evaluation_prompts(title, abstract)
        
        # Evaluate each criterion
        for criterion in criteria:
            print(f"  Evaluating {criterion}...", end='', flush=True)
            
            result = call_openai_api(prompts[criterion], criterion)
            test_df.at[idx, criterion] = result
            
            if result == -1:
                print(" [FAILED]")
                failed_criteria.append((idx + 1, criterion))
            else:
                print(f" [{result}]")
                successful_calls += 1
            
            api_calls += 1
            
            # Small additional delay between successful calls
            if result != -1:
                time.sleep(0.5)
    
    # Calculate summary statistics
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    for criterion in criteria:
        valid_results = test_df[test_df[criterion] != -1][criterion]
        if len(valid_results) > 0:
            included = (valid_results == 1).sum()
            total = len(valid_results)
            pct = (included / total * 100) if total > 0 else 0
            print(f"{criterion:20} {included}/{total} papers ({pct:.1f}%)")
        else:
            print(f"{criterion:20} No successful evaluations")
    
    # Report failures
    if failed_criteria:
        print(f"\n⚠️  Failed evaluations: {len(failed_criteria)}/{api_calls}")
        print("Failed on:")
        for paper_num, criterion in failed_criteria[:10]:  # Show first 10
            print(f"  - Paper {paper_num}, {criterion}")
        if len(failed_criteria) > 10:
            print(f"  ... and {len(failed_criteria) - 10} more")
    
    # Estimate costs (rough approximation)
    # Assuming ~500 tokens per prompt + ~5 tokens response
    est_input_tokens = successful_calls * 500
    est_output_tokens = successful_calls * 5
    est_cost = (est_input_tokens * 0.0004 + est_output_tokens * 0.0016) / 1000
    
    print(f"\nAPI Calls attempted: {api_calls}")
    print(f"Successful calls: {successful_calls}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Estimated cost: ${est_cost:.4f}")
    
    # Save results regardless of failures
    output_file = "6_TestResults.csv"
    test_df.to_csv(output_file, index=False)
    print(f"\n✓ Results saved to {output_file}")
    print("  (Papers with -1 values had persistent API failures)")
    
    # Show which papers met all inclusion criteria
    print("\n" + "=" * 60)
    print("PAPERS MEETING CORE INCLUSION CRITERIA (NLP + ENT)")
    print("=" * 60)
    
    # Only consider papers where we got valid results for both criteria
    valid_mask = (test_df['nlp_ent_relevant'] != -1) & (test_df['substantive_study'] != -1)
    included_mask = valid_mask & (test_df['nlp_ent_relevant'] == 1) & (test_df['substantive_study'] == 1)
    included_papers = test_df[included_mask]
    
    if len(included_papers) > 0:
        for idx, row in included_papers.iterrows():
            print(f"\n{idx + 1}. {row[title_col][:80]}...")
            if row['real_world_app'] != -1 and row['real_world_app'] == 1:
                apps = []
                if row['research_tool'] == 1: apps.append("Research Tool")
                if row['data_insights'] == 1: apps.append("Data Insights")
                if row['clinical_decision'] == 1: apps.append("Clinical Decision")
                if row['emr_integration'] == 1: apps.append("EMR Integration")
                if apps:
                    print(f"   Applications: {', '.join(apps)}")
    else:
        if valid_mask.sum() == 0:
            print("Could not evaluate papers due to API failures.")
        else:
            print("No papers met the inclusion criteria in this test sample.")
    
    # Final message about rate limits
    if api_calls > successful_calls:
        print(f"\n⚠️  Note: {api_calls - successful_calls} evaluations failed despite retries.")
        print("Consider:")
        print("- Waiting longer before running again")
        print("- Reducing concurrent usage of this API key")
        print("- Upgrading your OpenAI API tier for higher rate limits")

if __name__ == "__main__":
    main()
