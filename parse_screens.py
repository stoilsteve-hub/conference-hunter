import re
import urllib.parse

text = """
42 2nd Covalent Drug Discovery & Development Summit -> Protein Degradation -> https://covalent-drug-discovery.com/
43 7th RNA Targeted Drug Discovery & Development Summit -> RNA Therapy -> https://rna-drugdiscovery.com/
45 2nd Capital Project Engineering in Pharma Summit -> Process Development -> https://capital-project-engineering.com/
46 6th Targeted Radiopharmaceuticals Summit Europe -> ADCs & Engineered Antib -> https://targeted-radiopharma.com/
47 1st Annual Claudin-Targeted Therapies Summit -> ADCs & Engineered Antib -> https://claudin-targeted-therapies-summit.com/
49 6th CNS Drug Delivery Summit -> Central Nervous System -> https://cns-drug-delivery-summit.com/
50 5th Annual Genome Editing Therapeutics Summit -> Gene Therapy -> https://genome-editing-therapeutics-summit.com/
52 13th Tumour Models London Summit -> Precision Oncology -> https://tumour-models.com/
53 3rd Personalized Cancer Vaccine Summit -> RNA Therapy -> https://personalized-cancer-vaccines.com/
54 2nd Cell Therapy for Autoimmune Disease Summit -> Cell Therapy -> https://cell-therapy-autoimmune-disease.com/
55 Inaugural Donor Selection and Cell Source Summit -> Cell Therapy -> https://donor-selection-cell-source-summit.com/
57 GPCRs-Targeted Drug Discovery Summit Europe -> Protein Degradation -> https://gpcrs-europe.com/
58 6th Annual Gene Therapy for CNS Summit -> Gene Therapy -> https://genetherapy-cns.com/
59 3rd Liquid Biopsy Surveillance Summit -> Precision Oncology -> https://liquid-biopsy-surveillance-summit.com/
60 LEAP HR: Emerging Biopharma -> HR -> https://leaphr-emerging-biopharma.com/
61 5th Macrophage-directed Therapies Summit -> Cell Therapy -> https://macrophage-directed-therapies.com/
63 15th World ADC San Diego -> ADCs & Engineered Antib -> https://worldadc-usa.com/
64 4th TPD Summit Europe -> Protein Degradation -> https://tpd-europe.com/
65 6th TPD & Induced Proximity Summit -> Protein Degradation -> https://proteindegradation.com/
66 7th LEAP TA: Life Sciences Summit 2024 -> TA -> https://leapta-lifesciences.com/
67 2nd Fluid & Imaging Biomarkers & Endpoints in Neuroscience -> Central Nervous System -> https://fluid-imaging-biomarkers-neuro.com/
68 2nd Spatial Biology for Drug Development Summit -> Precision Oncology -> https://spatialbiology-drugdevelopment.com/
70 4th iPSC Drug Development & Manufacturing Summit -> Cell Therapy -> https://ipsc-therapies-summit.com/
72 2nd TRP Supply Chain & Manufacturing Summit -> ADCs & Engineered Antib -> https://targeted-radiopharma-manuf-supply.com/
73 7th Neuropsychiatric Drug Development Summit -> Central Nervous System -> https://neuropsychiatric-drug-development.com/
74 6th Annual RAS-Targeted Drug Development Summit -> Protein Degradation -> https://ras-drugdevelopment.com/
75 3rd Lipid Nanoparticles Development Europe -> RNA Therapy -> https://lipid-nanoparticle-development-europe.com/
76 9th CAR-TCR Summit -> Cell Therapy -> https://car-tcr-summit.com/
77 2nd ADC Process Development Summit -> ADCs & Engineered Antib -> https://adc-process-development.com/
78 2nd CRISPR-Based Therapy Analytical Development Summit -> Gene Therapy -> https://crispr-analytical-development.com/
79 3rd mRNA Process Development & Manufacturing Summit -> RNA Therapy -> https://mrna-processandmanufacturing.com/
80 6th Exosome-Based Therapeutics Development Summit -> RNA Therapy -> https://exosomebased-therapeutics.com/
81 14th World Clinical Biomarkers & Companion Diagnostics Summit -> Precision Oncology -> https://world-cdx.com/
82 15th World Bispecific Summit -> ADCs & Engineered Antib -> https://bispecific.com/
83 3rd Oligonucleotides CMC & Analytical Development Summit -> Precision Oncology -> https://oligos-cmc-analytical-development.com/
85 2nd ADC Linker & Conjugation Summit 2024 -> ADCs & Engineered Antib -> https://adc-linker-conjugation.com/
86 5th Gene Therapy Immunogenicity Summit -> Gene Therapy -> https://genetherapy-immunogenicity.com/
87 3rd Next Generation Lipid-Based Nanoparticles Delivery Summit -> RNA Therapy -> https://lipid-nanoparticle-delivery-summit.com/
88 LEAP HR: Life Sciences East -> HR -> https://leap-hr-lifesciences-east.com/
89 3rd Targeted Radiopharmaceuticals Summit US 2024 -> ADCs & Engineered Antib -> https://targeted-radiopharma-us2.com/
90 5th Gamma Delta T Therapies Summit -> Cell Therapy -> https://gamma-delta-t-therapies.com/
91 4th mRNA-Based Therapeutics Summit -> RNA Therapy -> https://mrnabased-therapeutics.com/
92 2nd ADC Toxicity Summit -> ADCs & Engineered Antib -> https://adc-toxicity.com/
93 4th Annual Induced Proximity-Based Drug Discovery Summit -> Protein Degradation -> https://induced-proximity-summit.com/
94 11th Annual Tumor Models Boston Summit -> Precision Oncology -> https://tumor-models.com/
95 2nd Gene Therapy Potency -> Gene Therapy -> https://genetherapy-potency-assay.com/
96 9th Microbiome Movement Drug Development Summit -> Microbiome -> https://microbiome-summit.com/
97 3rd In Vivo Cell Engineering & Gene Editing Summit -> Cell Therapy -> https://in-vivo-engineering.com/
99 4th Oligonucleotides for CNS Summit -> Central Nervous System -> https://oligonucleotides-cns.com/
100 Cell & Gene Therapy Pricing & Reimbursement Summit -> Cell Therapy -> https://cell-gene-pricing-reimbursement.com/
101 3rd World ADC Asia -> ADCs & Engineered Antib -> https://worldadc-asia.com/
102 13th HPAPI: Process Development for Highly Potent Drugs -> Process Development -> https://hpapi-summit.com/
103 5th RNA Editing Summit 2024 -> RNA Therapy -> https://rnaediting-summit.com/
104 4th Next Generation Gene Therapy Vectors Summit -> Gene Therapy -> https://next-gen-genetherapy-vectors.com/
105 3rd Process Development for Cell Therapies Summit -> Cell Therapy -> https://process-development-celltx.com/
106 4th Annual Tumor Myeloid Targeting Therapies Summit -> Cell Therapy -> https://tumor-myeloid-therapeutics.com/
107 6th Annual Allogeneic Cell Therapies Summit -> Cell Therapy -> https://allogeneic-cell-therapies.com/
108 2nd Annual Advancing Life Science Construction -> Project Type -> https://advancing-life-science-construction.com/
109 Computational RNA Design & Delivery Summit -> RNA Therapy -> https://computational-rna-design-delivery.com/
111 4th Gene Therapy Patient Engagement Summit -> Gene Therapy -> https://genetherapy-patient-engagement.com/
112 Lab Operations & Facility Management for Biopharma Summit -> Process Development -> https://lab-ops-for-biopharma.com/
113 LEAP HR: Healthcare -> HR -> https://leaphr-healthcare.com/
114 5th Gene Therapy Analytical Development Europe Summit -> Gene Therapy -> https://genetherapy-analytical-europe.com/
115 The 5th Cytokine-Based Drug Development Summit -> ADCs & Engineered Antib -> https://cytokine-immunotherapies.com/
116 6th Annual Treg Directed Therapies Summit -> Cell Therapy -> https://treg-directed-therapies.com/
117 6th Cell Engager Therapeutics Summit -> Cell Therapy -> https://cell-engager-summit.com/
118 Inaugural ADC Payload Summit -> ADCs & Engineered Antib -> https://adc-payload-summit.com/
119 6th Cell Engager Summit -> ADCs & Engineered Antib -> https://cell-engager-summit.com/
120 3rd Annual ALS Drug Development Summit -> Central Nervous System -> https://www.als-drug-development.com/
121 9th Annual 3D Tissue Models Summit 2024 -> Precision Oncology -> https://3d-tissuemodels.com/
124 GLP-1-Based Therapeutics Summit -> Autoimmune -> https://glp-1-based-therapeutics.com/
125 8th R&D Procurement & Sourcing in Pharma Summit -> Process Development -> https://advanced-procurement-in-pharma.com/
127 3rd Next Generation RNA Therapeutics Summit -> RNA Therapy -> https://www.next-gen-rna.com/
128 7th International Neoantigen Summit -> Precision Oncology -> https://neoantigen-summit.com/
130 5th TCR-based Therapies for Solid Tumors Summit -> Cell Therapy -> https://tcr-therapies-summit.com/
132 2nd mRNA Process Development... -> RNA Therapy -> https://mrna-processandmanufacturing-europe.com/
134 3rd ADC Analytical Development Summit -> ADCs & Engineered Antib -> https://adc-analytical.com/
135 4th Gene Therapy for Muscular Disorders Summit -> Gene therapy -> https://genetherapy-muscular.com/
136 5th Dermatology Drug Development Summit Europe -> Autoimmune -> https://dermatology-drugdevelopment-europe.com/
137 Translational Digital Pathology & AI Summit -> Precision Oncology -> https://translational-digital-pathology-ai.com/
139 7th Gene Therapy for Rare Disorders Summit -> Gene Therapy -> https://genetherapy-conference.com/
140 5th Supply Chain & Logistics for Cell Therapies Summit 2024 -> Cell Therapy -> https://cell-therapy-supply-chain-logistics.com/
141 3rd Cell Therapy Potency Assay Summit -> Cell Therapy -> https://www.cell-therapy-potency-assay.com/
142 2nd Precision Medicine in Inflammatory Bowel Disease Summit -> Autoimmune -> https://www.precision-medicine-in-ibd.com/
143 9th Innate Killer Summit -> Cell Therapy -> https://innate-killer.com/
144 Innate Killer 2023 -> Cell Therapy -> https://innate-killer.com/
146 3rd GPCR-Targeted Drug Discovery Summit -> Protein Degradation -> https://gpcrs-drugdiscovery.com/
148 7th CAR-TCR Summit Europe -> Cell Therapy -> https://cartcr-europe.com/
149 8th Microbiome Movement AgBioTech Summit -> Microbiome -> https://microbiome-agbiotech.com/
150 8th Antigen-Specific Immune Tolerance Summit -> Autoimmune -> https://as-immunetolerance.com/
151 2nd Viral Vector Process Development & Manufacturing Summit -> Process Development -> https://viral-vector-process-development.com/
152 4th Gene Therapy Comparability Summit -> Gene therapy -> https://genetherapy-comparability.com/
153 4th Wet AMD & Diabetic Eye Disease Drug Development -> Gene therapy -> https://wet-amd-drug-development.com/
155 2nd Next Generation Ophthalmic Drug Delivery Summit 2024 -> Gene therapy -> https://ophthalmic-drug-delivery.com/
158 The 2nd Annual PAT & Real Time Quality Summit 2023 -> Process Development -> https://process-analytical-technology.com/
159 5th Annual Cell Therapy Analytical Development Summit -> Cell Therapy -> https://cell-therapy-analytics.com/
160 5th Annual Gene Therapy Analytical Development Summit 2023 -> Gene therapy -> https://genetherapy-analytical.com/
161 4th Annual CRISPR 2.0 Congress 2023 -> Gene therapy -> https://crispr-conference.com/
165 5th Gene Therapy for Neurological Disorders Summit 2023 -> Gene therapy -> https://genetherapy-neurological.com/
168 2nd Innate Killer Europe Summit 2023 -> Cell Therapy -> https://innate-killer-europe.com/
171 4th Annual Gene Therapy for Ophthalmic Disorders Summit 2023 -> Gene therapy -> https://genetherapy-ophthalmology.com/
172 3rd Annual iPSC Derived Cell Therapies Summit -> Cell Therapy -> https://ipsc-therapies-summit.com/
173 5th TIL Therapies Summit -> Cell Therapy -> https://til-therapies.com/
187 4th Annual Gene Therapy Immunogenicity Summit 2023 -> Gene therapy -> https://genetherapy-immunogenicity.com/
189 CAR-TCR: Engineering a Disease-Free World -> Cell Therapy -> https://car-tcr-summit.com/
234 Gene Therapy for Neurological Disorders 2022 -> Gene Therapy -> https://genetherapy-neurological.com/
238 Gene Therapy Analytical Development 2022 -> Gene Therapy -> https://genetherapy-analytical.com/
239 Gene Therapy for Rare Disorders Europe Summit 2022 -> Gene Therapy -> https://genetherapy-europe.com/
"""

import sys
sys.path.append('.')
from core.engine import Engine
e = Engine()
existing_domains = list(e.spider_map.keys())

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
        
        if domain not in existing_domains:
            print(f'            "{domain}": (HansonWadeSpider, "{name}", "{topic}", ""),')
            existing_domains.append(domain)
