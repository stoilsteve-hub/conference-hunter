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

                # Informa uses stream filters on the left. Click them to load speakers.
                try:
                    stream_filters = page.locator(".filter-sidebar input[type=checkbox], .stream-filters input[type=checkbox]").all()
                    for cb in stream_filters:
                        try:
                            cb.click(timeout=2000)
                            page.wait_for_timeout(1000)
                        except:
                            pass
                except:
                    pass
                    
                # Ensure all speakers are visible by scrolling or waiting
                page.wait_for_timeout(2000)
                
                seen_texts = set()
                
                # Extract speaker blocks
                # Find all elements that look like speaker cards
                speaker_locators = page.locator(".speaker, .speaker-item, .person, .speaker-block").all()
                
                if not speaker_locators:
                    # Fallback to general structures
                    speaker_locators = page.locator("tr, div.row, li").all()

                for loc in speaker_locators:
                    try:
                        speaker_info = loc.evaluate('''el => {
                            let container = el.closest('.speaker, .speaker-item, .person, tr, li');
                            if (!container) container = el; // If it's already a speaker block
                            
                            let img = container.querySelector('img');
                            let textNodes = [];
                            
                            // Get all meaningful text inside
                            let walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null, false);
                            let node;
                            while (node = walker.nextNode()) {
                                if (node.nodeValue.trim().length > 0) {
                                    textNodes.push(node.nodeValue.trim());
                                }
                            }
                            
                            let text = textNodes.join('\\n');
                            if (!text || text.trim().length === 0) return null;
                            
                            return {
                                text: text,
                                img: img ? img.src : ""
                            }
                        }''')
                        
                        if not speaker_info or not speaker_info['text']: continue
                        
                        text = speaker_info['text'].strip()
                        img = speaker_info['img']
                        
                        if len(text) < 15 or len(text) > 800: continue
                        if text in seen_texts: continue
                        seen_texts.add(text)
                        
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        if len(lines) < 2 and not img: continue
                        
                        first_line = lines[0]
                        if "," not in first_line and len(lines) > 1:
                            first_line = lines[0] + ", " + lines[1]
                            lines.pop(1)
                                
                        parts = [p.strip() for p in first_line.split(",", 2)]
                        name = parts[0]
                        title = parts[1] if len(parts) > 1 else ""
                        company = parts[2] if len(parts) > 2 else ""
                        
                        summary = "\n".join(lines[1:]) if len(lines) > 1 else ""
                        
                        if len(name) > 60: continue
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
