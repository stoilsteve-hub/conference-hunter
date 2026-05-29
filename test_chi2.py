from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.immunogenicitysummit.com/22/immunogenicity-prediction", timeout=60000, wait_until="networkidle")
        
        # In CHI websites, speakers might be listed in tables, or specific tags. Let's dump all text from main content area.
        content = page.locator("body").inner_text()
        print(content[:1000])
            
        browser.close()

if __name__ == "__main__":
    run()
