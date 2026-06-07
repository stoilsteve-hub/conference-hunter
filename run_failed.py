import hashlib
from core.engine import Engine
import main

e = Engine()

failed_domains = [
    "mrna-processmanufacturing.com", "cell-therapy-analytics-europe.com", "genetherapy-ophthalmology.com",
    "genetherapy-immunogenicity.com", "inner-ear-disorders-therapeutics.com", "gamma-delta-t-therapies-summit.com",
    "genetherapy-patient-engagement.com", "mrna-quality-control.com", "genetherapy-neurological-europe.com",
    "cell-therapy-potency-assay.com", "allogeneic-cell-therapies.com", "ipsc-manufacturing-summit.com",
    "mrna-processmanufacturing-europe.com", "genetherapy-comparability.com", "supply-cell-immunotherapy.com",
    "allogeneic-cell-therapies-europe.com", "synthetic-biology-therapeutics-summit.com", "dry-amd-therapeutics.com",
    "innate-killer-europe.com", "macrophage-directed-therapies.com", "b-and-t-cell-for-autoimmune.com",
    "optimizing-aav-safety.com", "innerear-disorders-therapeutics.com", "multi-functional-cell-therapies.com",
    "lab-asset-facility-europe.com", "wet-amd-drug-development.com", "innatekiller.com",
    "continuous-processing-pharma.com", "fermentation-enabled-proteins.com", "cns-proteindegradation.com",
    "kinase-drug-discovery-summit.com", "tumor-models-sf.com", "adc-targetselection.com",
    "applied-biocatalysis.com", "rna-drugdiscovery.com", "capital-project-engineering.com",
    "targeted-radiopharma.com", "claudin-targeted-therapies-summit.com", "cns-drug-delivery-summit.com",
    "personalized-cancer-vaccines.com", "cell-therapy-autoimmune-disease.com", "donor-selection-cell-source-summit.com",
    "genetherapy-cns.com", "tpd-europe.com", "spatialbiology-drugdevelopment.com",
    "targeted-radiopharma-manuf-supply.com", "adc-process-development.com", "crispr-analytical-development.com",
    "targeted-radiopharma-us2.com", "gamma-delta-t-therapies.com", "induced-proximity-summit.com",
    "genetherapy-potency-assay.com", "microbiome-summit.com", "hpapi-summit.com",
    "next-gen-genetherapy-vectors.com", "tumor-myeloid-therapeutics.com", "computational-rna-design-delivery.com",
    "cytokine-immunotherapies.com", "cell-engager-summit.com", "adc-payload-summit.com",
    "als-drug-development.com", "glp-1-based-therapeutics.com", "advanced-procurement-in-pharma.com",
    "next-gen-rna.com", "neoantigen-summit.com", "genetherapy-muscular.com",
    "translational-digital-pathology-ai.com", "genetherapy-analytical.com", "genetherapy-neurological.com",
    "til-therapies.com", "genetherapy-europe.com", "discoveryontarget.com"
]

urls_to_scrape = []
with open("main.py", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith('"https://') or line.startswith('"http://'):
            url = line.strip('",')
            if any(fd in url for fd in failed_domains):
                urls_to_scrape.append(url)

print(f"Loaded {len(urls_to_scrape)} URLs for Archive Agent fallback.")
e.load_urls(urls_to_scrape)
e.run(max_workers=1)
