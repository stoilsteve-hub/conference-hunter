import pandas as pd
df = pd.read_excel('conference_data.xlsx')

print("--- Top 20 most common Presentation Titles ---")
titles = df['Presentation Title'].value_counts().head(20)
for t, c in titles.items():
    print(f"{c}: {str(t)[:100]}")

print("\n--- Top 20 most common Speaker Summaries ---")
summaries = df['Speaker Summary'].value_counts().head(20)
for s, c in summaries.items():
    print(f"{c}: {str(s)[:100]}")
