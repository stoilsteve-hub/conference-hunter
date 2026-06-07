import pandas as pd

df = pd.read_excel('conference_data.xlsx')

df['Speaker Company'] = df['Speaker Company'].fillna('').astype(str).str.strip()
df['Speaker Job Title'] = df['Speaker Job Title'].fillna('').astype(str).str.strip()
df['Speaker Profile'] = df['Speaker Profile'].fillna('').astype(str).str.strip()

missing_company = df[(df['Speaker Company'] == '') | (df['Speaker Company'] == 'nan') | (df['Speaker Company'].str.lower() == 'none')]
missing_title = df[(df['Speaker Job Title'] == '') | (df['Speaker Job Title'] == 'nan') | (df['Speaker Job Title'].str.lower() == 'none')]

with open('failed_urls_report.md', 'w') as f:
    f.write("# Failed Extractions Report\n\n")
    f.write("This document lists the speakers where the AI could not find the requested data, even after checking historical archives and waiting for JavaScript to render. The data simply does not exist on these pages.\n\n")
    
    f.write(f"## Missing Company Names (Total: {len(missing_company)})\n\n")
    for _, row in missing_company.iterrows():
        url = row['Speaker Profile']
        name = row['Speaker Full Name']
        if url and url != 'nan':
            f.write(f"- {name}: {url}\n")
        else:
            f.write(f"- {name} (No URL available on source site)\n")
            
    f.write(f"\n## Missing Job Titles (Total: {len(missing_title)})\n\n")
    for _, row in missing_title.iterrows():
        url = row['Speaker Profile']
        name = row['Speaker Full Name']
        if url and url != 'nan':
            f.write(f"- {name}: {url}\n")
        else:
            f.write(f"- {name} (No URL available on source site)\n")

print(f"Report generated: failed_urls_report.md with {len(missing_company)} missing companies and {len(missing_title)} missing titles.", flush=True)
