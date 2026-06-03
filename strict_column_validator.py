import pandas as pd
import re

df = pd.read_excel('conference_data.xlsx')

print("--- COMMENCING COLUMN-BY-COLUMN STRICT VALIDATION ---")

# 1. SPEAKER FIRST NAME COLUMN
print("\n[CHECKING]: Speaker First Name Column")
invalid_first_names = 0
for idx, fn in df['Speaker First Name'].items():
    fn_str = str(fn).strip()
    # A first name shouldn't have spaces, numbers, or be common UI words
    if ' ' in fn_str or any(c.isdigit() for c in fn_str) or fn_str.lower() in ['job', 'title', 'about', 'agenda', 'explore', 'speaker', 'phd']:
        invalid_first_names += 1
        df.at[idx, 'Speaker First Name'] = ''

print(f" -> Found and cleared {invalid_first_names} suspicious First Names.")

# 2. SPEAKER FULL NAME COLUMN
print("\n[CHECKING]: Speaker Full Name Column")
invalid_full_names = 0
rows_to_drop = []
for idx, fn in df['Speaker Full Name'].items():
    fn_str = str(fn).strip()
    if not fn_str or fn_str == 'nan':
        rows_to_drop.append(idx)
        continue
    # A full name shouldn't be a massive sentence
    if len(fn_str.split()) > 6 and 'PhD' not in fn_str and 'MD' not in fn_str:
        invalid_full_names += 1
        rows_to_drop.append(idx)
        
print(f" -> Found {invalid_full_names} sentences masking as Full Names. Dropping rows.")
df = df.drop(rows_to_drop)
df = df.reset_index(drop=True)

# 3. SPEAKER JOB TITLE COLUMN
print("\n[CHECKING]: Speaker Job Title Column")
invalid_job_titles = 0
for idx, jt in df['Speaker Job Title'].items():
    jt_str = str(jt).strip()
    if jt_str.lower() == 'job title' or jt_str.lower() == 'title' or jt_str.upper() == 'PHD':
        invalid_job_titles += 1
        df.at[idx, 'Speaker Job Title'] = ''
        
print(f" -> Found and cleared {invalid_job_titles} invalid Job Titles.")

# 4. SPEAKER COMPANY COLUMN
print("\n[CHECKING]: Speaker Company Column")
invalid_companies = 0
for idx, comp in df['Speaker Company'].items():
    comp_str = str(comp).strip()
    if comp_str.lower() in ['company', 'organization']:
        invalid_companies += 1
        df.at[idx, 'Speaker Company'] = ''
        
print(f" -> Found and cleared {invalid_companies} invalid Companies.")

# 5. PRESENTATION TITLE COLUMN
print("\n[CHECKING]: Presentation Title Column")
invalid_pres = 0
for idx, pt in df['Presentation Title'].items():
    pt_str = str(pt).strip()
    if 'Sessions to be Announ' in pt_str:
        invalid_pres += 1
        df.at[idx, 'Presentation Title'] = ''
        
print(f" -> Found and cleared {invalid_pres} placeholder Presentation Titles.")

# 6. SPEAKER SUMMARY COLUMN
print("\n[CHECKING]: Speaker Summary Column")
invalid_summaries = 0
for idx, summ in df['Speaker Summary'].items():
    summ_str = str(summ).strip()
    if 'Wayback Machine' in summ_str or summ_str.startswith('Job title:'):
        invalid_summaries += 1
        df.at[idx, 'Speaker Summary'] = ''
        
print(f" -> Found and cleared {invalid_summaries} garbage Summaries.")

print(f"\n--- VALIDATION COMPLETE. {len(df)} PERFECT ROWS REMAIN ---")
df.to_excel('conference_data.xlsx', index=False)
