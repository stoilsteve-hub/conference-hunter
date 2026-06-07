import pandas as pd
import re

df = pd.read_excel('conference_data.xlsx')

issues = {
    'long_names': [],
    'title_in_company': [],
    'company_in_title': [],
    'garbage_names': [],
    'urls_in_wrong_places': [],
    'empty_names': []
}

title_keywords = ['Director', 'VP', 'Vice President', 'Head', 'Scientist', 'Manager', 'Officer', 'Chief', 'Professor', 'CEO', 'CTO', 'Lead', 'Founder']
company_keywords = ['Inc', 'LLC', 'Ltd', 'Corp', 'University', 'Therapeutics', 'Biosciences', 'Pharma', 'Institute', 'GmbH', 'AG', 'Co.']
garbage_keywords = ['Panel', 'Chair', 'Moderator', 'Session', 'Welcome', 'Coffee', 'Break', 'Networking', 'Breakfast', 'Lunch', 'Dinner']

for idx, row in df.iterrows():
    name = str(row['Speaker Full Name']).strip()
    title = str(row['Speaker Job Title']).strip()
    company = str(row['Speaker Company']).strip()
    
    
    if name == 'nan' or not name:
        issues['empty_names'].append(idx)
        continue
        
    
    if len(name) > 40 or len(name.split()) > 5:
        issues['long_names'].append((idx, name))
        
    
    if any(k.lower() in name.lower() for k in garbage_keywords):
        issues['garbage_names'].append((idx, name))
        
    
    if 'http' in name or 'http' in title or 'http' in company:
        issues['urls_in_wrong_places'].append(idx)
        
    
    if company != 'nan' and any(k.lower() in company.lower() for k in title_keywords):
        
        if not any(c.lower() in company.lower() for c in company_keywords):
            issues['title_in_company'].append((idx, company))
            
    
    if title != 'nan' and any(k.lower() in title.lower() for k in company_keywords):
        if not any(t.lower() in title.lower() for t in title_keywords):
            issues['company_in_title'].append((idx, title))

print(f"Total Rows Checked: {len(df)}")
print(f"Empty Names: {len(issues['empty_names'])}")
print(f"Long/Suspicious Names: {len(issues['long_names'])}")
print(f"Event/Garbage Names: {len(issues['garbage_names'])}")
print(f"URLs in wrong places: {len(issues['urls_in_wrong_places'])}")
print(f"Titles accidentally in Company column: {len(issues['title_in_company'])}")
print(f"Companies accidentally in Title column: {len(issues['company_in_title'])}")

if issues['long_names']:
    print("\nExamples of Long Names:")
    for _, n in issues['long_names'][:5]: print(f" - {n}")

if issues['garbage_names']:
    print("\nExamples of Event/Garbage Names:")
    for _, n in issues['garbage_names'][:5]: print(f" - {n}")

if issues['title_in_company']:
    print("\nExamples of Titles in Company column:")
    for _, c in issues['title_in_company'][:5]: print(f" - {c}")

if issues['company_in_title']:
    print("\nExamples of Companies in Title column:")
    for _, t in issues['company_in_title'][:5]: print(f" - {t}")

