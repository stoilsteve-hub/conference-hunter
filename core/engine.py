import hashlib
from core.exporter import Exporter
from spiders.immuno_oncology import ImmunoOncologySpider
from spiders.hanson_wade_spider import HansonWadeSpider

class Engine:
    def __init__(self):
        self.exporter = Exporter()
        self.urls = []
        self.spider_map = {
            # Screenshot 1
            "tcr-therapies-summit.com": (HansonWadeSpider, "TCR-based therapies for solid tumors summit", "Cell Therapy", "https://tcr-therapies-summit.com/speakers/"),
            "mrna-processmanufacturing.com": (HansonWadeSpider, "2nd mRNA Process Development & Manufacturing Summit", "mRNA", "https://mrna-processmanufacturing.com/whats-on/speakers/"),
            "cell-therapy-analytics-europe.com": (HansonWadeSpider, "2nd Cell Therapy Analytical Development Summit Europe", "Cell Therapy", "https://cell-therapy-analytics-europe.com/whats-on/speakers/"),
            "genetherapy-ophthalmology.com": (HansonWadeSpider, "Gene Therapy for Ophthalmic Disorders", "Gene Therapy", "https://genetherapy-ophthalmology.com/whats-on/speakers/"),
            "lnp-characterization-analytical-development.com": (HansonWadeSpider, "LNP Characterization & Analytical Development Summit", "Gene Therapy", "https://lnp-characterization-analytical-development.com/whats-on/speakers/"),
            "genetherapy-immunogenicity.com": (HansonWadeSpider, "Annual Gene Therapy Immunogenicity Summit", "Gene Therapy", "https://genetherapy-immunogenicity.com/whats-on/speakers/"),
            "car-tcr-summit.com": (HansonWadeSpider, "8th CAR-TCR Summit", "Gene Therapy", "https://car-tcr-summit.com/speakers/"),
            "inner-ear-disorders-therapeutics.com": (HansonWadeSpider, "3rd Inner Ear Disorders Therapeutics Summit", "Gene Therapy", "https://inner-ear-disorders-therapeutics.com/speakers/"),
            "lipid-nanoparticle-delivery-summit.com": (HansonWadeSpider, "Next Generation Lipid-Based Nanoparticles Delivery Summit", "Gene Therapy", "https://lipid-nanoparticle-delivery-summit.com/whats-on/speakers/"),
            "mrnabased-therapeutics.com": (HansonWadeSpider, "3rd Annual mRNA-Based Therapeutics Summit", "mRNA", "https://mrnabased-therapeutics.com/whats-on/speakers/"),
            "gamma-delta-t-therapies-summit.com": (HansonWadeSpider, "4th Gamma Delta T Therapies Summit", "Cell Therapy", "https://gamma-delta-t-therapies-summit.com/whats-on/speakers/"),
            "in-vivo-engineering.com": (HansonWadeSpider, "In Vivo Engineering of Therapeutic Cells Summit", "Cell Therapy", "https://in-vivo-engineering.com/whats-on/speakers/"),
            "process-development-celltx.com": (HansonWadeSpider, "Process Development for Cell Therapies Summit", "Cell Therapy", "https://process-development-celltx.com/whats-on/speakers/"),
            
            # Legacy
            "peptide-based-therapeutics-summit.com": (HansonWadeSpider, "Peptide Summit", "Peptides", "https://peptide-based-therapeutics-summit.com/speakers/"),
            "cdx-europe.com": (HansonWadeSpider, "CDX Europe", "Biomarkers & Diagnostics", "https://cdx-europe.com/speakers/"),
            "lnp-formulation-process-development-pharma.com": (HansonWadeSpider, "LNP Formulation", "Nanoparticles", "https://lnp-formulation-process-development-pharma.com/whats-on/speakers/"),
            "genetherapy-conference.com": (HansonWadeSpider, "Gene Therapy Conference", "Gene Therapy", "https://genetherapy-conference.com/speakers/"),
            "immuno-oncologyeurope.com": (ImmunoOncologySpider, "Immuno-Oncology Europe", "Immuno-Oncology", "https://www.immuno-oncologyeurope.com/speaker-biographies"),

            # Screenshot 2
            "genetherapy-patient-engagement.com": (HansonWadeSpider, "Gene Therapy Patient Engagement Summit", "Gene Therapy", "https://genetherapy-patient-engagement.com/whats-on/speakers/"),
            "mrna-quality-control.com": (HansonWadeSpider, "mRNA Quality Control & Comparability Summit", "mRNA", "https://mrna-quality-control.com/about/speakers/"),
            "genetherapy-neurological-europe.com": (HansonWadeSpider, "Gene Therapy for Neurological Disorders Summit Europe", "Gene Therapy", "https://genetherapy-neurological-europe.com/whats-on/speakers/"),
            "cell-therapy-potency-assay.com": (HansonWadeSpider, "Cell Therapy Potency Assay Summit", "Cell Therapy", "https://www.cell-therapy-potency-assay.com/speakers/"),
            "allogeneic-cell-therapies.com": (HansonWadeSpider, "Allogeneic Cell Therapies Summit", "Cell Therapy", "https://allogeneic-cell-therapies.com/program/speakers/"),
            "ipsc-manufacturing-summit.com": (HansonWadeSpider, "iPSC Manufacturing Summit", "Cell Therapy", "https://ipsc-manufacturing-summit.com/whats-on/speakers/"),
            "genetherapy-analytical-europe.com": (HansonWadeSpider, "Gene Therapy Analytical Development Europe Summit", "Gene Therapy", "https://genetherapy-analytical-europe.com/whats-on/speakers/"),
            "mrna-processmanufacturing-europe.com": (HansonWadeSpider, "mRNA Process Development & Manufacturing Summit Europe", "mRNA", "https://mrna-processmanufacturing-europe.com/whats-on/speakers/"),
            "genetherapy-comparability.com": (HansonWadeSpider, "Gene Therapy Comparability Summit", "Gene Therapy", "https://genetherapy-comparability.com/whats-on/speakers/"),
            "supply-cell-immunotherapy.com": (HansonWadeSpider, "4th Supply Chain and Logistics for Cell & GTX Summit", "Manufacturing/Process", "https://supply-cell-immunotherapy.com/whats-on/speakers/"),
            "cartcr-europe.com": (HansonWadeSpider, "CAR-TCR Summit Europe", "Cell Therapy", "https://cartcr-europe.com/whats-on/speakers/"),
            "mrna-analytical-development.com": (HansonWadeSpider, "3rd mRNA Analytical Development Summit", "mRNA", "https://mrna-analytical-development.com/program/speakers/"),
            "allogeneic-cell-therapies-europe.com": (HansonWadeSpider, "2nd Allogeneic Cell Therapies Summit Europe", "Cell Therapy", "https://allogeneic-cell-therapies-europe.com/whats-on/speakers/"),
            "mrnabased-therapeutics-europe.com": (HansonWadeSpider, "2nd Annual mRNA-Based Therapeutics Summit Europe", "mRNA", "https://mrnabased-therapeutics-europe.com/whats-on/speakers/"),
            "cell-therapy-analytics.com": (HansonWadeSpider, "Cell Therapy Analytical Development Summit", "Cell Therapy", "https://cell-therapy-analytics.com/whats-on/speakers/"),
            "synthetic-biology-therapeutics-summit.com": (HansonWadeSpider, "Synthetic Biology-Based Therapeutics Summit", "Cell Therapy", "https://synthetic-biology-therapeutics-summit.com/agenda/speakers/"),
            "dry-amd-therapeutics.com": (HansonWadeSpider, "Dry AMD Therapeutics Summit", "Gene Therapy", "https://dry-amd-therapeutics.com/program/speakers/"),
            "crispr-conference.com": (HansonWadeSpider, "CRISPR 2.0 Summit", "Gene Therapy", "https://crispr-conference.com/whats-on/speakers/"),
            "innate-killer-europe.com": (HansonWadeSpider, "Innate Killer Summit Europe", "Cell Therapy", "https://innate-killer-europe.com/whats-on/speakers/"),
            "macrophage-directed-therapies.com": (HansonWadeSpider, "Macrophage-directed Therapies Summit", "Cell Therapy", "https://macrophage-directed-therapies.com/program/speakers/"),
            "b-and-t-cell-for-autoimmune.com": (HansonWadeSpider, "B & T Cell-Mediated Autoimmune Disease Drug Development", "Cell Therapy", "https://b-and-t-cell-for-autoimmune.com/program/speakers/"),
            "optimizing-aav-safety.com": (HansonWadeSpider, "Annual Optimizing Safety Summit", "Gene Therapy", "https://optimizing-aav-safety.com/whats-on/speakers/"),
            "innerear-disorders-therapeutics.com": (HansonWadeSpider, "Inner Ear Disorders Therapeutics Summit", "Gene Therapy", "https://innerear-disorders-therapeutics.com/speakers/"),
            "multi-functional-cell-therapies.com": (HansonWadeSpider, "2nd Multi-Functional Cell Therapies Summit", "Cell Therapy", "https://multi-functional-cell-therapies.com/whats-on/speakers/")
        }

    def load_urls(self, url_list):
        self.urls = url_list
        print(f"Loaded {len(self.urls)} urls to scrape.")

    def run(self):
        print("Engine starting... gonna loop through urls now")
        all_scraped_data = []
        for url in self.urls:
            print(f"Preparing to scrape {url}...")
            spider_tuple = None
            for domain, spider_tup in self.spider_map.items():
                if domain in url:
                    spider_tuple = spider_tup
                    break
            
            if spider_tuple:
                spider_class, conf_name, topic, speaker_url = spider_tuple
                conf_id = "CONF-" + hashlib.md5(url.encode()).hexdigest()[:6].upper()
                scraper = spider_class(conference_id=conf_id, conference_name=conf_name, topic=topic, url=url, speaker_url=speaker_url)
                data = scraper.extract()
                all_scraped_data.extend(data)
            else:
                print(f"No specific spider found for {url}, skipping!")
        
        if all_scraped_data:
            self.exporter.save_data(all_scraped_data)
        print("Engine finished running!")
