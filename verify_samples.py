import pandas as pd
df = pd.read_excel('conference_data.xlsx')

print("--- Samples of Companies > 100 chars ---")
long_comps = df[df['Speaker Company'].astype(str).str.len() > 100]['Speaker Company']
for c in long_comps.head(5):
    print(c)
    print("-")

print("\n--- Samples of Summaries < 20 chars ---")
short_sums = df[(df['Speaker Summary'].notna()) & (df['Speaker Summary'].astype(str).str.len() > 0) & (df['Speaker Summary'].astype(str).str.len() < 20)]['Speaker Summary']
for s in short_sums.head(5):
    print(s)
    print("-")

