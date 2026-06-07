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
                print(f"Rescuing: {name}")
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

def is_empty(val):
    if pd.isna(val):
        return True
    val_str = str(val).strip().lower()
    if val_str == "" or val_str == "nan" or val_str == "none":
        return True
    return False

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    # We explicitly check for empty strings, NaN strings, and true NaNs
    missing_mask = df['Speaker Company'].apply(is_empty) | df['Speaker Job Title'].apply(is_empty)
    missing_df = df[missing_mask].copy()
    
    total_to_rescue = len(missing_df)
    print(f"Found {total_to_rescue} speakers to rescue because of the Pandas string bug...")
    
    batch_size = 15 
    
    async with async_playwright() as p:
        for start in range(0, total_to_rescue, batch_size):
            end = min(start + batch_size, total_to_rescue)
            batch = missing_df.iloc[start:end]
            
            results = await process_batch(batch, p)
            
            for idx, ai_data in results:
                if ai_data:
                    # THE FIX: Properly check if the cell is empty before writing, using is_empty() instead of pd.isna()
                    if ai_data.get('job_title') and is_empty(df.at[idx, 'Speaker Job Title']):
                        df.at[idx, 'Speaker Job Title'] = ai_data['job_title']
                    if ai_data.get('company') and is_empty(df.at[idx, 'Speaker Company']):
                        df.at[idx, 'Speaker Company'] = ai_data['company']
                    if ai_data.get('summary') and is_empty(df.at[idx, 'Speaker Summary']):
                        df.at[idx, 'Speaker Summary'] = ai_data['summary']
            
            df.to_excel('conference_data.xlsx', index=False)
            print(f"Progress: {end}/{total_to_rescue} profiles rescued and properly saved.")
            
    print("Done! The lost data has been permanently secured in the Excel file.")

if __name__ == "__main__":
    asyncio.run(main())
