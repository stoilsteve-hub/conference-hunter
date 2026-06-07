import pandas as pd

df = pd.read_excel('conference_data.xlsx')

mask = df['Speaker Profile'].notna() & ~df['Speaker Profile'].astype(str).str.startswith('http')
bad_profiles = df[mask]
print("Rows where Profile is populated but NOT a URL:")
print(bad_profiles[['Speaker Full Name', 'Speaker Company', 'Speaker Profile']].head(20))
