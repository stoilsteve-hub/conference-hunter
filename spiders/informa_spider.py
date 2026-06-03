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

                seen_texts = set()
                
                # Check if there are stream filters we can click through
                labels = page.locator(".c-filter-group ul li label, .filter-sidebar label, .stream-filters label, .c-filter-checkbox").all()
                
                # Filter out labels that are empty or garbage
                valid_labels = []
                for l in labels:
                    txt = l.inner_text().strip()
                    if txt and len(txt) > 3 and "Show all" not in txt:
                        valid_labels.append((l, txt))
                        
                if valid_labels:
                    print(f"Found {len(valid_labels)} streams to iterate...")
                    for label, topic_name in valid_labels:
                        try:
                            label.click(timeout=2000)
                            page.wait_for_timeout(2000)
                            
                            # Ensure all speakers load
                            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            page.wait_for_timeout(1000)
                            
                            self._extract_speakers(page, topic_name, seen_texts, extracted_data)
                            
                            # Untoggle
                            label.click(timeout=2000)
                            page.wait_for_timeout(1000)
                        except:
                            pass
                else:
                    # No filters, just extract everything with the default topic
                    self._extract_speakers(page, self.topic, seen_texts, extracted_data)

                browser.close()
        except Exception as e:
            print(f"Error scraping {self.url}: {e}")
            
        return extracted_data

    def _extract_speakers(self, page, current_topic, seen_texts, extracted_data):
        speaker_locators = page.locator(".speaker, .speaker-item, .person, .speaker-block, [class*='speaker-block']").all()
        
        if not speaker_locators:
            speaker_locators = page.locator("tr, div.row, li").all()

        for loc in speaker_locators:
            try:
                speaker_info = loc.evaluate('''el => {
                    // Exclude Wayback header, navs, and footers
                    if (el.closest('#wm-ipp-base, header, footer, nav, .nav, .menu, .footer')) return null;
                
                    let container = el.closest('.speaker, .speaker-item, .person, [class*="speaker-block"], tr, li');
                    if (!container) container = el;
                    
                    // Prevent bleeding into hotel strings if it's too big
                    let img = container.querySelector('img');
                    let textNodes = [];
                    
                    let walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null, false);
                    let node;
                    while (node = walker.nextNode()) {
                        let txt = node.nodeValue.trim();
                        // Exclude agenda buttons or hotel texts
                        if (txt.length > 0 && !txt.includes('AgendaSponsor/Exhibit') && !txt.includes('Omni Boston') && !txt.includes('OVERVIEW | DOWNLOAD')) {
                            textNodes.push(txt);
                        }
                    }
                    
                    let text = textNodes.join('\\n');
                    if (!text || text.trim().length === 0) return null;
                    
                    // Exclude bad keywords
                    let bad_words = ['About', 'Attend', 'Learn', 'Speak', 'Internet', 'Archive-It', 'Images'];
                    for (let bw of bad_words) {
                        if (text.startsWith(bw + "\\n") || text === bw) return null;
                    }
                    
                    return {
                        text: text,
                        img: img ? (img.getAttribute('data-src') || img.src) : ""
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
                        
                dept_keywords = ['development', 'research', 'chemistry', 'operations', 'lab', 'strategy', 'manufacturing', 'controls', 'platform', 'immunology', 'discovery', 'sciences', 'biology', 'engineering', 'analytics', 'regulatory', 'access', 'value', 'project', 'team', 'biochemistry', 'oncology', 'medical affairs', 'clinical', 'data', 'bioinformatics', 'computational', 'formulation', 'delivery', 'cmc', 'quality', 'assurance', 'qc', 'qa', 'market', 'commercial', 'sales', 'marketing', 'business', 'alliance', 'search', 'evaluation', 'innovation', 'technology']
                company_keywords_ext = company_indicators + ['biotech', 'solutions', 'health', 'care', 'sanofi', 'pfizer', 'novartis', 'merck', 'janssen', 'astrazeneca', 'roche', 'abbvie', 'bayer', 'lilly', 'gsk', 'amgen', 'gilead', 'biogen', 'regeneron', 'vertex', 'moderna', 'biontech', 'takeda', 'daiichi', 'astellas', 'eisai', 'otsuka', 'sun', 'reddy', 'cipla', 'aurobindo', 'lupin', 'zydus', 'intas', 'torrent', 'biocon', 'glenmark', 'macleods', 'mankind', 'alchem', 'usv', 'wockhardt', 'group', 'partner', 'consulting', 'association', 'society', 'council', 'network', 'fund', 'foundation', 'ventures', 'capital', 'holdings', 'partners']
                
                if company.strip() != '':
                    c_lower = company.lower()
                    if not any(k in c_lower for k in company_keywords_ext):
                        if any(dk in c_lower for dk in dept_keywords) and 'national research council' not in c_lower:
                            title = title + ", " + company if title else company
                            company = ""
                
                summary = "\n".join(lines[1:]) if len(lines) > 1 else ""
                
                if summary.lower().startswith('job title:'):
                    summary = summary[10:].strip()
                if 'wayback machine' in summary.lower() or 'fight for the future' in summary.lower():
                    summary = ''
                    
                if len(name) > 60 or "Archived Content" in name or any(char.isdigit() for char in name): continue
                if "speaker" in name.lower() or "expand_more" in title.lower() or "@" in title or "bpicustomerservice" in title.lower(): continue
                if not title and not company and not img: continue
                
                data = {
                    "Conference ID": self.conference_id,
                    "Conference Name": self.conference_name,
                    "Topic": current_topic,
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
