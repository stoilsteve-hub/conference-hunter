import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os

def recover_missing_data():
    df = pd.read_excel('conference_data.xlsx')
    
    
    mask = df['Speaker Job Title'].isna() & df['Speaker Company'].isna() & df['Speaker Profile'].astype(str).str.startswith('http')
    target_rows = df[mask].index.tolist()
    
    print(f"Starting targeted recovery scrape for {len(target_rows)} speakers...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        recovered_count = 0
        for i, idx in enumerate(target_rows):
            url = str(df.at[idx, 'Speaker Profile'])
            name = str(df.at[idx, 'Speaker Full Name'])
            
            print(f"[{i+1}/{len(target_rows)}] Recovering {name} from {url}...")
            try:
                
                page.goto(url, timeout=15000, wait_until="domcontentloaded")
                
                
                title_loc = page.locator(".title, .job-title, .designation, .position").first
                if title_loc.count() > 0:
                    df.at[idx, 'Speaker Job Title'] = title_loc.text_content().strip()
                
                
                comp_loc = page.locator(".company, .organization, .org").first
                if comp_loc.count() > 0:
                    df.at[idx, 'Speaker Company'] = comp_loc.text_content().strip()
                    
                
                summ_loc = page.locator(".bio, .description, .speaker-bio, .content").first
                if summ_loc.count() > 0:
                    df.at[idx, 'Speaker Summary'] = summ_loc.text_content().strip()
                    
                recovered_count += 1
                
                
                if i % 10 == 0:
                    df.to_excel('conference_data.xlsx', index=False)
                    
            except Exception as e:
                print(f"Failed to recover {name}: {e}")
                
            time.sleep(2) 
            
        browser.close()
        
    df.to_excel('conference_data.xlsx', index=False)
    print(f"Recovery complete. Successfully pinged {recovered_count} profiles.")

if __name__ == "__main__":
    recover_missing_data()
