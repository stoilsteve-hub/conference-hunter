from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.immunogenicitysummit.com/22/immunogenicity-prediction", timeout=60000, wait_until="networkidle")
        
        # Look for typical speaker elements in CHI.
        # Often it's <span class="speaker-name"> or something. Let's query selector all h4 tags and see what's in them.
        els = page.locator("h4").all()
        for i, el in enumerate(els[:5]):
            print("--- H4", i)
            print(el.inner_text())
            print(el.evaluate("el => el.innerHTML"))
            
        print("---")
        # How about b tags or strong tags that might contain speaker names?
        sp_tags = page.locator("p > b, p > strong").all()
        count = 0
        for tag in sp_tags:
            text = tag.inner_text()
            if "," in text and len(text) < 100:
                print("SPEAKER?", text)
                count += 1
                if count > 5: break
                
        browser.close()

if __name__ == "__main__":
    run()
