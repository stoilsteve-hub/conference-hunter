from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://genetherapy-conference.com/", timeout=30000, wait_until="domcontentloaded")
    print("ALL TEXT")
    print(page.locator("body").inner_text()[:1000])
    browser.close()
