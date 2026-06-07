from spiders.hanson_wade_spider import HansonWadeSpider
spider = HansonWadeSpider("CONF-1", "iPSC Drug Development", "ipsc-therapies-summit.com", "Cell Therapy", "https://ipsc-therapies-summit.com/speakers/")
data = spider.extract()
print(f"Extracted {len(data)}")
