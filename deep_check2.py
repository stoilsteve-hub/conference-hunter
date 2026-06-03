import pandas as pd
df = pd.read_excel('conference_data.xlsx')
for idx, row in df.iterrows():
    title = str(row['Speaker Job Title'])
    comp = str(row['Speaker Company'])
    if 'including third party ones' in title or 'including third party ones' in comp:
        print("FOUND:", title, "||", comp)
