from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.immunogenicitysummit.com/22/immunogenicity-prediction", timeout=60000, wait_until="networkidle")
        
        
        content = page.locator("body").inner_text()
        print(content[:1000])
            
        browser.close()

if __name__ == "__main__":
    run()
