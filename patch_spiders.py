import os

spiders = ["spiders/chi_spider.py", "spiders/informa_spider.py"]

for spider in spiders:
    with open(spider, 'r') as f:
        content = f.read()
        
    if "from core.ai_extractor import extract_speaker_info" not in content:
        content = content.replace("from playwright.sync_api import sync_playwright", "from playwright.sync_api import sync_playwright\nfrom core.ai_extractor import extract_speaker_info")
        
    if "extract_speaker_info" in content and "ai_data =" not in content:
        
        if "chi_spider" in spider:
            old_block = """                        live_url = re.sub(r'^https?://web\.archive\.org/web/\d+/', '', s["url"])
                        page.goto(live_url, timeout=5000, wait_until="domcontentloaded")
                        
                        # Extract presentation topic
                        topic_loc = page.locator(".presentation-title, .session-title, h3").first
                        if topic_loc.count() > 0:
                            data["Presentation Title"] = topic_loc.inner_text().strip()
                        
                        # Extract bio
                        bio_loc = page.locator(".speaker-bio, .biography, .content p").all()
                        if bio_loc:
                            bio_text = "\\n\\n".join([p.inner_text().strip() for p in bio_loc if len(p.inner_text().strip()) > 50])
                            data["Speaker Summary"] = bio_text"""
            
            new_block = """                        page.goto(s["url"], timeout=15000, wait_until="domcontentloaded")
                        
                        raw_text = page.locator("body").inner_text()
                        ai_data = extract_speaker_info(raw_text)
                        
                        if ai_data["name"]: data["Speaker Full Name"] = ai_data["name"]
                        if ai_data["job_title"]: data["Speaker Job Title"] = ai_data["job_title"]
                        if ai_data["company"]: data["Speaker Company"] = ai_data["company"]
                        if ai_data["summary"]: data["Speaker Summary"] = ai_data["summary"]"""
            
            content = content.replace(old_block, new_block)
            
        
        if "informa_spider" in spider:
            old_block = """                        live_url = re.sub(r'^https?://web\.archive\.org/web/\d+/', '', s["url"])
                        page.goto(live_url, timeout=5000, wait_until="domcontentloaded")
                        
                        # Extract presentation topic
                        text = page.locator("body").inner_text()
                        if "Session:" in text:
                            parts = text.split("Session:")[1].strip().split("\\n")
                            if len(parts) > 0:
                                data["Presentation Title"] = parts[0].strip()
                        
                        # Extract bio
                        bio_loc = page.locator(".speaker-bio, .biography, .content p").all()
                        if not bio_loc:
                            bio_loc = page.locator("p").all()
                            
                        bio_text = "\\n\\n".join([p.inner_text().strip() for p in bio_loc if len(p.inner_text().strip()) > 50])
                        data["Speaker Summary"] = bio_text"""
            
            new_block = """                        page.goto(s["url"], timeout=15000, wait_until="domcontentloaded")
                        
                        raw_text = page.locator("body").inner_text()
                        ai_data = extract_speaker_info(raw_text)
                        
                        if ai_data["name"]: data["Speaker Full Name"] = ai_data["name"]
                        if ai_data["job_title"]: data["Speaker Job Title"] = ai_data["job_title"]
                        if ai_data["company"]: data["Speaker Company"] = ai_data["company"]
                        if ai_data["summary"]: data["Speaker Summary"] = ai_data["summary"]"""
            
            content = content.replace(old_block, new_block)

    with open(spider, 'w') as f:
        f.write(content)

print("Spiders patched!")
