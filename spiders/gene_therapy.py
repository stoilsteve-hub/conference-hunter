from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright

class GeneTherapySpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping Gene Therapy Conference at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.url, timeout=60000)
                
                links = page.locator("a").all()
                for link in links:
                    href = str(link.get_attribute("href"))
                    text = link.inner_text().strip()
                    if "/speaker/" in href and "\n" in text:
                        lines = text.split("\n")
                        if len(lines) >= 3:
                            data = self.data_template.copy()
                            data["Conference Name"] = "Gene Therapy Conference"
                            data["Topic"] = "Gene Therapy"
                            data["Speaker Full Name"] = lines[0].strip()
                            data["Speaker First Name"] = lines[0].strip().split(" ")[0]
                            data["Speaker Job Title"] = lines[1].strip()
                            data["Speaker Company"] = lines[2].strip()
                            data["Speaker Profile"] = href
                            results.append(data)
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
