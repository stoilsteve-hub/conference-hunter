from playwright.sync_api import sync_playwright

url = "https://web.archive.org/web/20220129110739/https://genetherapy-immunogenicity.com/speaker/genevieve-laforet-vice-president-clinical/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=15000, wait_until="domcontentloaded")
    text = page.locator("body").inner_text()
    
    if "Aspa" in text:
        print("Aspa FOUND with domcontentloaded")
    else:
        print("Aspa NOT FOUND with domcontentloaded")
        
    browser.close()
