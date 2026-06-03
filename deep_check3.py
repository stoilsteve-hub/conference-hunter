import pandas as pd
df = pd.read_excel('conference_data.xlsx')

title_keywords = ['Director', 'VP', 'Vice President', 'Head', 'Scientist', 'Manager', 'Officer', 'Chief', 'Professor', 'CEO', 'CTO', 'Lead', 'Founder', 'President', 'Partner', 'Principal']
company_keywords = ['Inc', 'LLC', 'Ltd', 'Corp', 'University', 'Therapeutics', 'Biosciences', 'Pharma', 'Institute', 'GmbH', 'AG', 'Co.', 'Clinic', 'Hospital', 'College']

weird_titles = []
for idx, row in df.iterrows():
    title = str(row['Speaker Job Title']).strip()
    if title and title != 'nan':
        if not any(k.lower() in title.lower() for k in title_keywords):
            weird_titles.append(title)
            
print(f"Found {len(weird_titles)} weird titles.")
for t in weird_titles[:30]:
    print(t)
