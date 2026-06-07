import pandas as pd

df = pd.read_excel('conference_data.xlsx')
total = len(df)
missing_title = df['Speaker Job Title'].isna().sum()
missing_company = df['Speaker Company'].isna().sum()
missing_both = df[(df['Speaker Job Title'].isna()) & (df['Speaker Company'].isna())].shape[0]

print(f"Total Speakers: {total}")
print(f"Missing Job Title: {missing_title}")
print(f"Missing Company: {missing_company}")
print(f"Missing Both: {missing_both}")


print("\nSample of missing both:")
print(df[(df['Speaker Job Title'].isna()) & (df['Speaker Company'].isna())][['Speaker Full Name', 'Conference Name']].head())

