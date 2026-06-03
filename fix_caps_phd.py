import pandas as pd
df = pd.read_excel('conference_data.xlsx')
original_len = len(df)

count = 0
def fix_all_phds(row):
    global count
    title = str(row['Speaker Job Title']).strip()
    # Check ignoring case
    if title.upper() in ['PHD', 'MD', 'PH.D.', 'M.D.', 'MSC', 'PHARMD', 'MBA', 'M.S.']:
        row['Speaker Full Name'] = str(row['Speaker Full Name']) + ', ' + title
        row['Speaker Job Title'] = str(row['Speaker Company'])
        row['Speaker Company'] = ''
        count += 1
    elif title == 'Job Title':
        row['Speaker Job Title'] = ''
        
    return row

df = df.apply(fix_all_phds, axis=1)
print(f"Fixed {count} uppercase PHD/MD stragglers.")
df.to_excel('conference_data.xlsx', index=False)
