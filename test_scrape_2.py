from spiders.hanson_wade_spider import HansonWadeSpider

spider = HansonWadeSpider("CONF-1234", "TCR-based therapies for solid tumors summit", "tcr-therapies-summit.com", "Cell Therapy", "https://tcr-therapies-summit.com/speakers/")
print("Extracting...")
data = spider.extract()
print(f"Extracted {len(data)} speakers")
