import pandas as pd

df = pd.read_excel('conference_data.xlsx')

total = len(df)
print(f"Total Speakers: {total}")



long_names = df[df['Speaker Full Name'].astype(str).str.len() > 50]
print(f"\nNames longer than 50 chars: {len(long_names)}")


long_titles = df[df['Speaker Job Title'].astype(str).str.len() > 150]
print(f"Titles longer than 150 chars: {len(long_titles)}")


long_companies = df[df['Speaker Company'].astype(str).str.len() > 100]
print(f"Companies longer than 100 chars: {len(long_companies)}")



short_summaries = df[(df['Speaker Summary'].notna()) & (df['Speaker Summary'].astype(str).str.len() > 0) & (df['Speaker Summary'].astype(str).str.len() < 20)]
print(f"Summaries shorter than 20 chars (excluding empty ones): {len(short_summaries)}")

