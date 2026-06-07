from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000, wait_until="domcontentloaded")
    print("STRONGS DOMCONTENTLOADED:", len(page.locator("p > strong, div > strong").all()))
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000) 
    print("STRONGS LOAD:", len(page.locator("p > strong, div > strong").all()))
    browser.close()
