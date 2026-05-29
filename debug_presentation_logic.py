from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://peptide-based-therapeutics-summit.com/speaker/tomi-sawyer/", timeout=60000, wait_until="networkidle")
    text = page.locator("body").inner_text()
    topic = ""
    if "Seminars\n" in text:
        parts = text.split("Seminars\n")[1].strip().split("\n")
        # Line 0 is usually date: Wednesday 29th April 2026
        # Line 1 is the title: Peptide Industry Leaders...
        if len(parts) > 1:
            topic = parts[1].strip()
    print("TOPIC EXTRACTED:", topic)
    browser.close()
