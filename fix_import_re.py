import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    if 'import re\n' not in content[:500]:
        content = 'import re\n' + content
    with open(filepath, 'w') as f:
        f.write(content)

fix_file('spiders/chi_spider.py')
fix_file('spiders/informa_spider.py')
fix_file('spiders/hanson_wade_spider.py')
print("Added import re to tops of files.")
