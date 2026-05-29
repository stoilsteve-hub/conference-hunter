import hashlib
from core.exporter import Exporter
from spiders.immuno_oncology import ImmunoOncologySpider
from spiders.peptide_summit import PeptideSummitSpider
from spiders.cdx_europe import CDXEuropeSpider
from spiders.lnp_formulation import LNPFormulationSpider
from spiders.gene_therapy import GeneTherapySpider

class Engine:
    def __init__(self):
        self.exporter = Exporter()
        self.urls = []
        self.spider_map = {
            "immuno-oncologyeurope.com": ImmunoOncologySpider,
            "peptide-based-therapeutics-summit.com": PeptideSummitSpider,
            "cdx-europe.com": CDXEuropeSpider,
            "lnp-formulation-process-development-pharma.com": LNPFormulationSpider,
            "genetherapy-conference.com": GeneTherapySpider
        }

    def load_urls(self, url_list):
        self.urls = url_list
        print(f"Loaded {len(self.urls)} urls to scrape.")

    def run(self):
        print("Engine starting... gonna loop through urls now")
        all_scraped_data = []
        for url in self.urls:
            print(f"Preparing to scrape {url}...")
            spider_class = None
            for domain, spider in self.spider_map.items():
                if domain in url:
                    spider_class = spider
                    break
            
            if spider_class:
                conf_id = "CONF-" + hashlib.md5(url.encode()).hexdigest()[:6].upper()
                scraper = spider_class(conference_id=conf_id, conference_name="auto", url=url)
                data = scraper.extract()
                all_scraped_data.extend(data)
            else:
                print(f"No specific spider found for {url}, skipping!")
        
        if all_scraped_data:
            self.exporter.save_data(all_scraped_data)
        print("Engine finished running!")
