from core.engine import Engine
from spiders.informa_spider import InformaSpider
import sys

e = Engine()
informa_urls = [url for url, vals in e.spider_map.items() if vals[0] == InformaSpider]

print(f"Running Informa specific scrape for {len(informa_urls)} URLs...")
e.load_urls(informa_urls)
e.run()
