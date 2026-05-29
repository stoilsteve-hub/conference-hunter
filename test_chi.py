from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.immunogenicitysummit.com/22/immunogenicity-prediction", timeout=60000, wait_until="networkidle")
        print("Title:", page.title())
        
        # Look for speaker elements
        speakers = page.locator("h4, .speaker, [class*='speaker']").all_text_contents()
        for s in speakers[:10]:
            print(s.strip())
            
        browser.close()

if __name__ == "__main__":
    run()
