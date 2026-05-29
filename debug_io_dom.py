from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000, wait_until="networkidle")
    strongs = page.locator("p > strong, div > strong").all()
    if strongs:
        try:
            print(strongs[0].evaluate("node => node.parentNode.parentNode.innerHTML"))
        except Exception as e:
            print("Error:", e)
    browser.close()
