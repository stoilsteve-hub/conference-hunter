from playwright.sync_api import sync_playwright
import sys

def test(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="networkidle")
        
        # Method 1: Find all links and check inner text
        links = page.locator("a").all()
        found_url = None
        for a in links:
            try:
                text = a.inner_text().strip().lower()
                href = a.get_attribute("href")
                if "speaker" in text and href and href != "#" and "mailto:" not in href:
                    if href.startswith("/"):
                        found_url = url.rstrip("/") + href
                    else:
                        found_url = href
                    # Prefer exact match or something reasonable
                    if "/speaker" in found_url.lower():
                        break
            except Exception:
                pass
                
        print(f"Found speaker URL for {url}: {found_url}")
        browser.close()

if __name__ == '__main__':
    test("https://treg-directed-therapies.com/")
    test("https://www.nasal-formulation-delivery.com/")
