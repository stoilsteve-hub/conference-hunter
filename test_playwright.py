from playwright.sync_api import sync_playwright

url = "https://web.archive.org/web/20220129110739/https://genetherapy-immunogenicity.com/speaker/genevieve-laforet-vice-president-clinical/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000, wait_until="networkidle")
    
    text = page.locator("body").inner_text()
    
    print("--- INNER TEXT ---")
    print(text[:2000])
    print("--- SEARCH FOR TITLE ---")
    if "Vice President" in text:
        print("Found Vice President in inner_text")
    else:
        print("Vice President NOT in inner_text")
        
    if "Aspa" in text:
        print("Found Aspa in inner_text")
    else:
        print("Aspa NOT in inner_text")
        
    print("\n--- TRYING iframes ---")
    for frame in page.frames:
        frame_text = frame.locator("body").inner_text()
        if "Aspa" in frame_text:
            print("Found Aspa in iframe:", frame.name)
            
    browser.close()
