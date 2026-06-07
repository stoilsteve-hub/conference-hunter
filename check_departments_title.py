import pandas as pd
df = pd.read_excel('conference_data.xlsx')

print("--- Long biographies in Job Title column ---")
mask_long = df['Speaker Job Title'].astype(str).str.len() > 100
print(df[mask_long][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(10))

print("\n--- Long biographies in Company column ---")
mask_long_comp = df['Speaker Company'].astype(str).str.len() > 100
print(df[mask_long_comp][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(10))
