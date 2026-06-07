import pandas as pd
from google import genai
from google.genai import types
import asyncio
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

prompt_template = """
You are a strict data auditor. You are receiving a batch of speaker profiles extracted from conference websites.
Your job is to strictly verify and fix the data structure for EACH speaker. 

Rules:
1. "name": The speaker's name.
2. "job_title": The speaker's role.
3. "company": ONLY the name of the organization. If the input company contains a biography, paragraph, or long sentence (e.g. "He joined Pfizer after working at..."), you MUST move that paragraph to the "summary" field, and extract ONLY the company name (e.g. "Pfizer") for this field.
4. "summary": The full biography paragraph. If it contains random marketing bullshit (e.g. "Coffee Break", "Register now"), replace it with an empty string.

You will receive an array of JSON objects. You MUST return an array of JSON objects in the exact same order, with the exact same "id" fields, but with the data perfectly cleaned and placed into the correct columns.

Input Data:
{batch_data}

Return ONLY a valid JSON array.
"""

async def audit_batch(batch_rows):
    
    batch_data = []
    for idx, row in batch_rows.iterrows():
        batch_data.append({
            "id": idx,
            "name": str(row['Speaker Full Name']) if pd.notna(row['Speaker Full Name']) else "",
            "job_title": str(row['Speaker Job Title']) if pd.notna(row['Speaker Job Title']) else "",
            "company": str(row['Speaker Company']) if pd.notna(row['Speaker Company']) else "",
            "summary": str(row['Speaker Summary']) if pd.notna(row['Speaker Summary']) else ""
        })
    
    prompt = prompt_template.format(batch_data=json.dumps(batch_data, indent=2))
    
    for attempt in range(5):
        try:
            
            response = await asyncio.to_thread(
                client.models.generate_content,
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            data = json.loads(response.text)
            return data
        except Exception as e:
            print(f"Batch failed (attempt {attempt+1}): {e}")
            await asyncio.sleep(2 ** attempt)
    return None

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    print(f"Starting Full AI Content Audit on all {len(df)} rows...")
    batch_size = 20
    
    tasks = []
    batches = []
    
    
    for start in range(0, len(df), batch_size):
        end = min(start + batch_size, len(df))
        batch = df.iloc[start:end]
        batches.append(batch)
    
    
    concurrency = 5
    semaphore = asyncio.Semaphore(concurrency)
    
    async def bounded_audit(batch, batch_num):
        async with semaphore:
            result = await audit_batch(batch)
            print(f"Audited batch {batch_num}/{len(batches)}")
            return result
            
    for i, batch in enumerate(batches):
        tasks.append(bounded_audit(batch, i+1))
        
    print("Sending all data to Gemini...")
    results = await asyncio.gather(*tasks)
    
    fixes_made = 0
    
    for batch_result in results:
        if batch_result:
            for item in batch_result:
                idx = item['id']
                
                
                old_company = str(df.at[idx, 'Speaker Company'])
                new_company = str(item.get('company', ''))
                
                old_summary = str(df.at[idx, 'Speaker Summary'])
                new_summary = str(item.get('summary', ''))
                
                if old_company != new_company or old_summary != new_summary:
                    if len(old_company) > len(new_company): 
                        fixes_made += 1
                        
                df.at[idx, 'Speaker Full Name'] = item.get('name', df.at[idx, 'Speaker Full Name'])
                df.at[idx, 'Speaker Job Title'] = item.get('job_title', df.at[idx, 'Speaker Job Title'])
                df.at[idx, 'Speaker Company'] = item.get('company', "")
                df.at[idx, 'Speaker Summary'] = item.get('summary', "")
                
    df.to_excel('conference_data.xlsx', index=False)
    print(f"\nAudit Complete! The AI made {fixes_made} major structural corrections to eliminate bullshit/misplaced data.")

if __name__ == "__main__":
    asyncio.run(main())
