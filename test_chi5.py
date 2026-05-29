from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.immunogenicitysummit.com/22/immunogenicity-prediction", timeout=60000, wait_until="networkidle")
        
        lines = page.locator("body").inner_text().split("\n")
        speaker_blocks = []
        for line in lines:
            if "PhD" in line or "MD" in line or "M.D." in line or "Ph.D" in line:
                speaker_blocks.append(line.strip())
        print(f"Found {len(speaker_blocks)} speaker blocks")
        for b in speaker_blocks[:5]: print(b)
        browser.close()

if __name__ == "__main__":
    run()
