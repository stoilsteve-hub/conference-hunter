import pandas as pd
df = pd.read_excel('conference_data.xlsx')

missing_both = df[df['Speaker Job Title'].isna() & df['Speaker Company'].isna()]
print(f"Total rows: {len(df)}")
print(f"Rows missing BOTH Job Title and Company: {len(missing_both)}")
print("\nSample of rows missing both:")
print(missing_both[['Speaker Full Name', 'Speaker Summary']].head(10))
