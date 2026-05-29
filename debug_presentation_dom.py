from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://peptide-based-therapeutics-summit.com/speaker/tomi-sawyer/", timeout=60000, wait_until="networkidle")
    seminar_heading = page.locator("h3:has-text('Seminars'), h2:has-text('Seminars')")
    if seminar_heading.count() > 0:
        parent = seminar_heading.first.evaluate_handle("node => node.parentNode")
        print("PARENT HTML:")
        print(parent.inner_html())
    else:
        print("No seminar heading found")
    browser.close()
