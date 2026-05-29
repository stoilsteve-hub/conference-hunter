from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.immuno-oncologyeurope.com/speaker-biographies", wait_until="networkidle")
    
    s = page.locator("p > strong, div > strong").first
    print("Found name:", s.inner_text())
    
    bio_link = s.evaluate_handle("node => { let n = node.closest('.spkr-name'); return n && n.parentElement ? Array.from(n.parentElement.querySelectorAll('a')).find(a => a.innerText.includes('Bio')) : null; }")
    if str(bio_link) != 'None' and bio_link:
        print("Clicking bio link via JS...")
        bio_link.evaluate("node => node.click()")
        try:
            page.wait_for_selector(".spkr-modal-content", timeout=5000, state="visible")
            texts = page.locator(".spkr-modal-content:visible").all_inner_texts()
            print("Modal texts:", texts)
        except Exception as e:
            print("Error:", e)
    else:
        print("No bio link found")
    browser.close()
