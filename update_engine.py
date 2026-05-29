import sys
sys.path.append('.')
from core.engine import Engine
e = Engine()
existing_map = e.spider_map

with open('parse_screens.py') as f:
    code = f.read()

import re
import urllib.parse
text = code.split('text = """')[1].split('"""')[0]

for line in text.strip().split("\n"):
    parts = line.split("->")
    if len(parts) >= 3:
        name_part = parts[0].strip()
        topic = parts[1].strip()
        url = parts[2].strip()
        name = re.sub(r'^\d+\s+', '', name_part)
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.replace("www.", "")
        if domain not in existing_map:
            existing_map[domain] = ('HansonWadeSpider', name, topic, "")

lines = [
    "import hashlib",
    "from core.exporter import Exporter",
    "from spiders.immuno_oncology import ImmunoOncologySpider",
    "from spiders.hanson_wade_spider import HansonWadeSpider",
    "",
    "class Engine:",
    "    def __init__(self):",
    "        self.exporter = Exporter()",
    "        self.urls = []",
    "        self.spider_map = {"
]

for d, v in existing_map.items():
    s_class = "ImmunoOncologySpider" if v[0] == "ImmunoOncologySpider" or d == "immuno-oncologyeurope.com" else "HansonWadeSpider"
    name = v[1]
    topic = v[2]
    s_url = v[3]
    lines.append(f'            "{d}": ({s_class}, "{name}", "{topic}", "{s_url}"),')

lines.append("        }")
lines.extend([
    "",
    "    def load_urls(self, url_list):",
    "        self.urls = url_list",
    "        print(f\"Loaded {len(self.urls)} urls to scrape.\")",
    "",
    "    def run(self):",
    "        print(\"Engine starting... gonna loop through urls now\")",
    "        all_scraped_data = []",
    "        for url in self.urls:",
    "            print(f\"Preparing to scrape {url}...\")",
    "            spider_tuple = None",
    "            for domain, spider_tup in self.spider_map.items():",
    "                if domain in url:",
    "                    spider_tuple = spider_tup",
    "                    break",
    "            ",
    "            if spider_tuple:",
    "                spider_class, conf_name, topic, speaker_url = spider_tuple",
    "                conf_id = \"CONF-\" + hashlib.md5(url.encode()).hexdigest()[:6].upper()",
    "                scraper = spider_class(conference_id=conf_id, conference_name=conf_name, topic=topic, url=url, speaker_url=speaker_url)",
    "                data = scraper.extract()",
    "                all_scraped_data.extend(data)",
    "            else:",
    "                print(f\"No specific spider found for {url}, skipping!\")"
])

with open('core/engine.py', 'w') as f:
    f.write("\n".join(lines) + "\n")
