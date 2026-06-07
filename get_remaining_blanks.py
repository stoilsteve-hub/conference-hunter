import pandas as pd
import urllib.request
import json

df = pd.read_excel('conference_data.xlsx')


missing_company = df[(df['Speaker Job Title'].notna()) & (df['Speaker Company'].isna()) | (df['Speaker Company'] == "")]

print("Here are 5 remaining genuine speakers who are missing their Company:")
count = 0
for _, row in missing_company.head(20).iterrows():
    if count >= 5:
        break
        
    u = str(row['Speaker Profile'])
    if pd.isna(u) or u == "nan" or "http" not in u:
        continue
        
    try:
        wayback_api = f"https://archive.org/wayback/available?url={u}"
        req = urllib.request.Request(wayback_api, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                archive_url = data['archived_snapshots']['closest']['url']
                print(f"\nName: {row['Speaker Full Name']}")
                print(f"Title: {row['Speaker Job Title']}")
                print(f"Archived URL: {archive_url}")
                count += 1
    except Exception as e:
        continue

