from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000, wait_until="networkidle")
    strongs = page.locator("p > strong, div > strong").all()
    for s in strongs:
        name = s.inner_text().strip()
        if name not in ["Cookie Policy", "Warning!", "Filter by:", ""] and len(name.split()) > 1:
            try:
                print("---", name)
                print(s.evaluate("node => node.parentNode.parentNode.innerHTML"))
            except Exception as e:
                pass
            break
    browser.close()
