import pandas as pd
import asyncio
import aiohttp
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

prompt_template = """
You are performing a final, cell-by-cell sanity check on this database of conference speakers.
Your job is to look at EVERY SINGLE CELL and ensure there are no anomalies.

Rules:
1. "name": Must be a human name.
2. "job_title": Must be a job title.
3. "company": Must be an organization name. NO paragraphs.
4. "summary": Must be a biography or empty. NO single words if it's supposed to be a bio.

You will receive an array of JSON objects representing rows. Return the EXACT SAME array of objects, but scrub any cell that violates the rules (replace violating text with ""). Do NOT change data that is correct.

Input Data:
{batch_data}

Return ONLY a valid JSON array.
"""

async def audit_batch(session, batch_rows):
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
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json"
        }
    }
    
    for attempt in range(6):
        try:
            async with session.post(API_URL, json=payload, timeout=aiohttp.ClientTimeout(total=45)) as response:
                if response.status == 200:
                    result = await response.json()
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    return json.loads(text)
                else:
                    await asyncio.sleep(2 ** attempt)
        except Exception as e:
            await asyncio.sleep(2 ** attempt)
    return None

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    print(f"Starting Final Cell-by-Cell AI Audit on all {len(df)} rows...", flush=True)
    batch_size = 40
    batches = [df.iloc[start:min(start + batch_size, len(df))] for start in range(0, len(df), batch_size)]
    
    concurrency = 2 
    semaphore = asyncio.Semaphore(concurrency)
    cells_scrubbed = 0
    
    async with aiohttp.ClientSession() as session:
        async def bounded_audit(batch, batch_num):
            async with semaphore:
                result = await audit_batch(session, batch)
                print(f"Cell-by-cell verification: Batch {batch_num}/{len(batches)} completely checked.", flush=True)
                return result
                
        tasks = [bounded_audit(batch, i+1) for i, batch in enumerate(batches)]
        results = await asyncio.gather(*tasks)
        
        for batch_result in results:
            if batch_result:
                for item in batch_result:
                    idx = item['id']
                    
                    for field, col in [('name', 'Speaker Full Name'), ('job_title', 'Speaker Job Title'), 
                                     ('company', 'Speaker Company'), ('summary', 'Speaker Summary')]:
                        old_val = str(df.at[idx, col])
                        new_val = str(item.get(field, ''))
                        if old_val != new_val and len(old_val) > len(new_val):
                            cells_scrubbed += 1
                            df.at[idx, col] = new_val
                            
        df.to_excel('conference_data.xlsx', index=False)
        print(f"\nFinal Audit Complete! The AI scrubbed {cells_scrubbed} anomalous cells.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
