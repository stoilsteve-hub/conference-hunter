import pandas as pd
df = pd.read_excel('conference_data.xlsx')
original_len = len(df)

company_keywords = [
    'inc', 'llc', 'ltd', 'university', 'therapeutics', 'biosciences', 'pharma', 'institute', 
    'gmbh', 'ag', 'corp', 'hospital', 'college', 'clinic', 'kgaa', 'universität', 'klinikum', 
    'biochemie', 'medical', 'center', 'school', 'biotech', 'solutions', 'health', 'care', 
    'sanofi', 'pfizer', 'novartis', 'merck', 'janssen', 'astrazeneca', 'roche', 'abbvie', 
    'bayer', 'lilly', 'gsk', 'amgen', 'gilead', 'biogen', 'regeneron', 'vertex', 'moderna', 
    'biontech', 'takeda', 'daiichi', 'astellas', 'eisai', 'otsuka', 'sun', 'reddy', 'cipla', 
    'aurobindo', 'lupin', 'zydus', 'intas', 'torrent', 'biocon', 'glenmark', 'macleods', 
    'mankind', 'alchem', 'usv', 'wockhardt', 'group', 'partner', 'consulting', 'association', 
    'society', 'council', 'network', 'fund', 'foundation', 'ventures', 'capital', 'holdings', 
    'partners', 'llp', 'pllc', 'plc', 'nv', 'bv', 'sa', 'spa', 'srl', 'sarl', 'ab', 'as', 
    'oy', 'aps', 'a/s', 'pvt', 'pte', 'sdn', 'bhd', 'co.', 'co', 'inc.', 'ltd.', 'corp.', 
    'gmbh.', 'ag.', 'llc.', 'pllc.', 'plc.', 'nv.', 'bv.', 'sa.', 'spa.', 'srl.', 'sarl.', 
    'ab.', 'as.', 'oy.', 'aps.', 'a/s.', 'pvt.', 'pte.', 'sdn.', 'bhd.'
]

dept_keywords = [
    'development', 'research', 'chemistry', 'operations', 'lab', 'strategy', 'manufacturing', 
    'controls', 'platform', 'immunology', 'discovery', 'sciences', 'biology', 'engineering', 
    'analytics', 'regulatory', 'access', 'value', 'project', 'team', 'biochemistry', 'oncology',
    'medical affairs', 'clinical', 'data', 'bioinformatics', 'computational', 'formulation', 
    'delivery', 'cmc', 'quality', 'assurance', 'qc', 'qa', 'market', 'commercial', 'sales', 
    'marketing', 'business', 'alliance', 'search', 'evaluation', 'innovation', 'technology'
]

count = 0
def fix_dept(row):
    global count
    comp = str(row['Speaker Company']).strip()
    title = str(row['Speaker Job Title']).strip()
    
    if comp and comp != 'nan':
        c_lower = comp.lower()
        
        
        if not any(k in c_lower for k in company_keywords):
            
            if any(dk in c_lower for dk in dept_keywords):
                
                if 'national research council canada' not in c_lower:
                    if title and title != 'nan':
                        row['Speaker Job Title'] = title + ', ' + comp
                    else:
                        row['Speaker Job Title'] = comp
                    row['Speaker Company'] = ''
                    count += 1
    return row

df = df.apply(fix_dept, axis=1)
print(f"Shifted {count} departments out of the Company column into the Job Title column.")
df.to_excel('conference_data.xlsx', index=False)
