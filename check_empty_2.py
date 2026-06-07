import pandas as pd
df = pd.read_excel('conference_data.xlsx')

missing_both = df[df['Speaker Job Title'].isna() & df['Speaker Company'].isna()]
print("Other columns for missing rows:")
print(missing_both[['Speaker Full Name', 'Presentation Title', 'Speaker Profile', 'Speaker Image URL']].head(10))
