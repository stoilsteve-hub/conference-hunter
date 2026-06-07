import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from core.ai_extractor import extract_speaker_info
import sys
import time
import math

async def process_batch(batch_df, start_idx, p):
    browser = await p.chromium.launch(headless=True)
    
    async def fetch_profile(idx, row, context):
        url = str(row['Speaker Profile'])
        name = str(row['Speaker Full Name'])
        
        if pd.isna(url) or url.strip() == "" or url == "nan":
            return idx, None

        try:
            page = await context.new_page()
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            raw_text = await page.locator("body").inner_text()
            await page.close()
            
            if len(raw_text.strip()) > 10:
                print(f"Deep scraping: {name}")
                
                ai_data = extract_speaker_info(raw_text)
                return idx, ai_data
            else:
                return idx, None
        except Exception as e:
            
            return idx, None

    context = await browser.new_context()
    tasks = []
    
    for idx, row in batch_df.iterrows():
        tasks.append(fetch_profile(idx, row, context))
        
    results = await asyncio.gather(*tasks)
    await browser.close()
    return results

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    total_rows = len(df)
    batch_size = 20 
    
    print(f"Starting Turbo Scrape for {total_rows} rows...")
    
    async with async_playwright() as p:
        for start in range(0, total_rows, batch_size):
            end = min(start + batch_size, total_rows)
            batch = df.iloc[start:end]
            
            results = await process_batch(batch, start, p)
            
            for idx, ai_data in results:
                if ai_data:
                    df.at[idx, 'Speaker Job Title'] = ai_data.get('job_title', "")
                    df.at[idx, 'Speaker Company'] = ai_data.get('company', "")
                    df.at[idx, 'Speaker Summary'] = ai_data.get('summary', "")
            
            
            df.to_excel('conference_data.xlsx', index=False)
            print(f"Progress: {end}/{total_rows} saved.")

if __name__ == "__main__":
    asyncio.run(main())
