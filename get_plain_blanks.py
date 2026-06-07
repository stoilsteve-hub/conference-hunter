import pandas as pd

df = pd.read_excel('conference_data.xlsx')
missing_company = df[(df['Speaker Job Title'].notna()) & ((df['Speaker Company'].isna()) | (df['Speaker Company'] == ""))]

print("Here are 5 remaining genuine speakers who are missing their Company:")
for _, row in missing_company.head(5).iterrows():
    print(f"\nName: {row['Speaker Full Name']}")
    print(f"Title: {row['Speaker Job Title']}")
    print(f"Original URL: {row['Speaker Profile']}")

