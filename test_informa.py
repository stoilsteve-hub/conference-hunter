from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://informaconnect.com/bioprocessinternational/speakers/", timeout=60000, wait_until="networkidle")
        
        
        html = page.content()
        lines = html.split('\n')
        for i, line in enumerate(lines):
            if "PhD" in line or "MD" in line:
                print("Line", i, line.strip())
            
        browser.close()

if __name__ == "__main__":
    run()
