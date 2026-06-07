import pandas as pd
df = pd.read_excel('conference_data.xlsx')

print(df[~df['Speaker Profile'].astype(str).str.startswith('http')][['Speaker Full Name', 'Speaker Company', 'Speaker Profile']].head(10))
