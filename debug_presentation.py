from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://peptide-based-therapeutics-summit.com/speaker/tomi-sawyer/", timeout=60000, wait_until="networkidle")
    print("BIO PAGE TEXT:")
    print(page.locator("body").inner_text()[:1000])
    
    # also try agenda page
    try:
        page.goto("https://peptide-based-therapeutics-summit.com/agenda/", timeout=60000, wait_until="networkidle")
        print("\nAGENDA PAGE TEXT:")
        print(page.locator("body").inner_text()[:1000])
    except Exception as e:
        print("Agenda failed:", e)
    browser.close()
