from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright

class ImmunoOncologySpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping Immuno-Oncology Europe at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                target_url = self.url.rstrip("/") + "/speaker-biographies"
                page.goto(target_url, timeout=60000)
                
                # The names are inside strong tags. 
                strongs = page.locator("p > strong, div > strong").all()
                seen_names = set()
                
                for s in strongs:
                    name = s.inner_text().strip()
                    # Filter out garbage
                    if name in ["Cookie Policy", "Warning!", "Filter by:", ""] or len(name.split()) < 2:
                        continue
                    
                    if name in seen_names:
                        continue # avoid duplicates
                    seen_names.add(name)
                    
                    # Try to get the parent paragraph for context (title/company)
                    parent_text = s.evaluate("node => node.parentNode.innerText")
                    lines = [line.strip() for line in parent_text.split("\n") if line.strip()]
                    
                    data = self.data_template.copy()
                    data["Conference Name"] = "Immuno-Oncology Europe"
                    data["Topic"] = "Immuno-Oncology"
                    data["Speaker Full Name"] = name
                    data["Speaker First Name"] = name.split(" ")[0]
                    
                    if len(lines) > 1:
                        title_company = lines[1]
                        if "," in title_company:
                            parts = title_company.split(",", 1)
                            data["Speaker Job Title"] = parts[0].strip()
                            data["Speaker Company"] = parts[1].strip()
                        else:
                            data["Speaker Job Title"] = title_company

                    # Extract bio text
                    data["Speaker Summary"] = "\n".join(lines[2:]) if len(lines) > 2 else ""
                    
                    # Extract image
                    parent_element = s.evaluate_handle("node => node.parentNode.parentNode")
                    if parent_element:
                        img_handle = parent_element.query_selector("img")
                        if img_handle:
                            src = img_handle.get_attribute("src")
                            if src:
                                # handle relative paths
                                if src.startswith("/"):
                                    src = "https://www.immuno-oncologyeurope.com" + src
                                data["Speaker Image URL"] = src
                                data["Speaker Image Local Path"] = self.download_image(src, name)
                    
                    results.append(data)
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
