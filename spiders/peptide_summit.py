from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright
import time

class PeptideSummitSpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping Peptide Summit at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.url, timeout=60000)
                time.sleep(3)
                
                # Look for speakers section or link
                # Typical wordpress/elementor structure
                speakers = page.locator(".elementor-widget-heading h3, .speaker-name").all()
                for s in speakers[:5]:
                    name = s.inner_text().strip()
                    if name:
                        data = self.data_template.copy()
                        data["Conference Name"] = "Peptide Summit"
                        data["Topic"] = "Peptides"
                        data["Speaker Full Name"] = name
                        results.append(data)
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
