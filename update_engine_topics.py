with open('core/engine.py', 'r') as f:
    content = f.read()

import re
# We need to replace:
# 'https://www.bioprocessingsummit.com/22/cell-culture': (CHISpider, 'Annual Bioprocessing Summit Boston 2022', 'Annual Bioprocessing  Boston 2022', 'https://www.bioprocessingsummit.com/22/cell-culture'),
# with the correct topic extracted from the slug.

lines = content.split('\n')
new_lines = []
for line in lines:
    if "'Annual Bioprocessing  Boston 2022'" in line and 'bioprocessingsummit.com' in line:
        # extract slug
        match = re.search(r"'(https://www\.bioprocessingsummit\.com/22/([^']+))'", line)
        if match:
            url = match.group(1)
            slug = match.group(2)
            topic = slug.replace('-', ' ').title()
            # replace 'Annual Bioprocessing  Boston 2022' with topic
            line = line.replace("'Annual Bioprocessing  Boston 2022'", f"'{topic}'")
    new_lines.append(line)

with open('core/engine.py', 'w') as f:
    f.write('\n'.join(new_lines))

print("Updated core/engine.py CHI topics.")
