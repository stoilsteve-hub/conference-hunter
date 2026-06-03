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

                # Find and click any Day tabs to load all speakers
                day_tabs = page.locator("a", has_text=re.compile(r"Day \d+", re.IGNORECASE)).all()
                if not day_tabs:
                    day_tabs = [None] # Just run once if no tabs

                seen_texts = set()

                for tab in day_tabs:
                    if tab:
                        try:
                            tab.click(timeout=3000)
                            page.wait_for_timeout(1500) # wait for render
                        except:
                            pass
                            
                    # Find any element that could be a speaker container
                    locators = page.locator(".speaker, .speaker-item, [class*='speaker'], [class*='Speaker'], tr, div.row, li.nav-item").all()
                    
                    for loc in locators:
                        try:
                            speaker_info = loc.evaluate('''el => {
                                let img = el.querySelector('img');
                                let text = el.innerText;
                                if (!text || text.trim().length === 0) return null;
                                return {
                                    text: text.trim(),
                                    img: img ? img.src : ""
                                }
                            }''')
                            
                            if not speaker_info or not speaker_info['text']: continue
                            
                            text = speaker_info['text'].strip()
                            img = speaker_info['img']
                            
                            if text in seen_texts: continue
                            if len(text) < 15 or len(text) > 800: continue
                            if text in seen_texts: continue
                            seen_texts.add(text)
                            
                            lines = [l.strip() for l in text.split('\n') if l.strip()]
                            if len(lines) < 2 and not img: continue # skip garbage lines
                            
                            first_line = lines[0]
                            # If first line doesn't have a comma, it's probably just the name
                            if "," not in first_line and len(lines) > 1:
                                first_line = lines[0] + ", " + lines[1]
                                lines.pop(1)
                                    
                            parts = [p.strip() for p in first_line.split(",", 2)]
                            name = parts[0]
                            title = parts[1] if len(parts) > 1 else ""
                            company = parts[2] if len(parts) > 2 else ""
                            
                            summary = "\n".join(lines[1:]) if len(lines) > 1 else ""
                            
                            # Sanity check: name shouldn't be too long
                            if len(name) > 60: continue
                            
                            # Must have at least a title or company, or an image to be considered a speaker
                            if not title and not company and not img: continue
                            
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
                                "Speaker Summary": summary,
                                "Speaker Profile": summary,
                                "Speaker Image URL": img
                            }
                            extracted_data.append(data)
                        except Exception as e:
                            pass

                browser.close()
        except Exception as e:
            print(f"Error scraping {self.url}: {e}")
            
        return extracted_data
