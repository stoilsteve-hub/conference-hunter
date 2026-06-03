import pandas as pd
import re

df = pd.read_excel('conference_data.xlsx')

def fix_topic(row):
    if row['Topic'] == 'Both':
        cname = str(row['Conference Name'])
        if ' - ' in cname:
            return cname.split(' - ')[-1].strip()
        else:
            # Try to clean up the conference name to make it a topic
            clean = re.sub(r'^\d+(th|st|nd|rd)\s+(Annual\s+)?', '', cname)
            clean = clean.replace('Conference & Expo', '').replace('Summit', '').strip()
            return clean
    return row['Topic']

df['Topic'] = df.apply(fix_topic, axis=1)
print('New unique topics count:', df['Topic'].nunique())

df.to_excel('conference_data.xlsx', index=False)
