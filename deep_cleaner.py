import pandas as pd

df = pd.read_excel('conference_data.xlsx')
original_len = len(df)

# 1. Delete severe garbage rows (Names that are addresses, code, or nav menus)
def is_severe_garbage(name):
    n = str(name).lower().strip()
    bad_exacts = [':', 'agenda', 'explore our bioprocessing portfolio ▼', 'explore our bioprocessing portfolio', 'explore', 'plenary', 'fireside chat:', 'phd candidate', 'phd student', 'united states']
    if n in bad_exacts: return True
    
    bad_partials = ['window._', '250 first avenue', 'life science portals', 'the clift royal', 'san francisco', '495 geary street', 'ca 94102', 'needham, ma', 'biomarkers & diagnosticsbi']
    if any(bp in n for bp in bad_partials): return True
    
    return False

df = df[~df['Speaker Full Name'].apply(is_severe_garbage)]

# 2. Fix Company/Title Split for "Inc", "LLC"
def fix_inc_split(row):
    title = str(row['Speaker Job Title']).strip()
    comp = str(row['Speaker Company']).strip()
    
    # If Company is just "Inc." or "LLC" and Title contains the real company
    if comp in ['Inc.', 'Inc', 'LLC', 'Ltd', 'Ltd.', 'Co.', 'Co', 'AG', 'GmbH', 'Corp.', 'Corp']:
        # We need to shift the last part of Title into Company
        if title and title != 'nan':
            # e.g. Title: "Senior Director, Lisata Therapeutics", Comp: "Inc."
            # Actually, because it split by comma, the Title might be "Lisata Therapeutics" and Comp "Inc."
            # So the real company is Title + ", " + Comp.
            # And the real title might be missing, or stuck in Name.
            # Let's just combine them into Company.
            # BUT wait! If original string was "John Doe, Director, Company, Inc."
            # Name: "John Doe", Title: "Director", Comp: "Company, Inc." -> wait, split max 2!
            # If it split max 2: parts[0]=Name, parts[1]=Title, parts[2]=Company.
            # If "David J Mazzo, Lisata Therapeutics, Inc." -> Name: "David J Mazzo", Title: "Lisata Therapeutics", Comp: "Inc."
            # So Title IS the company!
            row['Speaker Company'] = title + ', ' + comp
            row['Speaker Job Title'] = ''
    return row

df = df.apply(fix_inc_split, axis=1)

# 3. Clean Wayback and Hotel Summaries
def clean_deep_summary(summary):
    s = str(summary)
    if s == 'nan': return ''
    
    # Remove wayback machine banners completely
    if 'Wayback Machine' in s or "Fight for the Future" in s:
        return ''
        
    # Remove "Job title: " prefix
    if s.startswith('Job title:'):
        # We could try to extract it, but let's just strip the label
        s = s.replace('Job title:', '').strip()
        
    return s

df['Speaker Summary'] = df['Speaker Summary'].apply(clean_deep_summary)
df['Speaker Profile'] = df['Speaker Profile'].apply(clean_deep_summary)

# 4. Final PhD fix for stragglers
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
