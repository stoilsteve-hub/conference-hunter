from spiders.hanson_wade_spider import HansonWadeSpider

spider = HansonWadeSpider("https://tcr-therapies-summit.com/speakers/", "TCR-based therapies for solid tumors summit", "Cell Therapy", "conf_id")
print("Extracting...")
data = spider.extract()
print(f"Extracted {len(data)} speakers")
