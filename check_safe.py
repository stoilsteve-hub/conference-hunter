import pandas as pd
df = pd.read_excel('safe_data.xlsx')
print(f"Total: {len(df)}")
print(f"Missing Both: {df[(df['Speaker Job Title'].isna()) & (df['Speaker Company'].isna())].shape[0]}")
