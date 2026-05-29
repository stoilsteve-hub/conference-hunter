from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    response = page.goto("https://genetherapy-conference.com/speakers/", timeout=60000, wait_until="networkidle")
    print("STATUS:", response.status)
    links = page.locator("a").all()
    speaker_urls = set()
    for link in links:
        href = link.get_attribute("href")
        if href and "/speaker/" in href:
            speaker_urls.add(href)
    print("FOUND SPEAKERS:", len(speaker_urls))
    browser.close()
