import re

log_path = "/Users/stoil.steve/.gemini/antigravity-ide/brain/6caca1fa-8240-465e-8db9-6f6d8236862c/.system_generated/tasks/task-2123.log"
with open(log_path, 'r') as f:
    log_content = f.read()


domains = re.findall(r"Scraping .* at (https?://[^\n]+)", log_content)

bad_domains = set()
lines = log_content.split('\n')
current_domain = None

for line in lines:
    domain_match = re.search(r"Scraping .* at (https?://[^\n]+)", line)
    if domain_match:
        current_domain = domain_match.group(1)
        
    if "AI Extraction failed: 503" in line and current_domain:
        bad_domains.add(current_domain)

print("Domains that suffered 503 errors:")
for d in bad_domains:
    print(d)
