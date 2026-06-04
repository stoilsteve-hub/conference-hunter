import pandas as pd
import re

def clean_data(input_file="conference_data.xlsx", output_file="conference_data.xlsx"):
    df = pd.read_excel(input_file)
    print(f"Starting row count: {len(df)}")
    
    # 1. Clean Wayback Machine Garbage
    mask_wayback = df['Speaker Summary'].astype(str).str.contains('Wayback|bear with us', case=False, na=False)
    df.loc[mask_wayback, 'Speaker Summary'] = ""
    print(f"Cleared {mask_wayback.sum()} Wayback Machine errors from Summary.")

    mask_wayback_title = df['Presentation Title'].astype(str).str.contains('Wayback|bear with us|Sessions to be Announ', case=False, na=False)
    df.loc[mask_wayback_title, 'Presentation Title'] = ""
    print(f"Cleared {mask_wayback_title.sum()} garbage Presentation Titles.")

    # 2. Realign Job Titles from Company Column
    job_keywords = r'\b(Director|President|Officer|Scientist|Head|VP|Vice President|Manager|Investigator|Professor|Fellow|Leader|Expert|Assessor|CSO|CEO|CMO|CTO|CFO|COO|Founder|Partner|Principal|Specialist|Consultant|Advisor|Coordinator|Engineer|Analyst|Researcher)\b'
    company_mask = df['Speaker Company'].astype(str).str.contains(job_keywords, case=False, na=False)
    
    # But make sure it's not actually a company that has a job keyword in it, e.g. "Global Head, Research Unit" is a job title, not a company.
    for i, row in df[company_mask].iterrows():
        comp = str(row['Speaker Company'])
        jt = str(row['Speaker Job Title'])
        
        # If it looks like a job title, move it
        if pd.isna(row['Speaker Job Title']) or str(row['Speaker Job Title']) == "nan" or str(row['Speaker Job Title']).strip() == "":
            df.at[i, 'Speaker Job Title'] = comp
            df.at[i, 'Speaker Company'] = ""
        else:
            # Merge them if they both look like parts of a job title
            df.at[i, 'Speaker Job Title'] = f"{jt}, {comp}"
            df.at[i, 'Speaker Company'] = ""
            
    print(f"Realigned {company_mask.sum()} Job Titles that were stuck in the Company column.")

    # 3. Clean up Job Titles that were grabbed from the First Name / Last Name columns
    invalid_titles = r'^(job|title|about|agenda|explore|speaker|phd)$'
    mask_invalid_jt = df['Speaker Job Title'].astype(str).str.match(invalid_titles, case=False, na=False)
    df.loc[mask_invalid_jt, 'Speaker Job Title'] = ""
    print(f"Cleared {mask_invalid_jt.sum()} invalid Job Titles (e.g. 'title').")

    # 4. Clean up Names (Remove PhD, MD, etc.)
    degrees = r',?\s*\b(Ph\.?D\.?|M\.?D\.?|Pharm\.?D\.?|M\.?S\.?|B\.?S\.?|Sc\.?D\.?|D\.?V\.?M\.?)\b'
    df['Speaker Full Name'] = df['Speaker Full Name'].astype(str).str.replace(degrees, '', regex=True, flags=re.IGNORECASE).str.strip()
    df['Speaker Company'] = df['Speaker Company'].astype(str).str.replace(degrees, '', regex=True, flags=re.IGNORECASE).str.strip()
    
    # 5. Extract Companies from Summaries if Company is empty
    # If Company is empty, sometimes the first sentence of the Summary is the company name.
    # However, this is risky. Let's just pull out known companies if we can.
    # Let's extract any sentence ending in Inc, LLC, Corp, GmbH, Therapeutics, Pharma
    empty_company_mask = df['Speaker Company'].astype(str).replace('nan', '').str.strip() == ""
    company_keywords = r'([A-Za-z0-9\s\,\.\-]+(?:Inc\.?|LLC|Corp\.?|GmbH|Ltd\.?|Therapeutics|Pharma|University|Biosciences|Biotech))'
    
    extracted = 0
    for i, row in df[empty_company_mask].iterrows():
        summ = str(row['Speaker Summary'])
        if summ != "nan" and summ.strip():
            match = re.search(company_keywords, summ, re.IGNORECASE)
            if match:
                df.at[i, 'Speaker Company'] = match.group(1).strip()
                extracted += 1
                
    print(f"Extracted {extracted} missing companies from Speaker Summaries.")

    # 6. Realign Companies from Job Title Column
    jt_company_mask = df['Speaker Job Title'].astype(str).str.contains(r'\b(Inc\.?|LLC|Corp\.?|GmbH|Ltd\.?|Therapeutics|Pharma|University)\b', case=False, na=False)
    for i, row in df[jt_company_mask].iterrows():
        jt = str(row['Speaker Job Title'])
        comp = str(row['Speaker Company'])
        # If it looks like a company, move it
        if pd.isna(row['Speaker Company']) or str(row['Speaker Company']) == "nan" or str(row['Speaker Company']).strip() == "":
            df.at[i, 'Speaker Company'] = jt
            df.at[i, 'Speaker Job Title'] = ""
        
    print(f"Realigned {jt_company_mask.sum()} Companies that were stuck in the Job Title column.")

    df.to_excel(output_file, index=False)
    print(f"\nSaved perfectly cleaned dataset with {len(df)} rows to {output_file}")

if __name__ == "__main__":
    clean_data()
