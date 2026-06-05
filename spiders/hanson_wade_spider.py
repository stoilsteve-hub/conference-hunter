import re
from spiders.base_spider import BaseSpider
from playwright.sync_api import sync_playwright
from core.ai_extractor import extract_speaker_info
class HansonWadeSpider(BaseSpider):
    def extract(self):
        results = []
        print(f"Scraping {self.conference_name} at {self.url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            try:
                if not self.speaker_url:
                    target_url = self.url if self.url.startswith("http") else f"https://{self.url}"
                else:
                    target_url = self.speaker_url
                page.goto(target_url, timeout=60000, wait_until="domcontentloaded")
                
                # Extract Date and Location
                conf_date = "TBD"
                conf_loc = "TBD"
                months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
                for line in page.locator("body").inner_text().split("\n")[:100]:
                    if "|" in line and any(m in line.lower() for m in months):
                        parts = line.split("|", 1)
                        conf_date = parts[0].replace("Returning", "").replace("Ran", "").strip()
                        conf_loc = parts[1].strip()
                        break
                
                if conf_date == "TBD":
                    for line in page.locator("body").inner_text().split("\n")[:100]:
                        if "Returning 20" in line:
                            conf_date = line.strip()
                            break
                
                # Now go to speakers page
                speakers_url = self.speaker_url
                if not speakers_url:
                    # Dynamically discover speaker link from homepage
                    page.goto(self.url, timeout=60000, wait_until="networkidle")
                    links = page.locator("a").all()
                    for a in links:
                        try:
                            text = a.inner_text().strip().lower()
                            href = a.get_attribute("href")
                            if "speaker" in text and href and href != "#" and "mailto:" not in href:
                                if href.startswith("/"):
                                    speakers_url = self.url.rstrip("/") + href
                                else:
                                    speakers_url = href
                                if "/speaker" in speakers_url.lower():
                                    break
                        except Exception:
                            pass
                    
                    if not speakers_url:
                        speakers_url = self.url.rstrip("/") + "/speakers/"
                
                try:
                    response = page.goto(speakers_url, timeout=60000, wait_until="networkidle")
                    if response and response.status == 404:
                        # Fallback to homepage if /speakers/ is missing
                        page.goto(self.url, timeout=60000, wait_until="networkidle")
                except Exception:
                    pass
                
                # Scroll to bottom to trigger any lazy loading
                previous_height = page.evaluate("document.body.scrollHeight")
                while True:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1500)
                    
                    # Try to click any 'Load More' or 'View More' buttons
                    try:
                        more_btns = page.locator("button, a.button, .btn, .elementor-button").all()
                        clicked_any = False
                        for btn in more_btns:
                            text = btn.inner_text().lower()
                            if "more" in text or "load" in text:
                                btn.click(timeout=2000)
                                page.wait_for_timeout(1000)
                                clicked_any = True
                    except:
                        pass
                        
                    new_height = page.evaluate("document.body.scrollHeight")
                    if new_height == previous_height and not clicked_any:
                        break
                    previous_height = new_height
                
                # Get links
                links = page.locator("a").all()
                speaker_links = []
                for link in links:
                    href = str(link.get_attribute("href"))
                    text = link.inner_text().strip()
                    if "/speaker/" in href and len(text) > 0:
                        lines = [l.strip() for l in text.split("\n") if l.strip()]
                        if len(lines) >= 1:
                            first_line = lines[0]
                            if "," not in first_line and len(lines) > 1:
                                first_line = lines[0] + ", " + lines[1]
                                lines.pop(1)
                                    
                            parts = [p.strip() for p in first_line.split(",")]
                            name = parts[0]
                            
                            title = ""
                            company = ""
                            
                            if len(parts) > 1:
                                if parts[1].upper() in ['PHD', 'MD', 'PH.D.', 'M.D.', 'MSC', 'PHARMD', 'MBA', 'M.S.']:
                                    name += ", " + parts[1]
                                    if len(parts) > 2:
                                        title = ", ".join(parts[2:-1]) if len(parts) > 3 else parts[2]
                                        company = parts[-1] if len(parts) > 3 else (parts[3] if len(parts)>3 else "")
                                else:
                                    title = parts[1]
                                    company = ", ".join(parts[2:]) if len(parts) > 2 else ""
                                    
                            company_indicators = ['klinikum', 'universität', 'university', 'biochemie', 'kgaa', 'inc', 'llc', 'ltd', 'therapeutics', 'biosciences', 'pharma', 'institute', 'gmbh', 'ag', 'corp', 'hospital', 'college', 'clinic']
                            title_indicators = ['director', 'vp', 'head', 'scientist', 'manager', 'officer', 'chief', 'professor', 'ceo', 'cto', 'lead', 'founder', 'president']
                            if company.strip() == '':
                                if any(ci in title.lower() for ci in company_indicators) and not any(ti in title.lower() for ti in title_indicators):
                                    company = title
                                    title = ""
                                    
                            # Global PhD/MD scrubber
                            degree_pattern = r'(?i)\b(Ph\.?D\.?|M\.?D\.?|MSc|PharmD|MBA|M\.?S\.?)\b'
                            degrees_found = []
                            for field in [title, company]:
                                matches = re.findall(degree_pattern, field)
                                for match in matches:
                                    if match.upper().replace('.', '') not in [d.upper().replace('.', '') for d in degrees_found]:
                                        degrees_found.append(match)
                            
                            if degrees_found:
                                name += ", " + ", ".join(degrees_found)
                                title = re.sub(degree_pattern, '', title).strip(' ,')
                                company = re.sub(degree_pattern, '', company).strip(' ,')
                            
                            if len(name) < 60 and not any(char.isdigit() for char in name) and "speaker" not in name.lower() and "expand_more" not in title.lower() and "@" not in title:
                                speaker_links.append({
                                    "url": href,
                                    "name": name,
                                    "title": title,
                                    "company": company
                                })
                
                # deduplicate
                unique_speakers = {s["name"]: s for s in speaker_links}.values()
                
                for s in list(unique_speakers): # Removed test limit
                    print(f"Deep scraping: {s['name']}")
                    data = self.data_template.copy()
                    data["Conference Name"] = self.conference_name
                    data["Topic"] = self.topic
                    data["Dates"] = conf_date
                    data["Location"] = conf_loc
                    data["Speaker Full Name"] = s["name"]
                    data["Speaker First Name"] = s["name"].split(" ")[0]
                    data["Speaker Job Title"] = s["title"]
                    data["Speaker Company"] = s["company"]
                    data["Speaker Profile"] = s["url"]
                    
                    try:
                        # Use the original URL (even if it's a Wayback Machine archive) so we don't hit dead live domains!
                        page.goto(s["url"], timeout=15000, wait_until="domcontentloaded")
                        
                        # Grab the entire raw text of the page
                        raw_text = page.locator("body").inner_text()
                        
                        # SEND IT TO THE AI
                        ai_data = extract_speaker_info(raw_text)
                        
                        # Merge the AI's flawless extraction into the dataset
                        if ai_data["name"]: data["Speaker Full Name"] = ai_data["name"]
                        if ai_data["job_title"]: data["Speaker Job Title"] = ai_data["job_title"]
                        if ai_data["company"]: data["Speaker Company"] = ai_data["company"]
                        if ai_data["summary"]: data["Speaker Summary"] = ai_data["summary"]
                        
                        # Email Validation Helper
                        def is_valid_email(em, name, company):
                            em = em.lower()
                            if any(g in em for g in ["info@", "contact@", "enquiries@", "admin@", "sales@", "hansonwade"]):
                                return False
                            prefix, domain = em.split("@", 1)
                            name_parts = [p.lower() for p in name.split() if len(p) > 2]
                            comp_parts = [w.lower() for w in company.split() if len(w) > 2 and w.lower() not in ["inc", "llc", "ltd", "corp"]]
                            
                            if any(np in prefix for np in name_parts): return True
                            if any(cp in domain for cp in comp_parts): return True
                            return False

                        # Extract email
                        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                        potential_emails = []
                        potential_emails.extend(re.findall(email_pattern, data["Speaker Summary"]))
                        for a_tag in page.locator("a").all():
                            href = a_tag.get_attribute("href")
                            if href and href.startswith("mailto:"):
                                potential_emails.append(href.replace("mailto:", "").split("?")[0].strip())
                                
                        for em in potential_emails:
                            if is_valid_email(em, s["name"], s["company"]):
                                data["Speaker Email"] = em
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
