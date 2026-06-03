import re

with open('core/engine.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if '("CHISpider"' in line or '("InformaSpider"' in line or '(CHISpider' in line or '(InformaSpider' in line:
        if '"Both"' in line:
            # Extract the conference name to derive the topic
            # Line format: "url": (Spider, "Conf Name", "Both", "url"),
            match = re.search(r'\((.+?),\s*"([^"]+)",\s*"Both",', line)
            if match:
                spider, cname = match.groups()
                if ' - ' in cname:
                    topic = cname.split(' - ')[-1].strip()
                else:
                    topic = re.sub(r'^\d+(th|st|nd|rd)\s+(Annual\s+)?', '', cname)
                    topic = topic.replace('Conference & Expo', '').replace('Summit', '').strip()
                line = line.replace('"Both"', f'"{topic}"')
    new_lines.append(line)

with open('core/engine.py', 'w') as f:
    f.writelines(new_lines)
