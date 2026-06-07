import pandas as pd

df = pd.read_excel('conference_data.xlsx')
original_len = len(df)


def is_severe_garbage(name):
    n = str(name).lower().strip()
    bad_exacts = [':', 'agenda', 'explore our bioprocessing portfolio ▼', 'explore our bioprocessing portfolio', 'explore', 'plenary', 'fireside chat:', 'phd candidate', 'phd student', 'united states']
    if n in bad_exacts: return True
    
    bad_partials = ['window._', '250 first avenue', 'life science portals', 'the clift royal', 'san francisco', '495 geary street', 'ca 94102', 'needham, ma', 'biomarkers & diagnosticsbi']
    if any(bp in n for bp in bad_partials): return True
    
    return False

df = df[~df['Speaker Full Name'].apply(is_severe_garbage)]


def fix_inc_split(row):
    title = str(row['Speaker Job Title']).strip()
    comp = str(row['Speaker Company']).strip()
    
    
    if comp in ['Inc.', 'Inc', 'LLC', 'Ltd', 'Ltd.', 'Co.', 'Co', 'AG', 'GmbH', 'Corp.', 'Corp']:
        
        if title and title != 'nan':
            
            
            
            
            
            
            
            
            
            
            row['Speaker Company'] = title + ', ' + comp
            row['Speaker Job Title'] = ''
    return row

df = df.apply(fix_inc_split, axis=1)


def clean_deep_summary(summary):
    s = str(summary)
    if s == 'nan': return ''
    
    
    if 'Wayback Machine' in s or "Fight for the Future" in s:
        return ''
        
    
    if s.startswith('Job title:'):
        
        s = s.replace('Job title:', '').strip()
        
    return s

df['Speaker Summary'] = df['Speaker Summary'].apply(clean_deep_summary)
df['Speaker Profile'] = df['Speaker Profile'].apply(clean_deep_summary)


def fix_phd_stragglers(row):
    title = str(row['Speaker Job Title']).strip()
    if title in ['PhD', 'MD', 'Ph.D.', 'M.D.']:
        row['Speaker Full Name'] = str(row['Speaker Full Name']) + ', ' + title
        row['Speaker Job Title'] = str(row['Speaker Company'])
        row['Speaker Company'] = ''
    return row

df = df.apply(fix_phd_stragglers, axis=1)

print(f"Removed {original_len - len(df)} severe garbage rows.")
print(f"Total pristine speakers: {len(df)}")

df.to_excel('conference_data.xlsx', index=False)
