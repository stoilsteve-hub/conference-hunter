import pandas as pd
import re

def ruthless_clean():
    df = pd.read_excel('conference_data.xlsx')
    
    initial_rows = len(df)
    
    
    
    long_jt_mask = df['Speaker Job Title'].astype(str).str.len() > 80
    long_comp_mask = df['Speaker Company'].astype(str).str.len() > 80
    
    moved_bios = 0
    for i, row in df[long_jt_mask | long_comp_mask].iterrows():
        jt = str(row['Speaker Job Title'])
        comp = str(row['Speaker Company'])
        summ = str(row['Speaker Summary'])
        
        bio_text = ""
        if len(jt) > 80:
            bio_text = jt
            df.at[i, 'Speaker Job Title'] = ""
            
        if len(comp) > 80:
            
            if len(comp) > len(bio_text) and comp not in bio_text:
                bio_text += " " + comp
            df.at[i, 'Speaker Company'] = ""
            
        
        if pd.isna(row['Speaker Summary']) or summ == 'nan' or len(summ) < 10:
            df.at[i, 'Speaker Summary'] = bio_text.strip()
            moved_bios += 1
            
    print(f"Erased {long_jt_mask.sum()} massive paragraphs from Job Title column.")
    print(f"Erased {long_comp_mask.sum()} massive paragraphs from Company column.")
    print(f"Migrated {moved_bios} of those paragraphs to empty Summary columns.")

    
    dept_keywords = r'\b(Department|Dept|Division|Institute|Center|Hospital|Faculty|Lab|Laboratory|School|Program)\b'
    dept_mask = df['Speaker Company'].astype(str).str.contains(dept_keywords, case=False, na=False)
    
    
    moved_depts = 0
    for i, row in df[dept_mask].iterrows():
        comp = str(row['Speaker Company']).strip()
        jt = str(row['Speaker Job Title']).strip()
        
        if comp and comp != 'nan':
            
            if pd.isna(row['Speaker Job Title']) or jt == 'nan' or jt == "":
                df.at[i, 'Speaker Job Title'] = comp
            elif comp not in jt:
                df.at[i, 'Speaker Job Title'] = f"{jt}, {comp}"
                
            df.at[i, 'Speaker Company'] = ""
            moved_depts += 1
            
    print(f"Purged {dept_mask.sum()} academic departments from Company column (and appended to Job Title).")

    
    
    empty_company_mask = df['Speaker Company'].astype(str).replace('nan', '').str.strip() == ""
    company_keywords = r'([A-Z][A-Za-z0-9\s\,\.\-]+(?:Inc\.?|LLC|Corp\.?|GmbH|Ltd\.?|Therapeutics|Pharma|Biosciences|Biotech|Ag|S\.A\.?|N\.V\.?|B\.V\.?|AB|SpA|Srl|Oy|A/S|Ltd|Pty))'
    
    extracted = 0
    for i, row in df[empty_company_mask].iterrows():
        summ = str(row['Speaker Summary'])
        if summ != "nan" and summ.strip():
            match = re.search(company_keywords, summ) 
            if match:
                df.at[i, 'Speaker Company'] = match.group(1).strip()
                extracted += 1
                
    print(f"Extracted {extracted} actual corporate entities from Summaries to fill the void.")
    
    
    df['Speaker Job Title'] = df['Speaker Job Title'].astype(str).replace('nan', '').str.strip(', ')
    df['Speaker Company'] = df['Speaker Company'].astype(str).replace('nan', '').str.strip(', ')
    
    df.to_excel('conference_data.xlsx', index=False)
    print(f"Ruthless clean complete. Dataset retains {len(df)} rows.")

if __name__ == "__main__":
    ruthless_clean()
