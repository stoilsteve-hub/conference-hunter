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
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            raw_text = await page.locator("body").inner_text()
            await page.close()
            
            if len(raw_text.strip()) > 10:
                print(f"Deep scraping targeted rescue: {name}")
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
    
    df_clean = pd.read_excel('conference_data.xlsx')
    df_backup = pd.read_excel('conference_data_backup.xlsx')
    
    
    clean_urls = set(df_clean['Speaker Profile'].dropna().unique())
    missing_df = df_backup[~df_backup['Speaker Profile'].isin(clean_urls)].copy()
    
    
    garbage_words = ["PLENARY", "PEGS", "SPONSOR", "EXHIBITOR", "SCENES FROM", "FIRESIDE CHAT", "BREAK", "LUNCH", "CHAIR", "PANEL", "REGISTRATION"]
    
    def is_human(name):
        name_up = str(name).upper()
        if len(name_up) < 4: return False 
        for word in garbage_words:
            if word in name_up:
                return False
        return True
        
    missing_humans = missing_df[missing_df['Speaker Full Name'].apply(is_human)].copy()
    
    total_to_rescue = len(missing_humans)
    print(f"Found {total_to_rescue} legitimate missing human speakers to rescue!")
    
    
    batch_size = 20
    async with async_playwright() as p:
        for start in range(0, total_to_rescue, batch_size):
            end = min(start + batch_size, total_to_rescue)
            batch = missing_humans.iloc[start:end]
            
            results = await process_batch(batch, p)
            
            for idx, ai_data in results:
                if ai_data:
                    missing_humans.at[idx, 'Speaker Job Title'] = ai_data.get('job_title', "")
                    missing_humans.at[idx, 'Speaker Company'] = ai_data.get('company', "")
                    missing_humans.at[idx, 'Speaker Summary'] = ai_data.get('summary', "")
            
            print(f"Targeted Progress: {end}/{total_to_rescue} scraped.")
    
    
    final_df = pd.concat([df_clean, missing_humans], ignore_index=True)
    final_df.to_excel('conference_data.xlsx', index=False)
    print(f"Done! Final dataset size is now {len(final_df)}.")

if __name__ == "__main__":
    asyncio.run(main())
