import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.exporter import Exporter
from spiders.immuno_oncology import ImmunoOncologySpider
from spiders.hanson_wade_spider import HansonWadeSpider
from spiders.chi_spider import CHISpider
from spiders.informa_spider import InformaSpider

class Engine:
    def __init__(self):
        self.exporter = Exporter()
        self.urls = []
        self.spider_map = {
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
            "peptide-based-therapeutics-summit.com": (HansonWadeSpider, "Peptide Summit", "Peptides", "https://peptide-based-therapeutics-summit.com/speakers/"),
            "cdx-europe.com": (HansonWadeSpider, "CDX Europe", "Biomarkers & Diagnostics", "https://cdx-europe.com/speakers/"),
            "lnp-formulation-process-development-pharma.com": (HansonWadeSpider, "LNP Formulation", "Nanoparticles", "https://lnp-formulation-process-development-pharma.com/whats-on/speakers/"),
            "genetherapy-conference.com": (HansonWadeSpider, "Gene Therapy Conference", "Gene Therapy", "https://genetherapy-conference.com/speakers/"),
            "immuno-oncologyeurope.com": (ImmunoOncologySpider, "Immuno-Oncology Europe", "Immuno-Oncology", "https://www.immuno-oncologyeurope.com/speaker-biographies"),
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
            "multi-functional-cell-therapies.com": (HansonWadeSpider, "2nd Multi-Functional Cell Therapies Summit", "Cell Therapy", "https://multi-functional-cell-therapies.com/whats-on/speakers/"),
            "nasal-formulation-delivery.com": (HansonWadeSpider, "3rd Novel Nasal Formulation & Delivery Summit", "Process Development", ""),
            "novel-conjugates.com": (HansonWadeSpider, "4th Novel Conjugate Summit", "ADCs & Engineered Antib.", ""),
            "treg-directed-therapies.com": (HansonWadeSpider, "7th Treg Directed Therapies Summit", "Cell Therapy", ""),
            "lab-asset-facility-europe.com": (HansonWadeSpider, "3rd Lab Asset & Facility Management in Pharma Summit Europe", "Process Development", ""),
            "alzheimers-parkinsons-summit.com": (HansonWadeSpider, "13th Alzheimer's & Parkinson's Drug Development Summit", "Central Nervous System", ""),
            "wet-amd-drug-development.com": (HansonWadeSpider, "Wet AMD & Diabetic Eye Disease Drug Summit", "Gene Therapy", ""),
            "supply-chain-logistics-cgt.com": (HansonWadeSpider, "5th Supply Chain & Logistics for Cell & Gene Therapies Summit", "Cell Therapy", ""),
            "worldadc-europe.com": (HansonWadeSpider, "15th World ADC London", "ADCs & Engineered Antib.", ""),
            "innatekiller.com": (HansonWadeSpider, "10th Annual Innate Killer Summit", "Cell Therapy", ""),
            "neuroimmunology-drugdevelopment.com": (HansonWadeSpider, "7th Neuroimmunology Drug Development Summit", "Central Nervous System", ""),
            "continuous-processing-pharma.com": (HansonWadeSpider, "9th Commercializing Continuous Processing Summit", "Process Development", ""),
            "fermentation-enabled-proteins.com": (HansonWadeSpider, "5th Fermentation-Enabled Alternative Protein Summit", "Process Development", ""),
            "viral-vector-process-development.com": (HansonWadeSpider, "3rd Viral Vector Process Development & Manufacturing Summit", "Process Development", ""),
            "leaphr-lifesciences-europe.com": (HansonWadeSpider, "LEAP HR: Life Sciences Europe", "HR", ""),
            "lbx-summit.com": (HansonWadeSpider, "9th Liquid Biopsy for Precision Oncology Summit", "Precision Oncology", ""),
            "glioblastoma-drugdevelopment.com": (HansonWadeSpider, "6th Glioblastoma Drug Development Summit", "Precision Oncology", ""),
            "cns-proteindegradation.com": (HansonWadeSpider, "2nd Protein Degradation for CNS Summit", "Protein Degradation", ""),
            "proteomic-drug-discovery.com": (HansonWadeSpider, "Inaugural Proteomics-Based Drug Discovery Summit", "Protein Degradation", ""),
            "kinase-drug-discovery-summit.com": (HansonWadeSpider, "3rd Kinase Targeted Drug Discovery Summit", "Precision Oncology", ""),
            "crispr-agbio-congress.com": (HansonWadeSpider, "7th CRISPR AgBio Congress", "Gene Therapy", ""),
            "ophthalmic-drug-delivery.com": (HansonWadeSpider, "3rd Ophthalmic Drug Delivery Summit", "Gene Therapy", ""),
            "microbiome-europe.com": (HansonWadeSpider, "9th Microbiome Movement Summit Europe", "Microbiome", ""),
            "ddr-inhibitors-summit.com": (HansonWadeSpider, "8th Annual DDR Inhibitors Summit", "Precision Oncology", ""),
            "spatial-biology-immuno-oncology.com": (HansonWadeSpider, "3rd Spatial Biology for Immuno-Oncology Summit", "Precision Oncology", ""),
            "tumor-models-sf.com": (HansonWadeSpider, "9th Tumor Models San Francisco Summit", "Precision Oncology", ""),
            "molecular-glue-summit.com": (HansonWadeSpider, "3rd Molecular Glue Drug Development Summit", "Protein Degradation", ""),
            "rnaibased-therapeutics.com": (HansonWadeSpider, "6th RNAi-Based Therapeutics Summit", "RNA Therapy", ""),
            "adc-targetselection.com": (HansonWadeSpider, "4th ADC Target Selection Summit", "ADCs & Engineered Antib.", ""),
            "applied-biocatalysis.com": (HansonWadeSpider, "4th Applied Biocatalysis & Enzyme Engineering Summit", "Process Development", ""),
            "process-analytical-technology.com": (HansonWadeSpider, "3rd PAT & Real Time Quality Summit", "Process Development", ""),
            "covalent-drug-discovery.com": (HansonWadeSpider, "2nd Covalent Drug Discovery & Development Summit", "Protein Degradation", ""),
            "rna-drugdiscovery.com": (HansonWadeSpider, "7th RNA Targeted Drug Discovery & Development Summit", "RNA Therapy", ""),
            "capital-project-engineering.com": (HansonWadeSpider, "2nd Capital Project Engineering in Pharma Summit", "Process Development", ""),
            "targeted-radiopharma.com": (HansonWadeSpider, "6th Targeted Radiopharmaceuticals Summit Europe", "ADCs & Engineered Antib", ""),
            "claudin-targeted-therapies-summit.com": (HansonWadeSpider, "1st Annual Claudin-Targeted Therapies Summit", "ADCs & Engineered Antib", ""),
            "cns-drug-delivery-summit.com": (HansonWadeSpider, "6th CNS Drug Delivery Summit", "Central Nervous System", ""),
            "genome-editing-therapeutics-summit.com": (HansonWadeSpider, "5th Annual Genome Editing Therapeutics Summit", "Gene Therapy", ""),
            "tumour-models.com": (HansonWadeSpider, "13th Tumour Models London Summit", "Precision Oncology", ""),
            "personalized-cancer-vaccines.com": (HansonWadeSpider, "3rd Personalized Cancer Vaccine Summit", "RNA Therapy", ""),
            "cell-therapy-autoimmune-disease.com": (HansonWadeSpider, "2nd Cell Therapy for Autoimmune Disease Summit", "Cell Therapy", ""),
            "donor-selection-cell-source-summit.com": (HansonWadeSpider, "Inaugural Donor Selection and Cell Source Summit", "Cell Therapy", ""),
            "gpcrs-europe.com": (HansonWadeSpider, "GPCRs-Targeted Drug Discovery Summit Europe", "Protein Degradation", ""),
            "genetherapy-cns.com": (HansonWadeSpider, "6th Annual Gene Therapy for CNS Summit", "Gene Therapy", ""),
            "liquid-biopsy-surveillance-summit.com": (HansonWadeSpider, "3rd Liquid Biopsy Surveillance Summit", "Precision Oncology", ""),
            "leaphr-emerging-biopharma.com": (HansonWadeSpider, "LEAP HR: Emerging Biopharma", "HR", ""),
            "worldadc-usa.com": (HansonWadeSpider, "15th World ADC San Diego", "ADCs & Engineered Antib", ""),
            "tpd-europe.com": (HansonWadeSpider, "4th TPD Summit Europe", "Protein Degradation", ""),
            "proteindegradation.com": (HansonWadeSpider, "6th TPD & Induced Proximity Summit", "Protein Degradation", ""),
            "leapta-lifesciences.com": (HansonWadeSpider, "7th LEAP TA: Life Sciences Summit 2024", "TA", ""),
            "fluid-imaging-biomarkers-neuro.com": (HansonWadeSpider, "2nd Fluid & Imaging Biomarkers & Endpoints in Neuroscience", "Central Nervous System", ""),
            "spatialbiology-drugdevelopment.com": (HansonWadeSpider, "2nd Spatial Biology for Drug Development Summit", "Precision Oncology", ""),
            "ipsc-therapies-summit.com": (HansonWadeSpider, "4th iPSC Drug Development & Manufacturing Summit", "Cell Therapy", ""),
            "targeted-radiopharma-manuf-supply.com": (HansonWadeSpider, "2nd TRP Supply Chain & Manufacturing Summit", "ADCs & Engineered Antib", ""),
            "neuropsychiatric-drug-development.com": (HansonWadeSpider, "7th Neuropsychiatric Drug Development Summit", "Central Nervous System", ""),
            "ras-drugdevelopment.com": (HansonWadeSpider, "6th Annual RAS-Targeted Drug Development Summit", "Protein Degradation", ""),
            "lipid-nanoparticle-development-europe.com": (HansonWadeSpider, "3rd Lipid Nanoparticles Development Europe", "RNA Therapy", ""),
            "adc-process-development.com": (HansonWadeSpider, "2nd ADC Process Development Summit", "ADCs & Engineered Antib", ""),
            "crispr-analytical-development.com": (HansonWadeSpider, "2nd CRISPR-Based Therapy Analytical Development Summit", "Gene Therapy", ""),
            "mrna-processandmanufacturing.com": (HansonWadeSpider, "3rd mRNA Process Development & Manufacturing Summit", "RNA Therapy", ""),
            "exosomebased-therapeutics.com": (HansonWadeSpider, "6th Exosome-Based Therapeutics Development Summit", "RNA Therapy", ""),
            "world-cdx.com": (HansonWadeSpider, "14th World Clinical Biomarkers & Companion Diagnostics Summit", "Precision Oncology", ""),
            "bispecific.com": (HansonWadeSpider, "15th World Bispecific Summit", "ADCs & Engineered Antib", ""),
            "oligos-cmc-analytical-development.com": (HansonWadeSpider, "3rd Oligonucleotides CMC & Analytical Development Summit", "Precision Oncology", ""),
            "adc-linker-conjugation.com": (HansonWadeSpider, "2nd ADC Linker & Conjugation Summit 2024", "ADCs & Engineered Antib", ""),
            "leap-hr-lifesciences-east.com": (HansonWadeSpider, "LEAP HR: Life Sciences East", "HR", ""),
            "targeted-radiopharma-us2.com": (HansonWadeSpider, "3rd Targeted Radiopharmaceuticals Summit US 2024", "ADCs & Engineered Antib", ""),
            "gamma-delta-t-therapies.com": (HansonWadeSpider, "5th Gamma Delta T Therapies Summit", "Cell Therapy", ""),
            "adc-toxicity.com": (HansonWadeSpider, "2nd ADC Toxicity Summit", "ADCs & Engineered Antib", ""),
            "induced-proximity-summit.com": (HansonWadeSpider, "4th Annual Induced Proximity-Based Drug Discovery Summit", "Protein Degradation", ""),
            "tumor-models.com": (HansonWadeSpider, "11th Annual Tumor Models Boston Summit", "Precision Oncology", ""),
            "genetherapy-potency-assay.com": (HansonWadeSpider, "2nd Gene Therapy Potency", "Gene Therapy", ""),
            "microbiome-summit.com": (HansonWadeSpider, "9th Microbiome Movement Drug Development Summit", "Microbiome", ""),
            "oligonucleotides-cns.com": (HansonWadeSpider, "4th Oligonucleotides for CNS Summit", "Central Nervous System", ""),
            "cell-gene-pricing-reimbursement.com": (HansonWadeSpider, "Cell & Gene Therapy Pricing & Reimbursement Summit", "Cell Therapy", ""),
            "worldadc-asia.com": (HansonWadeSpider, "3rd World ADC Asia", "ADCs & Engineered Antib", ""),
            "hpapi-summit.com": (HansonWadeSpider, "13th HPAPI: Process Development for Highly Potent Drugs", "Process Development", ""),
            "rnaediting-summit.com": (HansonWadeSpider, "5th RNA Editing Summit 2024", "RNA Therapy", ""),
            "next-gen-genetherapy-vectors.com": (HansonWadeSpider, "4th Next Generation Gene Therapy Vectors Summit", "Gene Therapy", ""),
            "tumor-myeloid-therapeutics.com": (HansonWadeSpider, "4th Annual Tumor Myeloid Targeting Therapies Summit", "Cell Therapy", ""),
            "advancing-life-science-construction.com": (HansonWadeSpider, "2nd Annual Advancing Life Science Construction", "Project Type", ""),
            "computational-rna-design-delivery.com": (HansonWadeSpider, "Computational RNA Design & Delivery Summit", "RNA Therapy", ""),
            "lab-ops-for-biopharma.com": (HansonWadeSpider, "Lab Operations & Facility Management for Biopharma Summit", "Process Development", ""),
            "leaphr-healthcare.com": (HansonWadeSpider, "LEAP HR: Healthcare", "HR", ""),
            "cytokine-immunotherapies.com": (HansonWadeSpider, "The 5th Cytokine-Based Drug Development Summit", "ADCs & Engineered Antib", ""),
            "cell-engager-summit.com": (HansonWadeSpider, "6th Cell Engager Therapeutics Summit", "Cell Therapy", ""),
            "adc-payload-summit.com": (HansonWadeSpider, "Inaugural ADC Payload Summit", "ADCs & Engineered Antib", ""),
            "als-drug-development.com": (HansonWadeSpider, "3rd Annual ALS Drug Development Summit", "Central Nervous System", ""),
            "3d-tissuemodels.com": (HansonWadeSpider, "9th Annual 3D Tissue Models Summit 2024", "Precision Oncology", ""),
            "glp-1-based-therapeutics.com": (HansonWadeSpider, "GLP-1-Based Therapeutics Summit", "Autoimmune", ""),
            "advanced-procurement-in-pharma.com": (HansonWadeSpider, "8th R&D Procurement & Sourcing in Pharma Summit", "Process Development", ""),
            "next-gen-rna.com": (HansonWadeSpider, "3rd Next Generation RNA Therapeutics Summit", "RNA Therapy", ""),
            "neoantigen-summit.com": (HansonWadeSpider, "7th International Neoantigen Summit", "Precision Oncology", ""),
            "mrna-processandmanufacturing-europe.com": (HansonWadeSpider, "2nd mRNA Process Development...", "RNA Therapy", ""),
            "adc-analytical.com": (HansonWadeSpider, "3rd ADC Analytical Development Summit", "ADCs & Engineered Antib", ""),
            "genetherapy-muscular.com": (HansonWadeSpider, "4th Gene Therapy for Muscular Disorders Summit", "Gene therapy", ""),
            "dermatology-drugdevelopment-europe.com": (HansonWadeSpider, "5th Dermatology Drug Development Summit Europe", "Autoimmune", ""),
            "translational-digital-pathology-ai.com": (HansonWadeSpider, "Translational Digital Pathology & AI Summit", "Precision Oncology", ""),
            "cell-therapy-supply-chain-logistics.com": (HansonWadeSpider, "5th Supply Chain & Logistics for Cell Therapies Summit 2024", "Cell Therapy", ""),
            "precision-medicine-in-ibd.com": (HansonWadeSpider, "2nd Precision Medicine in Inflammatory Bowel Disease Summit", "Autoimmune", ""),
            "innate-killer.com": (HansonWadeSpider, "9th Innate Killer Summit", "Cell Therapy", ""),
            "gpcrs-drugdiscovery.com": (HansonWadeSpider, "3rd GPCR-Targeted Drug Discovery Summit", "Protein Degradation", ""),
            "microbiome-agbiotech.com": (HansonWadeSpider, "8th Microbiome Movement AgBioTech Summit", "Microbiome", ""),
            "as-immunetolerance.com": (HansonWadeSpider, "8th Antigen-Specific Immune Tolerance Summit", "Autoimmune", ""),
            "genetherapy-analytical.com": (HansonWadeSpider, "5th Annual Gene Therapy Analytical Development Summit 2023", "Gene therapy", ""),
            "genetherapy-neurological.com": (HansonWadeSpider, "5th Gene Therapy for Neurological Disorders Summit 2023", "Gene therapy", ""),
            "til-therapies.com": (HansonWadeSpider, "5th TIL Therapies Summit", "Cell Therapy", ""),
            "genetherapy-europe.com": (HansonWadeSpider, "Gene Therapy for Rare Disorders Europe Summit 2022", "Gene Therapy", ""),
            "informaconnect.com": (InformaSpider, "BioProcess International 2024", "Both", "https://informaconnect.com/bioprocessinternational/speakers/"),
            "bioprocessingsummit.com": (CHISpider, "16th Annual Bioprocessing Summit", "Both", "https://www.bioprocessingsummit.com/Streams/Cell-Therapy"),
            "pegsummit.com": (CHISpider, "Pegs Boston CAR-T, TCRs and TILs", "Both", "https://www.pegsummit.com/"),
            "discoveryontarget.com": (CHISpider, "Discovery on Target 2023", "Both", "https://www.discoveryontarget.com/"),
            "immunogenicitysummit.com": (CHISpider, "Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control", "Both", "https://www.immunogenicitysummit.com/22/immunogenicity-prediction"),
            "web.archive.org": (InformaSpider, "BPI 2022", "Both", "http://web.archive.org/web/20220711180806/https://informaconnect.com/bioprocessinternational/speakers/"),
            "bioprocessingeurope.com": (CHISpider, "Bioprocessing summit 2021 - Cell Culture and Bioproduction", "Both", "https://www.bioprocessingeurope.com/21/cell-culture#Day2"),
        }

    def load_urls(self, url_list):
        self.urls = url_list
        print(f"Loaded {len(self.urls)} urls to scrape.")

    def run(self):
        print("Engine starting... gonna loop through urls now")
        
        def scrape_url(url):
            spider_tuple = None
            for domain, spider_tup in self.spider_map.items():
                if domain in url:
                    spider_tuple = spider_tup
                    break
            
            if spider_tuple:
                spider_class, conf_name, topic, speaker_url = spider_tuple
                conf_id = "CONF-" + hashlib.md5(url.encode()).hexdigest()[:6].upper()
                scraper = spider_class(conference_id=conf_id, conference_name=conf_name, topic=topic, url=url, speaker_url=speaker_url)
                return scraper.extract()
            else:
                print(f"No specific spider found for {url}, skipping!")
                return []

        all_scraped_data = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(scrape_url, url): url for url in self.urls}
            for future in as_completed(future_to_url):
                try:
                    data = future.result()
                    if data:
                        all_scraped_data.extend(data)
                except Exception as exc:
                    print(f"URL generated an exception: {exc}")
        
        self.exporter.save_data(all_scraped_data)
