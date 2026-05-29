from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright

class PeptideSummitSpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping Peptide Summit at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.url, timeout=60000)
                
                # Get links
                links = page.locator("a").all()
                speaker_links = []
                for link in links:
                    href = str(link.get_attribute("href"))
                    text = link.inner_text().strip()
                    if "/speaker/" in href and "\n" in text:
                        lines = text.split("\n")
                        if len(lines) >= 3:
                            speaker_links.append({
                                "url": href,
                                "name": lines[0].strip(),
                                "title": lines[1].strip(),
                                "company": lines[2].strip()
                            })
                
                # deduplicate
                unique_speakers = {s["name"]: s for s in speaker_links}.values()
                
                for s in list(unique_speakers)[:10]: # Limit to 10 for speed during testing
                    print(f"Deep scraping: {s['name']}")
                    data = self.data_template.copy()
                    data["Conference Name"] = "Peptide Summit"
                    data["Topic"] = "Peptides"
                    data["Speaker Full Name"] = s["name"]
                    data["Speaker First Name"] = s["name"].split(" ")[0]
                    data["Speaker Job Title"] = s["title"]
                    data["Speaker Company"] = s["company"]
                    data["Speaker Profile"] = s["url"]
                    
                    try:
                        page.goto(s["url"], timeout=30000)
                        
                        # Extract bio
                        paragraphs = page.locator(".hw-speaker-content p").all()
                        if not paragraphs:
                            paragraphs = page.locator("p").all()
                        
                        bio_text = []
                        garbage_phrases = [
                            "cookies", "privacy", "thank you to our speakers", 
                            "ambitious people", "hanson wade", "this website uses", 
                            "by clicking", "opt out"
                        ]
                        for p_elem in paragraphs:
                            pt = p_elem.inner_text().strip()
                            if len(pt) > 50 and not any(phrase in pt.lower() for phrase in garbage_phrases):
                                bio_text.append(pt)
                        data["Speaker Summary"] = "\n\n".join(bio_text)
                        
                        # Extract email
                        import re
                        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                        emails = re.findall(email_pattern, data["Speaker Summary"])
                        if emails:
                            data["Speaker Email"] = emails[0]
                        else:
                            # Try searching all hrefs for mailto
                            for a_tag in page.locator("a").all():
                                href = a_tag.get_attribute("href")
                                if href and href.startswith("mailto:"):
                                    data["Speaker Email"] = href.replace("mailto:", "").strip()
                                    break
                        
                        # Extract image
                        imgs = page.locator("img").all()
                        for img in imgs:
                            src = img.get_attribute("src")
                            if src and ("uploads" in src and "logo" not in src.lower() and "hw-group" not in src.lower()):
                                data["Speaker Image URL"] = src
                                break
                    except Exception as e:
                        print(f"Failed to deep scrape {s['url']}: {e}")
                        
                    results.append(data)
                    
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
