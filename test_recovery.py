from playwright.sync_api import sync_playwright
import pandas as pd

df = pd.read_excel('conference_data.xlsx')
mask = df['Speaker Job Title'].isna() & df['Speaker Company'].isna() & df['Speaker Profile'].astype(str).str.startswith('http')
url = df[mask].iloc[0]['Speaker Profile']
print(f"Testing URL: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto(url, timeout=30000)
        print("Page loaded!")
        
        
        title_loc = page.locator(".title, .job-title, .designation, .position").first
        if title_loc.count() > 0:
            print(f"Title found: {title_loc.text_content().strip()}")
        else:
            print("Title NOT found")
            
        comp_loc = page.locator(".company, .organization, .org").first
        if comp_loc.count() > 0:
            print(f"Company found: {comp_loc.text_content().strip()}")
        else:
            print("Company NOT found")
            
    except Exception as e:
        print(f"Error: {e}")
    browser.close()
