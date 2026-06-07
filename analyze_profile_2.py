import pandas as pd
df = pd.read_excel('conference_data.xlsx')
mask = df['Speaker Profile'].notna() & ~df['Speaker Profile'].astype(str).str.startswith('http')
print(df[mask][['Speaker Full Name', 'Speaker Company', 'Speaker Profile']].head(10))
