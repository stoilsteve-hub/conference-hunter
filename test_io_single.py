import json
from spiders.immuno_oncology import ImmunoOncologySpider
spider = ImmunoOncologySpider("https://www.immuno-oncologyeurope.com/")
res = spider.extract()
for i, r in enumerate(res[:3]):
    print(json.dumps(r, indent=2))
