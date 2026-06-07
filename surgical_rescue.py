import pandas as pd
from playwright.sync_api import sync_playwright
from core.ai_extractor import extract_speaker_info
import time

print("Starting Surgical Rescue Operation on conference_data.xlsx...")

df = pd.read_excel('conference_data.xlsx')


mask = (df['Speaker Job Title'].isna() | df['Speaker Company'].isna()) & df['Speaker Profile'].notna()
missing_indices = df[mask].index.tolist()

print(f"Found {len(missing_indices)} speakers missing critical data.")

if len(missing_indices) == 0:
    print("No missing data found! Dataset is perfect.")
    exit(0)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    updates = 0
    for idx in missing_indices:
        name = str(df.at[idx, 'Speaker Full Name'])
        url = str(df.at[idx, 'Speaker Profile'])
        
        print(f"\nRescuing: {name}")
        print(f"URL: {url}")
        
        try:
            
            page.goto(url, timeout=45000, wait_until="networkidle")
            
            
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            
            raw_text = page.locator("body").inner_text()
            
            if len(raw_text.strip()) < 10:
                print("Warning: Page returned almost no text. Trying iframes...")
                for frame in page.frames:
                    frame_text = frame.locator("body").inner_text()
                    if len(frame_text) > len(raw_text):
                        raw_text = frame_text
            
            print("Sending raw text to hardened AI...")
            ai_data = extract_speaker_info(raw_text)
            
            updated = False
            if ai_data["job_title"] and pd.isna(df.at[idx, 'Speaker Job Title']):
                df.at[idx, 'Speaker Job Title'] = ai_data["job_title"]
                updated = True
                print(f"  -> Recovered Title: {ai_data['job_title']}")
                
            if ai_data["company"] and pd.isna(df.at[idx, 'Speaker Company']):
                df.at[idx, 'Speaker Company'] = ai_data["company"]
                updated = True
                print(f"  -> Recovered Company: {ai_data['company']}")
                
            if ai_data["summary"] and pd.isna(df.at[idx, 'Speaker Summary']):
                df.at[idx, 'Speaker Summary'] = ai_data["summary"]
                updated = True
                print(f"  -> Recovered Summary!")
                
            if updated:
                updates += 1
                
        except Exception as e:
            print(f"Failed to rescue {name}: {e}")
            
        
        if updates > 0 and updates % 10 == 0:
            print(f"Saving intermediate progress ({updates} rows rescued)...")
            df.to_excel('conference_data.xlsx', index=False)

    browser.close()


df.to_excel('conference_data.xlsx', index=False)
print(f"\nSurgical Rescue Complete! Successfully recovered data for {updates} speakers.")
