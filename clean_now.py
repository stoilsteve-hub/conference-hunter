import pandas as pd
import re

df = pd.read_excel('conference_data.xlsx')
original_len = len(df)

# 1. Remove garbage names
garbage_exact = ['Attend', 'Learn', 'Watch', 'Speak', 'About', 'Internet', 'Images', 'Software', 'Video', 'Texts', 'Mobile', 'Browser', 'Save', 'Search', 'Donate', 'Forum', 'Real', 'BioProcess', 'Finance', 'Contract', 'Human', 'Electricity', 'Engage', 'Your', 'The', 'Revolutionizing', 'Recognizing', 'Craft', 'Quick', 'Archive-It', 'Sessions']
df = df[~df['Speaker First Name'].str.strip().isin(garbage_exact)]

# Remove "Archived Content"
df = df[~df['Speaker Full Name'].astype(str).str.contains('Archived Content')]

# 2. Scrub garbage summaries
def clean_summary(text):
    if pd.isna(text): return text
    text_str = str(text)
    if 'Omni Boston Hotel' in text_str or 'AgendaSponsor/Exhibit' in text_str or "Sorry, we couldn't find" in text_str or '450 Summer Street' in text_str or 'OVERVIEW | DOWNLOAD BROCHURE' in text_str:
        return ''
    return text

df['Speaker Summary'] = df['Speaker Summary'].apply(clean_summary)
df['Speaker Profile'] = df['Speaker Profile'].apply(clean_summary)

# 3. Fix PhD/MD title bug
def fix_phd(row):
    title = str(row['Speaker Job Title']).strip()
    if title in ['PhD', 'MD', 'Ph.D.', 'M.D.', 'MSc', 'PharmD', 'MBA', 'M.S.', 'Ph.D']:
        row['Speaker Full Name'] = str(row['Speaker Full Name']) + ', ' + title
        company_str = str(row['Speaker Company'])
        if company_str and company_str != 'nan':
            parts = [p.strip() for p in company_str.split(',')]
            if len(parts) > 1:
                row['Speaker Job Title'] = ', '.join(parts[:-1])
                row['Speaker Company'] = parts[-1]
            else:
                row['Speaker Job Title'] = company_str
                row['Speaker Company'] = ''
        else:
            row['Speaker Job Title'] = ''
            
    # Also clean Presentation Title if it says "Sessions to be Announced"
    pt = str(row['Presentation Title'])
    if 'Sessions to be Announ' in pt:
        row['Presentation Title'] = ''
        
    return row

df = df.apply(fix_phd, axis=1)

print(f"Removed {original_len - len(df)} garbage rows.")
print(f"Remaining real speakers: {len(df)}")
df.to_excel('conference_data.xlsx', index=False)
