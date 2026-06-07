import pandas as pd
df = pd.read_excel('conference_data.xlsx')
print("--- Bad Companies ---")
print(df[df['Speaker Company'].str.contains('PhD|MD|Department|University', na=False, case=False)][['Speaker Full Name', 'Speaker Company', 'Speaker Profile']].head(10))
print("\n--- Empty Companies with Profiles ---")
print(df[df['Speaker Company'].isna() & df['Speaker Profile'].notna()][['Speaker Full Name', 'Speaker Company', 'Speaker Profile']].head(10))
