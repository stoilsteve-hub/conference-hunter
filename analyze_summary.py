import pandas as pd
df = pd.read_excel('conference_data.xlsx')
mask = df['Speaker Company'].isna() & df['Speaker Summary'].notna()
print("Rows where Company is NaN but Summary is populated:")
print(df[mask][['Speaker Full Name', 'Speaker Company', 'Speaker Summary']].head(10))
