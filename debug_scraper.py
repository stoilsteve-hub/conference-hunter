from playwright.sync_api import sync_playwright

def inspect(url):
    print(f"\n--- Inspecting {url} ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        
        strongs = page.locator("p > strong, div > strong").all()
        for s in strongs[:10]:
            print(s.inner_text().strip())
                 
        browser.close()

inspect("https://www.immuno-oncologyeurope.com/speaker-biographies")
