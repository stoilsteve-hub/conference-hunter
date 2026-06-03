import pandas as pd
import re

df = pd.read_excel('conference_data.xlsx')
original_len = len(df)
issues = 0

def validate_and_clean(row):
    global issues
    
    # 1. First Name
    fn = str(row['Speaker First Name']).strip()
    if fn and fn != 'nan':
        # First name should generally be one or two words, no numbers, no weird symbols
        if len(fn.split()) > 2 or any(char.isdigit() for char in fn) or fn.lower() in ['job', 'title', 'phd', 'md', 'speaker', 'mr', 'mrs', 'dr', 'dr.']:
            # Maybe it's a prefix or just garbage.
            # We'll just note it, but if it's literally "Job Title" we wipe it.
            if fn.lower() in ['job', 'title', 'job title']:
                row['Speaker First Name'] = ''
                issues += 1
                
    # 2. Full Name
    fn_full = str(row['Speaker Full Name']).strip()
    if fn_full.lower() == 'job title' or 'window._' in fn_full:
        row['Speaker Full Name'] = ''
        issues += 1
        
    # 3. Job Title
    jt = str(row['Speaker Job Title']).strip()
    if jt and jt != 'nan':
        if jt.lower() == 'job title' or jt.lower() == 'title':
            row['Speaker Job Title'] = ''
            issues += 1
        elif jt.upper() in ['PHD', 'MD', 'PH.D.', 'M.D.', 'MSC', 'PHARMD', 'MBA', 'M.S.']:
            # Still somehow a degree?
            row['Speaker Job Title'] = ''
            row['Speaker Full Name'] = fn_full + ', ' + jt
            issues += 1
            
    # 4. Company
    comp = str(row['Speaker Company']).strip()
    if comp and comp != 'nan':
        if comp.lower() in ['company', 'organization', 'inc', 'llc']: # just 'inc' is bad
            row['Speaker Company'] = ''
            issues += 1

    # 5. Summary
    summ = str(row['Speaker Summary']).strip()
    if summ and summ != 'nan':
        if summ.lower().startswith('job title:'):
            row['Speaker Summary'] = summ[10:].strip()
            issues += 1
        if 'wayback machine' in summ.lower():
            row['Speaker Summary'] = ''
            issues += 1
            
    return row

df = df.apply(validate_and_clean, axis=1)

# Drop rows where First Name AND Full Name are empty
df = df.dropna(subset=['Speaker Full Name'])
df = df[df['Speaker Full Name'].str.strip() != '']
df = df[df['Speaker Full Name'].str.strip() != 'nan']

print(f"Fixed {issues} minor cell-level issues.")
print(f"Dropped {original_len - len(df)} empty speaker rows.")
print(f"Final strict valid speakers: {len(df)}")

df.to_excel('conference_data.xlsx', index=False)
