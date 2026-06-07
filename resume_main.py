import pandas as pd
from main import Launcher


try:
    df = pd.read_excel('conference_data.xlsx')
    completed_confs = set(df['Conference Name'].dropna().unique())
except Exception as e:
    completed_confs = set()

launcher = Launcher()

launcher.engine.load_urls([
    "https://tcr-therapies-summit.com/",
    "https://mrna-processmanufacturing.com/",
    "https://cell-therapy-analytics-europe.com/",
    "https://genetherapy-ophthalmology.com/",
    "https://lnp-characterization-analytical-development.com/",
    "https://genetherapy-immunogenicity.com/",
    "https://car-tcr-summit.com/",
    "https://inner-ear-disorders-therapeutics.com/",
    "https://lipid-nanoparticle-delivery-summit.com/",
    "https://mrnabased-therapeutics.com/",
    "https://gamma-delta-t-therapies-summit.com/",
    "https://in-vivo-engineering.com/",
    "https://process-development-celltx.com/",
    "https://peptide-based-therapeutics-summit.com/",
    "https://cdx-europe.com/",
    "https://lnp-formulation-process-development-pharma.com/",
    "https://genetherapy-conference.com/",
    "https://immuno-oncologyeurope.com/",
    "https://genetherapy-patient-engagement.com/",
    "https://mrna-quality-control.com/",
    "https://genetherapy-neurological-europe.com/",
    "https://cell-therapy-potency-assay.com/",
    "https://allogeneic-cell-therapies.com/",
    "https://ipsc-manufacturing-summit.com/",
    "https://genetherapy-analytical-europe.com/",
    "https://mrna-processmanufacturing-europe.com/",
    "https://genetherapy-comparability.com/",
    "https://supply-cell-immunotherapy.com/",
    "https://cartcr-europe.com/",
    "https://mrna-analytical-development.com/",
    "https://allogeneic-cell-therapies-europe.com/",
    "https://mrnabased-therapeutics-europe.com/",
    "https://cell-therapy-analytics.com/",
    "https://synthetic-biology-therapeutics-summit.com/",
    "https://dry-amd-therapeutics.com/",
    "https://crispr-conference.com/",
    "https://innate-killer-europe.com/",
    "https://macrophage-directed-therapies.com/",
    "https://b-and-t-cell-for-autoimmune.com/",
    "https://optimizing-aav-safety.com/",
    "https://innerear-disorders-therapeutics.com/",
    "https://multi-functional-cell-therapies.com/",
    "https://nasal-formulation-delivery.com/",
    "https://novel-conjugates.com/",
    "https://treg-directed-therapies.com/",
    "https://lab-asset-facility-europe.com/",
    "https://alzheimers-parkinsons-summit.com/",
    "https://wet-amd-drug-development.com/",
    "https://supply-chain-logistics-cgt.com/",
    "https://worldadc-europe.com/",
    "https://innatekiller.com/",
    "https://neuroimmunology-drugdevelopment.com/",
    "https://continuous-processing-pharma.com/",
    "https://fermentation-enabled-proteins.com/",
    "https://viral-vector-process-development.com/",
    "https://leaphr-lifesciences-europe.com/",
    "https://lbx-summit.com/",
    "https://glioblastoma-drugdevelopment.com/",
    "https://cns-proteindegradation.com/",
    "https://proteomic-drug-discovery.com/",
    "https://kinase-drug-discovery-summit.com/",
    "https://crispr-agbio-congress.com/",
    "https://ophthalmic-drug-delivery.com/",
    "https://microbiome-europe.com/",
    "https://ddr-inhibitors-summit.com/",
    "https://spatial-biology-immuno-oncology.com/",
    "https://tumor-models-sf.com/",
    "https://molecular-glue-summit.com/",
    "https://rnaibased-therapeutics.com/",
    "https://adc-targetselection.com/",
    "https://applied-biocatalysis.com/",
    "https://process-analytical-technology.com/",
    "https://covalent-drug-discovery.com/",
    "https://rna-drugdiscovery.com/",
    "https://capital-project-engineering.com/",
    "https://targeted-radiopharma.com/",
    "https://claudin-targeted-therapies-summit.com/",
    "https://cns-drug-delivery-summit.com/",
    "https://genome-editing-therapeutics-summit.com/",
    "https://tumour-models.com/",
    "https://personalized-cancer-vaccines.com/",
    "https://cell-therapy-autoimmune-disease.com/",
    "https://donor-selection-cell-source-summit.com/",
    "https://gpcrs-europe.com/",
    "https://genetherapy-cns.com/",
    "https://liquid-biopsy-surveillance-summit.com/",
    "https://tpd-europe.com/",
    "https://spatialbiology-drugdevelopment.com/",
    "https://targeted-radiopharma-manuf-supply.com/",
    "https://adc-process-development.com/",
    "https://crispr-analytical-development.com/",
    "https://targeted-radiopharma-us2.com/",
    "https://gamma-delta-t-therapies.com/",
    "https://induced-proximity-summit.com/",
    "https://genetherapy-potency-assay.com/",
    "https://microbiome-summit.com/",
    "https://hpapi-summit.com/",
    "https://next-gen-genetherapy-vectors.com/",
    "https://tumor-myeloid-therapeutics.com/",
    "https://computational-rna-design-delivery.com/",
    "https://cytokine-immunotherapies.com/",
    "https://cell-engager-summit.com/",
    "https://adc-payload-summit.com/",
    "https://als-drug-development.com/",
    "https://glp-1-based-therapeutics.com/",
    "https://advanced-procurement-in-pharma.com/",
    "https://next-gen-rna.com/",
    "https://neoantigen-summit.com/",
    "https://genetherapy-muscular.com/",
    "https://translational-digital-pathology-ai.com/",
    "https://genetherapy-analytical.com/",
    "https://genetherapy-neurological.com/",
    "https://til-therapies.com/",
    "https://genetherapy-europe.com/",
    "https://discoveryontarget.com/",
    "https://advancing-life-science-construction.com/",
    "https://lab-ops-for-biopharma.com/",
    "https://leaphr-healthcare.com/",
    "https://www.bioprocessingeurope.com/21/cell-culture#Day2",
    "https://www.bioprocessingeurope.com/21/continuous-processing",
    "https://www.bioprocessingeurope.com/21/analytical-characterisation",
    "https://www.immunogenicitysummit.com/20/Immunogenicity-Assessment-Clinical-Relevance",
    "https://www.immunogenicitysummit.com/20/immunogenicity-prediction",
    "https://www.immunogenicitysummit.com/20/Bioassays-for-Biologics",
    "http://web.archive.org/web/20200806181949/https://informaconnect.com/bioprocessinternational/speakers/",
    "https://www.bioprocessingeurope.com/20/cell-culture",
    "https://www.bioprocessingeurope.com/20/cell-line-development",
    "https://www.bioprocessingeurope.com/20/continuous-processing",
    "https://www.bioprocessingeurope.com/20/purification",
    "https://www.bioprocessingeurope.com/20/cell-therapy",
    "https://www.bioprocessingeurope.com/20/gene-therapy",
    "https://www.bioprocessingeurope.com/20/analytical-characterisation",
    "https://www.bioprocessingeurope.com/20/formulation",
    "http://web.archive.org/web/20210302033734/https://informaconnect.com/bpieurope/speakers/",
    "https://www.immunogenicitysummit.com/19/Immunogenicity-Assessment-Clinical-Relevance",
    "https://www.immunogenicitysummit.com/19/immunogenicity-prediction",
    "https://www.immunogenicitysummit.com/19/Bioassays-for-Biologics",
    "https://www.immunogenicitysummit.com/19/Training-Immunology-for-Biotechnology",
    "https://www.immunogenicitysummit.com/18/Immunogenicity-Assessment-Clinical-Relevance",
    "https://www.immunogenicitysummit.com/18/immunogenicity-prediction",
    "https://www.immunogenicitysummit.com/18/Bioassays-for-Biologics",
    "https://www.immunogenicitysummit.com/18/Training-Immunology-for-Biotechnology"
])


remaining_urls = []
for url in launcher.engine.urls:
    
    spider_tuple = launcher.engine.spider_map.get(url)
    if not spider_tuple:
        for key, spider_tup in launcher.engine.spider_map.items():
            if key in url:
                spider_tuple = spider_tup
                break
    
    if spider_tuple:
        conf_name = spider_tuple[1]
        if conf_name not in completed_confs:
            remaining_urls.append(url)

print(f"Skipping {len(launcher.engine.urls) - len(remaining_urls)} completed URLs. Resuming {len(remaining_urls)} remaining URLs...")
launcher.engine.urls = remaining_urls
launcher.engine.run()
