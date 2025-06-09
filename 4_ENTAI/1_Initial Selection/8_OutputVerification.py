#Mustafa Mumtaz
#ENT Project 1
#Natural Language Processing in Otolaryngology
#Script 4: Create validation sample for manual review

import pandas as pd
import numpy as np
from scipy import stats

# Set random seed for reproducibility
np.random.seed(42)

print("Creating validation sample for manual review of AI decisions...")

# Read the original full dataset and Claude's output
df_original = pd.read_csv("1_PubMed_Sources.csv")
df_claude = pd.read_csv("6_ClaudeOutput.csv")

# Verify the datasets align
assert len(df_original) == len(df_claude), "Datasets have different lengths!"

# Add the original index to track papers
df_claude['original_index'] = df_claude.index

# Separate included and excluded papers
included_papers = df_claude[df_claude['include'] == 1]
excluded_papers = df_claude[df_claude['include'] == 0]

print(f"Total papers: {len(df_claude)}")
print(f"Included by AI: {len(included_papers)} ({len(included_papers)/len(df_claude)*100:.1f}%)")
print(f"Excluded by AI: {len(excluded_papers)} ({len(excluded_papers)/len(df_claude)*100:.1f}%)")

# Calculate sample sizes for stratified sampling
MIN_SAMPLE = 10
DESIRED_SAMPLE = 20  # Aim for 20 to get better statistical power

# Stratified sampling proportions
inclusion_rate = len(included_papers) / len(df_claude)
n_included_sample = max(2, int(DESIRED_SAMPLE * inclusion_rate))
n_excluded_sample = max(2, DESIRED_SAMPLE - n_included_sample)

# Ensure we don't exceed available papers
n_included_sample = min(n_included_sample, len(included_papers))
n_excluded_sample = min(n_excluded_sample, len(excluded_papers))

# Adjust if total is less than minimum
total_sample = n_included_sample + n_excluded_sample
if total_sample < MIN_SAMPLE:
    # Proportionally increase to reach minimum
    if len(included_papers) > n_included_sample:
        n_included_sample = min(len(included_papers), 
                               n_included_sample + (MIN_SAMPLE - total_sample))
    if len(excluded_papers) > n_excluded_sample:
        n_excluded_sample = min(len(excluded_papers), 
                               MIN_SAMPLE - n_included_sample)

print(f"\nValidation sample:")
print(f"  Papers AI included: {n_included_sample}")
print(f"  Papers AI excluded: {n_excluded_sample}")
print(f"  Total sample size: {n_included_sample + n_excluded_sample}")

# Randomly sample from each group
included_sample = included_papers.sample(n=n_included_sample)
excluded_sample = excluded_papers.sample(n=n_excluded_sample)

# Combine samples
validation_sample = pd.concat([included_sample, excluded_sample])

# Shuffle the combined sample
validation_sample = validation_sample.sample(frac=1).reset_index(drop=True)

# Get column indices safely
columns = df_claude.columns.tolist()
journal_col = columns[0]   # Journal
title_col = columns[1]     # Title
author_col = columns[2]    # Author
abstract_col = columns[3]  # Abstract

# Create blinded DataFrame
df_blinded = pd.DataFrame({
    'review_id': range(1, len(validation_sample) + 1),
    'journal': validation_sample[journal_col].values,
    'title': validation_sample[title_col].values,
    'abstract': validation_sample[abstract_col].fillna('No abstract available').values,
    'your_decision': ''  # Empty column for manual input
})

# Create revealed DataFrame
df_revealed = pd.DataFrame({
    'review_id': range(1, len(validation_sample) + 1),
    'original_row': validation_sample['original_index'].values + 1,  # 1-indexed for readability
    'journal': validation_sample[journal_col].values,
    'title': validation_sample[title_col].values,
    'abstract': validation_sample[abstract_col].fillna('No abstract available').values,
    'ai_decision': validation_sample['include'].values
})

# Save the files
df_blinded.to_csv("9_BlindedAbstracts.csv", index=False)
df_revealed.to_csv("10_RevealedAbstracts.csv", index=False)

print("\nFiles created successfully!")
print("1. Review '9_BlindedAbstracts.csv' and mark your decisions (1=include, 0=exclude)")
print("2. After review, run the analysis script to compare with AI decisions")

