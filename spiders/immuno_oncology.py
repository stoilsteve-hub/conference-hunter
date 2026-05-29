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
                # Visit homepage first to get the date and location
                page.goto(self.url, timeout=60000, wait_until="networkidle")
                conf_date = "TBD"
                conf_loc = "TBD"
                title = page.title()
                if "|" in title:
                    date_loc = title.split("|")[-1].strip()
                    if " in " in date_loc:
                        conf_date, conf_loc = date_loc.split(" in ", 1)
                    else:
                        conf_date = date_loc
                
                # Now go to speakers page
                target_url = self.url.rstrip("/") + "/speaker-biographies"
                page.goto(target_url, timeout=60000, wait_until="networkidle")
                
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
                    data["Dates"] = conf_date.strip()
                    data["Location"] = conf_loc.strip()
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
                    
                    # Email Validation Helper
                    def is_valid_email(em, name, company):
                        em = em.lower()
                        if any(g in em for g in ["info@", "contact@", "enquiries@", "admin@", "sales@", "hansonwade", "cambridgeinnovationinstitute"]):
                            return False
                        prefix, domain = em.split("@", 1)
                        name_parts = [p.lower() for p in name.split() if len(p) > 2]
                        comp_parts = [w.lower() for w in company.split() if len(w) > 2 and w.lower() not in ["inc", "llc", "ltd", "corp"]]
                        
                        if any(np in prefix for np in name_parts): return True
                        if any(cp in domain for cp in comp_parts): return True
                        return False

                    # Extract email
                    import re
                    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                    potential_emails = []
                    potential_emails.extend(re.findall(email_pattern, data["Speaker Summary"]))
                    parent_element = s.evaluate_handle("node => node.parentNode.parentNode")
                    if parent_element:
                        for a_tag in parent_element.query_selector_all("a"):
                            href = a_tag.get_attribute("href")
                            if href and href.startswith("mailto:"):
                                potential_emails.append(href.replace("mailto:", "").split("?")[0].strip())
                                
                    for em in potential_emails:
                        if is_valid_email(em, data["Speaker Full Name"], data.get("Speaker Company", "")):
                            data["Speaker Email"] = em
                            break
                    
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
                    
                    results.append(data)
            except Exception as e:
                print(f"Error on {self.url}: {e}")
            finally:
                browser.close()
        return results
