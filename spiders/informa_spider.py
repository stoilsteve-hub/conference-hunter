from playwright.sync_api import sync_playwright
import re
from spiders.base_spider import BaseSpider

class InformaSpider(BaseSpider):
    def extract(self):
        print(f"Extracting InformaConnect format from {self.url}...")
        extracted_data = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(self.url, timeout=90000, wait_until="networkidle")

                # Extract text containing PhD, MD, etc.
                content = page.content()
                
                # InformaConnect uses dynamic JSON or generic speaker blocks
                speaker_blocks = page.locator("h3, h4, .speaker, .name").all_text_contents()
                
                if not speaker_blocks:
                    # fallback
                    lines = page.locator("body").inner_text().split("\n")
                    speaker_blocks = []
                    for line in lines:
                        if "PhD" in line or "MD" in line or "M.D." in line or "Ph.D" in line:
                            speaker_blocks.append(line.strip())

                for block in speaker_blocks:
                    block = block.strip()
                    if len(block) < 5 or len(block) > 150: continue
                    # Generic parsing
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
