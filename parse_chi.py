import re
import urllib.parse

text = """
71 BioProcess International 2024 -> InformaConnect -> https://informaconnect.com/bioprocessinternational/speakers/
84 16th Annual Bioprocessing Summit -> CHI -> https://www.bioprocessingsummit.com/Streams/Cell-Therapy
122 Pegs Boston CAR-T, TCRs and TILs -> CHI -> https://www.pegsummit.com/
123 Cambridge Healthtech Institute's 3rd Annual In vivo Cell and Gene Engineering -> CHI -> https://www.pegsummit.com/In-vivo-engineering
126 Cambridge Healthtech Institute's 11th Annual Cell-Based Immunotherapies -> CHI -> https://www.pegsummit.com/cell-based-immunotherapies#2
131 Cambridge Healthtech Institute's 8th Annual Next Generation Cell-Based Therapies -> CHI -> https://www.immuno-oncologyeurope.com/ 
156 3rd Allogeneic Cell Therapies Summit Europe -> CHI -> https://allogeneic-cell-therapies-europe.com/ 
176 Discovery on Target 2023 -> CHI -> https://www.discoveryontarget.com/
213 PEGS Boston Conference & Expo -> CHI -> https://www.pegsummit.com/
215 BPI Europe 2023 (Bioprocess International) -> InformaConnect -> https://informaconnect.com/bpieurope/speakers/
243 Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control -> CHI -> https://www.immunogenicitysummit.com/22/immunogenicity-prediction
244 Immunogenicity & Bioassay Summit - Optimizing Bioassays for Biologics -> CHI -> https://www.immunogenicitysummit.com/22/bioassays-for-biologics
245 Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance -> CHI -> https://www.immunogenicitysummit.com/22/immunogenicity-assessment-Clinical-Relevance
246 Immunogenicity & Bioassay Summit - Immunology for Biotherapeutics -> CHI -> https://www.immunogenicitysummit.com/22/Immunology-for-Biotherapeutics
247 BPI 2022 -> InformaConnect -> http://web.archive.org/web/20220711180806/https://informaconnect.com/bioprocessinternational/speakers/
248 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/cell-culture
249 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/bioproduction
250 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/continuous-processing
251 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/purification-and-recovery
252 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/gene-therapy-cmc
253 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/gene-therapy-manufacturing
254 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/cell-therapy-cmc
255 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/host-cell-proteins
256 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/preclinical-analytical-development
257 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/stability-biologics
258 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/formulation-and-delivery-of-biologics
259 Annual Bioprocessing Summit Boston 2022 -> CHI -> https://www.bioprocessingsummit.com/22/vaccine-manufacturing
265 Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control -> CHI -> https://www.immunogenicitysummit.com/21/immunogenicity-prediction
266 Immunogenicity & Bioassay Summit - Optimizing Bioassays for Biologics -> CHI -> https://www.immunogenicitysummit.com/21/Bioassays-for-Biologics
267 Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance -> CHI -> https://www.immunogenicitysummit.com/21/Immunogenicity-Assessment-Clinical-Relevance
268 Immunogenicity & Bioassay Summit - Immunology for Biotherapeutics -> CHI -> https://www.immunogenicitysummit.com/21/Immunology-for-Biotherapeutics
269 BPI 2021 -> InformaConnect -> http://web.archive.org/web/20210619002826/https://informaconnect.com/bioprocessinternational/speakers/
270 BPI Europe 2021 -> InformaConnect -> http://web.archive.org/web/20220119235400/https://informaconnect.com/bpieurope/speakers/
271 Bioprocessing summit 2021 - Cell Culture and Bioproduction -> CHI -> https://www.bioprocessingeurope.com/21/cell-culture#Day2
272 Bioprocessing summit 2021 - Downstream Processing and Continuous Processing -> CHI -> https://www.bioprocessingeurope.com/21/continuous-processing
273 Bioprocessing summit 2021 - Analytical Characterisation and Formulation -> CHI -> https://www.bioprocessingeurope.com/21/analytical-characterisation
274 Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance -> CHI -> https://www.immunogenicitysummit.com/20/Immunogenicity-Assessment-Clinical-Relevance
275 Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control -> CHI -> https://www.immunogenicitysummit.com/20/immunogenicity-prediction
276 Immunogenicity & Bioassay Summit - Optimizing Bioassays for Biologics -> CHI -> https://www.immunogenicitysummit.com/20/Bioassays-for-Biologics
277 BPI 2020 -> InformaConnect -> http://web.archive.org/web/20200806181949/https://informaconnect.com/bioprocessinternational/speakers/
278 Bioprocessing summit 2020 - Cell Culture to Bioproduction -> CHI -> https://www.bioprocessingeurope.com/20/cell-culture
279 Bioprocessing summit 2020 - Cell Line Development to Protein Expression -> CHI -> https://www.bioprocessingeurope.com/20/cell-line-development
280 Bioprocessing summit 2020 - Continuous Processing for Biopharmaceuticals -> CHI -> https://www.bioprocessingeurope.com/20/continuous-processing
281 Bioprocessing summit 2020 - Advances in Recovery and Purification -> CHI -> https://www.bioprocessingeurope.com/20/purification
282 Bioprocessing summit 2020 - Cell Therapy CMC and Manufacturing -> CHI -> https://www.bioprocessingeurope.com/20/cell-therapy
283 Bioprocessing summit 2020 - Gene Therapy CMC and Manufacturing -> CHI -> https://www.bioprocessingeurope.com/20/gene-therapy
284 Bioprocessing summit 2020 - Analytical Characterisation -> CHI -> https://www.bioprocessingeurope.com/20/analytical-characterisation
285 Bioprocessing summit 2020 - Formulation, Stability & Aggregation -> CHI -> https://www.bioprocessingeurope.com/20/formulation
286 BPI Europe 2020 -> InformaConnect -> http://web.archive.org/web/20210302033734/https://informaconnect.com/bpieurope/speakers/
287 Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance -> CHI -> https://www.immunogenicitysummit.com/19/Immunogenicity-Assessment-Clinical-Relevance
288 Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control -> CHI -> https://www.immunogenicitysummit.com/19/immunogenicity-prediction
289 Immunogenicity & Bioassay Summit - Optimizing Bioassays for Biologics -> CHI -> https://www.immunogenicitysummit.com/19/Bioassays-for-Biologics
290 Immunogenicity & Bioassay Summit - Immunology for Biotherapeutics -> CHI -> https://www.immunogenicitysummit.com/19/Training-Immunology-for-Biotechnology
291 Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance -> CHI -> https://www.immunogenicitysummit.com/18/Immunogenicity-Assessment-Clinical-Relevance
292 Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control -> CHI -> https://www.immunogenicitysummit.com/18/immunogenicity-prediction
293 Immunogenicity & Bioassay Summit - Optimizing Bioassays for Biologics -> CHI -> https://www.immunogenicitysummit.com/18/Bioassays-for-Biologics
294 Immunogenicity & Bioassay Summit - Immunology for Biotherapeutics -> CHI -> https://www.immunogenicitysummit.com/18/Training-Immunology-for-Biotechnology
"""

import sys
sys.path.append('.')
from core.engine import Engine
e = Engine()
existing_urls = set(e.urls)
existing_domains = set(e.spider_map.keys())

lines = text.strip().split("\n")
for line in lines:
    parts = line.split("->")
    if len(parts) >= 3:
        name_part = parts[0].strip()
        provider = parts[1].strip()
        url = parts[2].strip()
        name = re.sub(r'^\d+\s+', '', name_part)
        
        spider_cls = "CHISpider" if provider == "CHI" else "InformaSpider"
        print(f'{url}|{spider_cls}|{name}|{"Both"}')
