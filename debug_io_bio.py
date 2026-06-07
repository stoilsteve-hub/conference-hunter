from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", timeout=60000, wait_until="networkidle")
    
    bio_link = page.locator("a:has-text('Bio')").first
    bio_link.click()
    page.wait_for_selector(".spkr-modal-content", timeout=10000)
    print("MODAL TEXT:")
    print(page.locator(".spkr-modal-content").inner_text())
    browser.close()
