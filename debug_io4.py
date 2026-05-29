from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000, wait_until="networkidle")
    print("STRONGS NETWORKIDLE:", len(page.locator("p > strong, div > strong").all()))
    browser.close()
