import pandas as pd

df = pd.read_excel('conference_data.xlsx')

issues = {
    'window': [],
    'agenda_explore': [],
    'address_speakers': [],
    'wayback_summaries': [],
    'phd_still_in_title': [],
    'inc_in_company': [],
    'job_title_in_summary': []
}

for idx, row in df.iterrows():
    name = str(row['Speaker Full Name'])
    title = str(row['Speaker Job Title'])
    comp = str(row['Speaker Company'])
    summary = str(row['Speaker Summary'])
    
    if 'window._' in name or 'window.' in name:
        issues['window'].append(name)
    if name.lower() in ['agenda', 'explore our bioprocessing portfolio ▼', 'explore our bioprocessing portfolio', 'explore', 'plenary', 'fireside chat:', 'phd candidate', 'phd student']:
        issues['agenda_explore'].append(name)
    if '250 first avenue' in name.lower() or 'life science portals' in name.lower() or 'the clift royal' in name.lower() or 'san francisco' in name.lower() or 'united states' == name.lower():
        issues['address_speakers'].append(name)
    if 'wayback machine' in summary.lower():
        issues['wayback_summaries'].append(summary)
    if title in ['PhD', 'MD', 'Ph.D.', 'M.D.']:
        issues['phd_still_in_title'].append(name)
    if comp.strip() in ['Inc.', 'Inc', 'LLC', 'Ltd', 'Co.', 'Co']:
        issues['inc_in_company'].append(comp)
    if summary.startswith('Job title:'):
        issues['job_title_in_summary'].append(summary)

print("Errors in current conference_data.xlsx:")
for k, v in issues.items():
    print(f"{k}: {len(v)}")
    
