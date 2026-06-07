import pandas as pd

df = pd.read_excel('conference_data.xlsx')

def is_corrupted(row):
    try:
        company = str(row['Speaker Company'])
        title = str(row['Speaker Job Title'])
        summary = str(row['Speaker Summary'])
        name = str(row['Speaker Full Name'])
        
        
        if len(company) > 70 and ' joined ' in company or ' previously ' in company.lower(): return True
        if len(company) > 100: return True
        
        
        if len(title) > 150: return True
        
        
        if len(summary) < 30 and summary != "nan" and summary != "": return True
        
        
        if len(name) > 50: return True
        
        return False
    except:
        return False

corrupted = df[df.apply(is_corrupted, axis=1)]
print(f"Total corrupted rows found: {len(corrupted)}")

