from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright
import time

class ImmunoOncologySpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping Immuno-Oncology Europe at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                # Cambridge Innovation sites usually have speaker bios at /speaker-biographies
                target_url = self.url.rstrip("/") + "/speaker-biographies"
                page.goto(target_url, timeout=60000)
                time.sleep(3) # wait for dynamic load
                
                # Example of a heuristic extraction for CII sites
                speakers = page.locator("div.speaker-bio, div.speaker, .speaker-box").all()
                if not speakers:
                     # fallback to any h3 or strong tag that might be a name
                     speakers = page.locator("h3, strong").all()[:10] # limit to 10 for safety
                
                for s in speakers:
                    text = s.inner_text().strip()
                    if text and len(text.split()) < 10: # likely a name
                        data = self.data_template.copy()
                        data["Conference Name"] = "Immuno-Oncology Europe"
                        data["Topic"] = "Immuno-Oncology"
                        data["Speaker Full Name"] = text.split("\n")[0]
                        results.append(data)
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
