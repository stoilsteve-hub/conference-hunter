import pandas as pd
df = pd.read_excel('conference_data.xlsx')

print("--- Job Titles that look like companies ---")
print(df[df['Speaker Job Title'].astype(str).str.contains('Inc|LLC|Corp|GmbH|Ltd|Therapeutics|Pharma|University', case=False, na=False)][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(10))

print("\n--- Companies that look like Job Titles ---")
print(df[df['Speaker Company'].astype(str).str.contains('Director|President|Officer|Scientist|Head|VP', case=False, na=False)][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(10))

print("\n--- Companies that look like PhD/MD ---")
print(df[df['Speaker Company'].astype(str).str.contains(r'\b(PhD|MD|Ph\.D)\b', case=False, na=False)][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(10))

print("\n--- Wayback Machine Errors in Summary ---")
print(df[df['Speaker Summary'].astype(str).str.contains('Wayback|bear with us', case=False, na=False)].shape[0])
