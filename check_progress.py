import pandas as pd
df = pd.read_excel('conference_data.xlsx')
mask = df['Speaker Job Title'].isna() & df['Speaker Company'].isna() & df['Speaker Profile'].astype(str).str.startswith('http')
print(f"Remaining targeted speakers: {mask.sum()}")
