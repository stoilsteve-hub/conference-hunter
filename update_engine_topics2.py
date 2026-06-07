with open('core/engine.py', 'r') as f:
    content = f.read()

import re

lines = content.split('\n')
new_lines = []
for line in lines:
    if 'Annual Bioprocessing  Boston 2022' in line and 'bioprocessingsummit.com/22/' in line:
        
        match = re.search(r"bioprocessingsummit\.com/22/([a-zA-Z0-9\-]+)", line)
        if match:
            slug = match.group(1)
            topic = slug.replace('-', ' ').title()
            line = line.replace("'Annual Bioprocessing  Boston 2022'", f"'{topic}'")
            line = line.replace('"Annual Bioprocessing  Boston 2022"', f"'{topic}'")
    new_lines.append(line)

with open('core/engine.py', 'w') as f:
    f.write('\n'.join(new_lines))

print("Updated core/engine.py CHI topics again.")
