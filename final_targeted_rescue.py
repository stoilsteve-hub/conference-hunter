import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from core.ai_extractor import extract_speaker_info
import os

async def process_batch(batch_df, p):
    browser = await p.chromium.launch(headless=True)
    
    async def fetch_profile(idx, row, context):
        url = str(row['Speaker Profile'])
        name = str(row['Speaker Full Name'])
        
        if pd.isna(url) or url.strip() == "" or url == "nan":
            return idx, None

        try:
            page = await context.new_page()
            
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2500) 
            
            raw_text = await page.locator("body").inner_text()
            
            
            if len(raw_text.strip()) < 50:
                for frame in page.frames:
                    try:
                        frame_text = await frame.locator("body").inner_text()
                        if len(frame_text) > len(raw_text):
                            raw_text = frame_text
                    except:
                        pass
                        
            await page.close()
            
            if len(raw_text.strip()) > 10:
                print(f"JS-Aware Rescue: {name}")
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
    
    
    missing_mask = df['Speaker Company'].isna() | df['Speaker Job Title'].isna() | (df['Speaker Company'] == "") | (df['Speaker Job Title'] == "")
    missing_df = df[missing_mask].copy()
    
    total_to_rescue = len(missing_df)
    print(f"Found {total_to_rescue} speakers to rescue using JS-Aware scraping...")
    
    batch_size = 15 
    
    async with async_playwright() as p:
        for start in range(0, total_to_rescue, batch_size):
            end = min(start + batch_size, total_to_rescue)
            batch = missing_df.iloc[start:end]
            
            results = await process_batch(batch, p)
            
            for idx, ai_data in results:
                if ai_data:
                    
                    if ai_data.get('job_title') and pd.isna(df.at[idx, 'Speaker Job Title']):
                        df.at[idx, 'Speaker Job Title'] = ai_data['job_title']
                    if ai_data.get('company') and pd.isna(df.at[idx, 'Speaker Company']):
                        df.at[idx, 'Speaker Company'] = ai_data['company']
                    if ai_data.get('summary') and pd.isna(df.at[idx, 'Speaker Summary']):
                        df.at[idx, 'Speaker Summary'] = ai_data['summary']
            
            df.to_excel('conference_data.xlsx', index=False)
            print(f"Progress: {end}/{total_to_rescue} JS-Aware profiles rescued.")
            
    print("Done! All Javascript-rendered profiles have been processed.")

if __name__ == "__main__":
    asyncio.run(main())
