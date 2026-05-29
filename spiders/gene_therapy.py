from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright
import time

class GeneTherapySpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping Gene Therapy Conference at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.url, timeout=60000)
                time.sleep(3)
                
                speakers = page.locator(".speaker-name, h3").all()
                for s in speakers[:5]:
                    name = s.inner_text().strip()
                    if name:
                        data = self.data_template.copy()
                        data["Conference Name"] = "Gene Therapy Conference"
                        data["Topic"] = "Gene Therapy"
                        data["Speaker Full Name"] = name
                        results.append(data)
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
