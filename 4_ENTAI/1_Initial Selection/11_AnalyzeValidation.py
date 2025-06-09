#Mustafa Mumtaz
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

print(f"\nResults:")
print(f"Total papers reviewed: {total}")
print(f"Agreements: {agreements}")
print(f"Disagreements: {total - agreements}")
print(f"Raw accuracy: {accuracy:.1%}")

# Binomial test (one-sided, testing if accuracy > 80%)
result = stats.binomtest(agreements, total, p=0.8, alternative='greater')
p_value = result.pvalue
print(f"\nBinomial test (H0: accuracy ≤ 80%):")
print(f"P-value: {p_value:.4f}")

# Wilson confidence interval - FIXED
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

print(f"\nCohen's Kappa: {kappa:.3f}")

# Confusion matrix
tp = ((your_decisions == 1) & (ai_decisions == 1)).sum()
tn = ((your_decisions == 0) & (ai_decisions == 0)).sum()
fp = ((your_decisions == 1) & (ai_decisions == 0)).sum()
fn = ((your_decisions == 0) & (ai_decisions == 1)).sum()

print(f"\nConfusion Matrix:")
print(f"                 AI Include  AI Exclude")
print(f"You Include      {tp:^10} {fp:^10}")
print(f"You Exclude      {fn:^10} {tn:^10}")

# Sensitivity and Specificity (using your decision as ground truth)
if n_include_you > 0:
    sensitivity = tp / n_include_you
    print(f"\nSensitivity (AI detecting your inclusions): {sensitivity:.1%}")
if (total - n_include_you) > 0:
    specificity = tn / (total - n_include_you)
    print(f"Specificity (AI detecting your exclusions): {specificity:.1%}")

# List disagreements for review
if total - agreements > 0:
    print(f"\nDisagreements for review:")
    for i in range(total):
        if your_decisions[i] != ai_decisions[i]:
            print(f"Row {df_revealed.loc[i, 'original_row']}: "
                  f"You={your_decisions[i]}, AI={ai_decisions[i]} - "
                  f"{df_revealed.loc[i, 'title'][:60]}...")
else:
    print(f"\nPerfect agreement! No disagreements to review.")
