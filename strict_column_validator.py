import pandas as pd
from google import genai
from google.genai import types
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

df = pd.read_excel('conference_data.xlsx')

def is_corrupted(row):
    try:
        company = str(row['Speaker Company'])
        title = str(row['Speaker Job Title'])
        summary = str(row['Speaker Summary'])
        name = str(row['Speaker Full Name'])
        
        if len(company) > 70 and (' joined ' in company or ' previously ' in company.lower()): return True
        if len(company) > 100: return True
        if len(title) > 150: return True
        if len(summary) < 30 and summary != "nan" and summary != "": return True
        if len(name) > 50: return True
        
        return False
    except:
        return False

corrupted_mask = df.apply(is_corrupted, axis=1)
corrupted_indices = df[corrupted_mask].index.tolist()

print(f"Starting Gemini Verification on {len(corrupted_indices)} misplaced rows...")

prompt_template = """
The following speaker data has been improperly formatted. The biography paragraph might be in the "company" field, or the job title might be in the "summary" field. 
Please reorganize the data into the correct keys.

Rules:
- "name": The speaker's name.
- "job_title": The speaker's role (e.g., CEO, Director).
- "company": ONLY the name of the organization (e.g., Pfizer, Stanford University). NO biographies or paragraphs here.
- "summary": The full biography paragraph.

Raw corrupted data:
Name: {name}
Job Title: {title}
Company: {company}
Summary: {summary}

Return ONLY a valid JSON object with keys "name", "job_title", "company", "summary".
"""

def fix_row(idx):
    row = df.loc[idx]
    prompt = prompt_template.format(
        name=row['Speaker Full Name'],
        title=row['Speaker Job Title'],
        company=row['Speaker Company'],
        summary=row['Speaker Summary']
    )
    
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            data = json.loads(response.text)
            return idx, data
        except Exception as e:
            time.sleep(2 ** attempt)
    return idx, None

processed = 0
total = len(corrupted_indices)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fix_row, idx): idx for idx in corrupted_indices}
    
    for future in as_completed(futures):
        idx, data = future.result()
        processed += 1
        
        if data:
            df.at[idx, 'Speaker Full Name'] = data.get('name', df.at[idx, 'Speaker Full Name'])
            df.at[idx, 'Speaker Job Title'] = data.get('job_title', "")
            df.at[idx, 'Speaker Company'] = data.get('company', "")
            df.at[idx, 'Speaker Summary'] = data.get('summary', "")
            
        if processed % 50 == 0 or processed == total:
            print(f"Verified & Fixed: {processed}/{total}")
            df.to_excel('conference_data.xlsx', index=False)

print("Verification complete! Spreadsheet has been scrubbed.")
