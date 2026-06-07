import pandas as pd

df = pd.read_excel('conference_data.xlsx')

blanks = df[(df['Speaker Job Title'].isna()) & (df['Speaker Company'].isna()) & (df['Speaker Profile'].notna()) & (df['Speaker Profile'].str.contains('archive.org', na=False))]

if not blanks.empty:
    sample = blanks.iloc[0]
    print("Name:", sample['Speaker Full Name'])
    print("URL:", sample['Speaker Profile'])
else:
    print("No archive profile found with missing title/company.")
