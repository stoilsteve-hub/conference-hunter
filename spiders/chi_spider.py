from playwright.sync_api import sync_playwright
import re
from spiders.base_spider import BaseSpider

class CHISpider(BaseSpider):
    def extract(self):
        print(f"Extracting CHI format from {self.url}...")
        extracted_data = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(self.url, timeout=60000, wait_until="networkidle")

                # The URL passed for CHI is usually the correct agenda/speakers page.
                target_url = self.url
                try:
                    # In case it redirected or didn't fully load, ensure we are at self.url
                    page.goto(target_url, timeout=60000, wait_until="networkidle")
                except:
                    pass
                
                # Extract text containing PhD, MD, etc.
                lines = page.locator("body").inner_text().split("\n")
                speaker_blocks = []
                for line in lines:
                    if "PhD" in line or "MD" in line or "M.D." in line or "Ph.D" in line:
                        speaker_blocks.append(line.strip())

                for block in speaker_blocks:
                    block = block.strip()
                    if len(block) < 5 or len(block) > 200: continue
                    if "PhD" in block or "MD" in block or "," in block:
                        parts = [p.strip() for p in block.split(",", 2)]
                        name = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        company = parts[2] if len(parts) > 2 else ""
                        email = "info@" + re.sub(r'[^a-zA-Z0-9]', '', company.lower()) + ".com" if company else ""
                        
                        data = {
                            "Conference ID": self.conference_id,
                            "Conference Name": self.conference_name,
                            "Topic": self.topic,
                            "Dates": "TBD",
                            "Location": "TBD",
                            "Speaker First Name": name.split()[0] if name else "",
                            "Speaker Full Name": name,
                            "Speaker Job Title": title,
                            "Speaker Company": company,
                            "Presentation Title": "",
                            "Speaker Summary": "",
                            "Speaker Profile": "",
                            "Speaker Image URL": ""
                        }
                        extracted_data.append(data)
                        
                browser.close()
        except Exception as e:
            print(f"Error scraping {self.url}: {e}")
            
        return extracted_data
