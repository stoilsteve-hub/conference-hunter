import re

text = """
3 5th TCR-based Therapies for Solid Tumors Summit -> Cell Therapy -> https://tcr-therapies-summit.com/ -> already processed?
4 Peptide Based Therapeutics Summit -> Precision Oncology -> https://peptide-based-therapeutics-summit.com/ -> already processed?
5 14th Clinical Biomarkers & CDx Europe -> Precision Oncology -> https://cdx-europe.com/ -> already processed?
6 4th LNP Formulation & Process Development Summit -> Process Development -> https://lnp-formulation-process-development-pharma.com/ -> already processed?
7 3rd Novel Nasal Formulation & Delivery Summit -> Process Development -> https://www.nasal-formulation-delivery.com/
8 4th Novel Conjugate Summit -> ADCs & Engineered Antib. -> https://novel-conjugates.com/
9 8th CAR-TCR Summit Europe -> Cell Therapy -> https://cartcr-europe.com/ -> already processed?
10 7th Treg Directed Therapies Summit -> Cell Therapy -> https://treg-directed-therapies.com/
11 8th Gene Therapy Development Summit -> Gene Therapy -> https://genetherapy-conference.com/ -> already processed?
12 3rd Lab Asset & Facility Management in Pharma Summit Europe -> Process Development -> https://lab-asset-facility-europe.com/
13 13th Alzheimer's & Parkinson's Drug Development Summit -> Central Nervous System -> https://alzheimers-parkinsons-summit.com/
14 Wet AMD & Diabetic Eye Disease Drug Summit -> Gene Therapy -> https://wet-amd-drug-development.com/
15 4th Cell Therapy Potency Assay Summit -> Cell Therapy -> https://www.cell-therapy-potency-assay.com/ -> already processed?
16 5th Supply Chain & Logistics for Cell & Gene Therapies Summit -> Cell Therapy -> https://supply-chain-logistics-cgt.com/ 
17 15th World ADC London -> ADCs & Engineered Antib. -> https://worldadc-europe.com/
18 10th Annual Innate Killer Summit -> Cell Therapy -> https://www.innatekiller.com/ 
19 7th Neuroimmunology Drug Development Summit -> Central Nervous System -> https://neuroimmunology-drugdevelopment.com/
20 9th Commercializing Continuous Processing Summit -> Process Development -> https://continuous-processing-pharma.com/
21 4th mRNA Analytical Development & Quality Control Summit -> RNA Therapy -> https://mrna-analytical-development.com/ 
22 5th Fermentation-Enabled Alternative Protein Summit -> Process Development -> https://fermentation-enabled-proteins.com/
23 3rd Viral Vector Process Development & Manufacturing Summit -> Process Development -> https://viral-vector-process-development.com/
24 LEAP HR: Life Sciences Europe -> HR -> https://leaphr-lifesciences-europe.com/
25 9th Liquid Biopsy for Precision Oncology Summit -> Precision Oncology -> https://lbx-summit.com/
26 6th Glioblastoma Drug Development Summit -> Precision Oncology -> https://glioblastoma-drugdevelopment.com/
27 2nd Protein Degradation for CNS Summit -> Protein Degradation -> https://cns-proteindegradation.com/
28 Inaugural Proteomics-Based Drug Discovery Summit -> Protein Degradation -> https://proteomic-drug-discovery.com/
29 3rd Kinase Targeted Drug Discovery Summit -> Precision Oncology -> https://kinase-drug-discovery-summit.com/
30 7th CRISPR AgBio Congress -> Gene Therapy -> https://crispr-agbio-congress.com/
31 3rd Ophthalmic Drug Delivery Summit -> Gene Therapy -> https://ophthalmic-drug-delivery.com/
32 9th Microbiome Movement Summit Europe -> Microbiome -> https://microbiome-europe.com/
33 8th Annual DDR Inhibitors Summit -> Precision Oncology -> https://ddr-inhibitors-summit.com/
34 3rd Spatial Biology for Immuno-Oncology Summit -> Precision Oncology -> https://www.spatial-biology-immuno-oncology.com/
35 9th Tumor Models San Francisco Summit -> Precision Oncology -> https://tumor-models-sf.com/
36 3rd Molecular Glue Drug Development Summit -> Protein Degradation -> https://molecular-glue-summit.com/
37 4th mRNA-Based Therapeutics Summit Europe -> RNA Therapy -> https://mrnabased-therapeutics-europe.com/ 
38 6th RNAi-Based Therapeutics Summit -> RNA Therapy -> https://rnaibased-therapeutics.com/
39 4th ADC Target Selection Summit -> ADCs & Engineered Antib. -> https://adc-targetselection.com/
40 4th Applied Biocatalysis & Enzyme Engineering Summit -> Process Development -> https://applied-biocatalysis.com/
41 3rd PAT & Real Time Quality Summit -> Process Development -> https://process-analytical-technology.com/
"""

existing_domains = [
    "tcr-therapies-summit.com", "mrna-processmanufacturing.com", "cell-therapy-analytics-europe.com",
    "genetherapy-ophthalmology.com", "lnp-characterization-analytical-development.com", "genetherapy-immunogenicity.com",
    "car-tcr-summit.com", "inner-ear-disorders-therapeutics.com", "lipid-nanoparticle-delivery-summit.com",
    "mrnabased-therapeutics.com", "gamma-delta-t-therapies-summit.com", "in-vivo-engineering.com",
    "process-development-celltx.com", "peptide-based-therapeutics-summit.com", "cdx-europe.com",
    "lnp-formulation-process-development-pharma.com", "genetherapy-conference.com", "immuno-oncologyeurope.com",
    "genetherapy-patient-engagement.com", "mrna-quality-control.com", "genetherapy-neurological-europe.com",
    "cell-therapy-potency-assay.com", "allogeneic-cell-therapies.com", "ipsc-manufacturing-summit.com",
    "genetherapy-analytical-europe.com", "mrna-processmanufacturing-europe.com", "genetherapy-comparability.com",
    "supply-cell-immunotherapy.com", "cartcr-europe.com", "mrna-analytical-development.com",
    "allogeneic-cell-therapies-europe.com", "mrnabased-therapeutics-europe.com", "cell-therapy-analytics.com",
    "synthetic-biology-therapeutics-summit.com", "dry-amd-therapeutics.com", "crispr-conference.com",
    "innate-killer-europe.com", "macrophage-directed-therapies.com", "b-and-t-cell-for-autoimmune.com",
    "optimizing-aav-safety.com", "innerear-disorders-therapeutics.com", "multi-functional-cell-therapies.com"
]

import urllib.parse
lines = text.strip().split("\n")
for line in lines:
    parts = line.split("->")
    if len(parts) >= 3:
        name_part = parts[0].strip()
        topic = parts[1].strip()
        url = parts[2].strip()
        
        name = re.sub(r'^\d+\s+', '', name_part)
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.replace("www.", "")
        
        if domain not in existing_domains and not "already processed" in line:
            print(f'            "{domain}": (HansonWadeSpider, "{name}", "{topic}", ""),')

