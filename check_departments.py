import pandas as pd
df = pd.read_excel('conference_data.xlsx')
mask = df['Speaker Company'].astype(str).str.contains(r'\b(Department|Dept|Division|Institute|Center|Hospital|Faculty|Lab|Laboratory|School|Program)\b', case=False, na=False)
print("--- Departments in Company Column ---")
print(df[mask][['Speaker Full Name', 'Speaker Job Title', 'Speaker Company']].head(20))
