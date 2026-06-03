import pandas as pd
df = pd.read_excel('conference_data.xlsx')

count = 0
company_indicators = ['Klinikum', 'Universität', 'University', 'Biochemie', 'KGaA', 'Inc', 'LLC', 'Ltd', 'Therapeutics', 'Biosciences', 'Pharma', 'Institute', 'GmbH', 'AG', 'Corp', 'Hospital', 'College', 'Clinic']
title_indicators = ['Director', 'VP', 'Head', 'Scientist', 'Manager', 'Officer', 'Chief', 'Professor', 'CEO', 'CTO', 'Lead', 'Founder', 'President']

def fix_swapped(row):
    global count
    title = str(row['Speaker Job Title']).strip()
    comp = str(row['Speaker Company']).strip()
    
    # If Company is empty, and Title contains Company words but NO Title words
    if (comp == 'nan' or comp == '') and title and title != 'nan':
        if any(ci.lower() in title.lower() for ci in company_indicators):
            if not any(ti.lower() in title.lower() for ti in title_indicators):
                row['Speaker Company'] = title
                row['Speaker Job Title'] = ''
                count += 1
    return row

df = df.apply(fix_swapped, axis=1)
print(f"Shifted {count} orphaned Companies from Job Title into the Company column.")
df.to_excel('conference_data.xlsx', index=False)