# Create analysis script
analysis_script = '''#Mustafa Mumtaz
#ENT Project 1
#Natural Language Processing in Otolaryngology
#Script 5: Analyze validation results

import pandas as pd
import numpy as np
from scipy import stats

print("Analyzing validation results...")

# Read the reviewed blinded abstracts (with your decisions)
try:
    df_reviewed = pd.read_csv("9_BlindedAbstracts.csv")
except UnicodeDecodeError:
    df_reviewed = pd.read_csv("9_BlindedAbstracts.csv", encoding='latin-1')
    
df_revealed = pd.read_csv("10_RevealedAbstracts.csv")

# Extract decisions
your_decisions = df_reviewed['your_decision'].values
ai_decisions = df_revealed['ai_decision'].values

# Calculate agreement
agreements = (your_decisions == ai_decisions).sum()
total = len(your_decisions)
accuracy = agreements / total

print(f"\\nResults:")
print(f"Total papers reviewed: {total}")
print(f"Agreements: {agreements}")
print(f"Disagreements: {total - agreements}")
print(f"Raw accuracy: {accuracy:.1%}")

# Binomial test (one-sided, testing if accuracy > 80%)
result = stats.binomtest(agreements, total, p=0.8, alternative='greater')
p_value = result.pvalue
print(f"\\nBinomial test (H0: accuracy ≤ 80%):")
print(f"P-value: {p_value:.4f}")

# Wilson confidence interval
ci = result.proportion_ci(confidence_level=0.95, method='wilson')
ci_low, ci_high = ci.low, ci.high
print(f"95% Confidence interval: [{ci_low:.1%}, {ci_high:.1%}]")

# Calculate Cohen's Kappa
po = accuracy  # Observed agreement
# Expected agreement by chance
n_include_you = your_decisions.sum()
n_include_ai = ai_decisions.sum()
pe = ((n_include_you * n_include_ai) + 
      ((total - n_include_you) * (total - n_include_ai))) / (total ** 2)
kappa = (po - pe) / (1 - pe) if pe != 1 else 1

print(f"\\nCohen's Kappa: {kappa:.3f}")

# Confusion matrix
tp = ((your_decisions == 1) & (ai_decisions == 1)).sum()
tn = ((your_decisions == 0) & (ai_decisions == 0)).sum()
fp = ((your_decisions == 1) & (ai_decisions == 0)).sum()
fn = ((your_decisions == 0) & (ai_decisions == 1)).sum()

print(f"\\nConfusion Matrix:")
print(f"                 AI Include  AI Exclude")
print(f"You Include      {tp:^10} {fp:^10}")
print(f"You Exclude      {fn:^10} {tn:^10}")

# Sensitivity and Specificity (using your decision as ground truth)
if n_include_you > 0:
    sensitivity = tp / n_include_you
    print(f"\\nSensitivity (AI detecting your inclusions): {sensitivity:.1%}")
if (total - n_include_you) > 0:
    specificity = tn / (total - n_include_you)
    print(f"Specificity (AI detecting your exclusions): {specificity:.1%}")

# List disagreements for review
if total - agreements > 0:
    print(f"\\nDisagreements for review:")
    for i in range(total):
        if your_decisions[i] != ai_decisions[i]:
            print(f"Row {df_revealed.loc[i, 'original_row']}: "
                  f"You={your_decisions[i]}, AI={ai_decisions[i]} - "
                  f"{df_revealed.loc[i, 'title'][:60]}...")
else:
    print(f"\\nPerfect agreement! No disagreements to review.")
'''

# Save analysis script
with open("11_AnalyzeValidation.py", "w") as f:
    f.write(analysis_script)

print("\nNext steps:")
print("1. Open '9_BlindedAbstracts.csv' in Excel or your preferred editor")
print("2. For each paper, enter 1 (include) or 0 (exclude) in the 'your_decision' column")
print("3. Save the file")
print("4. Run '11_AnalyzeValidation.py' to see the validation results")

# Print statistical power information
print("\nStatistical power notes:")
print(f"With n={n_included_sample + n_excluded_sample} and expected 95% accuracy:")
print("- Can detect accuracy ≥ 80% with >99% power")
print("- 95% CI margin of error: ±10-15%")
print("- Minimum detectable agreement for κ > 0.6: ~85%")
