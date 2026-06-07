import pandas as pd
df = pd.read_excel('conference_data.xlsx')
missing_job = df['Speaker Job Title'].isna() | (df['Speaker Job Title'].astype(str).str.strip() == "")
print(f"Total rows missing Job Title: {missing_job.sum()}")

missing_pres = df['Presentation Title'].isna() | (df['Presentation Title'].astype(str).str.strip() == "")
print(f"Total rows missing Presentation Title: {missing_pres.sum()}")

print("\nSample missing Job Title (where Company is populated):")
mask = missing_job & df['Speaker Company'].notna()
print(df[mask][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(10))
