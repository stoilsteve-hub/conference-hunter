import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from core.ai_extractor import extract_speaker_info
import urllib.request
import json
import ssl
import time

def get_wayback_url(original_url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    wayback_api = f"https://archive.org/wayback/available?url={original_url}"
    try:
        req = urllib.request.Request(wayback_api, headers={'User-Agent': 'Mozilla/5.0 Conference-Data-Rescue/1.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            data = json.loads(response.read().decode())
            if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                
                return data['archived_snapshots']['closest']['url']
    except Exception as e:
        print(f"Wayback API error for {original_url}: {e}")
    return None

async def process_batch(batch_df, p):
    browser = await p.chromium.launch(headless=True)
    
    async def fetch_archive(idx, row, context):
        original_url = str(row['Speaker Profile'])
        name = str(row['Speaker Full Name'])
        
        if pd.isna(original_url) or original_url.strip() == "" or "http" not in original_url:
            return idx, None

        
        archive_url = await asyncio.to_thread(get_wayback_url, original_url)
        
        if not archive_url:
            return idx, None

        try:
            page = await context.new_page()
            
            await page.goto(archive_url, timeout=45000, wait_until="networkidle")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2500) 
            
            raw_text = await page.locator("body").inner_text()
                        
            await page.close()
            
            if len(raw_text.strip()) > 10:
                print(f"Time Machine Rescue: {name} (from {archive_url.split('/')[4]})")
                ai_data = extract_speaker_info(raw_text)
                return idx, ai_data
            else:
                return idx, None
        except Exception as e:
            return idx, None

    context = await browser.new_context()
    tasks = []
    
    for idx, row in batch_df.iterrows():
        tasks.append(fetch_archive(idx, row, context))
        
    results = await asyncio.gather(*tasks)
    await browser.close()
    return results

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    
    missing_mask = df['Speaker Company'].isna() | (df['Speaker Company'] == "")
    missing_df = df[missing_mask].copy()
    
    total_to_rescue = len(missing_df)
    print(f"Found {total_to_rescue} speakers to rescue from the past using the Time Machine Spider...")
    
    
    batch_size = 5 
    
    async with async_playwright() as p:
        for start in range(0, total_to_rescue, batch_size):
            end = min(start + batch_size, total_to_rescue)
            batch = missing_df.iloc[start:end]
            
            results = await process_batch(batch, p)
            
            for idx, ai_data in results:
                if ai_data:
                    
                    if ai_data.get('company'):
                        df.at[idx, 'Speaker Company'] = ai_data['company']
                    
                    
                    if ai_data.get('job_title') and (pd.isna(df.at[idx, 'Speaker Job Title']) or "Formerly" in str(df.at[idx, 'Speaker Job Title'])):
                        df.at[idx, 'Speaker Job Title'] = ai_data['job_title']
                        
                    
                    if ai_data.get('summary'):
                        df.at[idx, 'Speaker Summary'] = ai_data['summary']
            
            df.to_excel('conference_data.xlsx', index=False)
            print(f"Time Machine Progress: {end}/{total_to_rescue} past profiles analyzed.")
            
            
            await asyncio.sleep(2)
            
    print("Time Machine complete! Returning to the present.")

if __name__ == "__main__":
    asyncio.run(main())
