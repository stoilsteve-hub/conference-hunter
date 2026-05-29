from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for site in ["peptide-based-therapeutics-summit.com", "cdx-europe.com", "lnp-formulation-process-development-pharma.com"]:
        url = f"https://{site}/speakers/"
        response = page.goto(url, timeout=60000, wait_until="networkidle")
        links = page.locator("a").all()
        speaker_urls = set()
        for link in links:
            href = link.get_attribute("href")
            if href and "/speaker/" in href:
                speaker_urls.add(href)
        print(f"SITE: {site} STATUS: {response.status if response else 'None'} FOUND SPEAKERS: {len(speaker_urls)}")
    browser.close()
