from spiders.archive_spider import ArchiveSpider
spider = ArchiveSpider("CONF-2", "mRNA Process Manufacturing", "mrna-processmanufacturing.com", "mRNA", "")
data = spider.extract()
print(f"Extracted {len(data)}")
