from playwright.sync_api import sync_playwright

def inspect(url):
    print(f"\n--- Inspecting {url} ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        
        paragraphs = page.locator(".hw-speaker-content p").all()
        for p_elem in paragraphs:
            print(p_elem.inner_text().strip())
                 
        browser.close()

inspect("https://peptide-based-therapeutics-summit.com/speaker/tomi-sawyer/")
inspect("https://genetherapy-conference.com/speaker/damir-simic/")
