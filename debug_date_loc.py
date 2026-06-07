from playwright.sync_api import sync_playwright

def inspect(url):
    print(f"\n--- Inspecting {url} ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        print("TITLE:", page.title())
        
        
        text = page.locator("body").inner_text()
        lines = text.split('\n')
        for line in lines[:30]:
            if "|" in line and any(m in line.lower() for m in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]):
                print("FOUND DATE/LOC:", line.strip())
                 
        browser.close()

inspect("https://peptide-based-therapeutics-summit.com/")
inspect("https://lnp-formulation-process-development-pharma.com/")
inspect("https://genetherapy-conference.com/")
