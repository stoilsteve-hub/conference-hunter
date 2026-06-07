import pandas as pd
df = pd.read_excel('conference_data_backup.xlsx')
print(df.columns)
print(df[['Speaker Full Name', 'Speaker Summary']].head())
