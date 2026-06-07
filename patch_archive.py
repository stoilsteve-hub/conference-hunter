import os

spider = "spiders/archive_spider.py"

with open(spider, 'r') as f:
    content = f.read()
    
if "from core.ai_extractor import extract_speaker_info" not in content:
    content = content.replace("from spiders.base_spider import BaseSpider", "from spiders.base_spider import BaseSpider\nfrom core.ai_extractor import extract_speaker_info")
    
if "extract_speaker_info" in content and "ai_data =" not in content:
    
    old_block = """                        bio_loc = page.locator(".speaker-bio, .biography, .content p").all()
                        if not bio_loc:
                            bio_loc = page.locator("p").all()
                            
                        bio_text = "\\n\\n".join([p.inner_text().strip() for p in bio_loc if len(p.inner_text().strip()) > 50])
                        data["Speaker Summary"] = bio_text"""
        
    new_block = """                        raw_text = page.locator("body").inner_text()
                        ai_data = extract_speaker_info(raw_text)
                        
                        if ai_data["name"]: data["Speaker Full Name"] = ai_data["name"]
                        if ai_data["job_title"]: data["Speaker Job Title"] = ai_data["job_title"]
                        if ai_data["company"]: data["Speaker Company"] = ai_data["company"]
                        if ai_data["summary"]: data["Speaker Summary"] = ai_data["summary"]"""
        
    content = content.replace(old_block, new_block)

with open(spider, 'w') as f:
    f.write(content)

print("Archive spider patched!")
