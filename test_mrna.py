from spiders.hanson_wade_spider import HansonWadeSpider
spider = HansonWadeSpider("CONF-2", "mRNA Process Manufacturing", "mrna-processmanufacturing.com", "mRNA", "")
data = spider.extract()
print(f"Extracted {len(data)}")
