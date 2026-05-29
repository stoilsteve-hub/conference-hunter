from playwright.sync_api import sync_playwright

def inspect(url):
    print(f"\n--- Inspecting {url} ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        
        # Try to find biography text
        print("--- Text content ---")
        paragraphs = page.locator("p").all()
        for p_elem in paragraphs:
            text = p_elem.inner_text().strip()
            if len(text) > 50:
                 print(text[:100] + "...")
                 
        # Try to find images
        print("--- Images ---")
        imgs = page.locator("img").all()
        for img in imgs:
            src = img.get_attribute("src")
            if src and ("speaker" in src.lower() or "jorg" in src.lower() or "upload" in src.lower()):
                print(f"Img src: {src}")
                 
        browser.close()

inspect("https://cdx-europe.com/speaker/jorg-engelbergs/")
