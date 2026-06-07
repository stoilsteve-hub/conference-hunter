import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from core.ai_extractor import extract_speaker_info
import re
import os

CONF_URLS = {
    "Annual Bioprocessing Summit Boston 2022": "https://www.bioprocessingsummit.com/speakers",
    "BPI 2022": "https://web.archive.org/web/20221001000000/https://informaconnect.com/bioprocessinternational/speakers/",
    "BPI Europe 2020": "https://web.archive.org/web/20200501000000/https://informaconnect.com/bpieurope/speakers/",
    "BPI Europe 2023 (Bioprocess International)": "https://informaconnect.com/bpieurope/speakers/",
    "BPI 2021": "https://web.archive.org/web/20211001000000/https://informaconnect.com/bioprocessinternational/speakers/",
    "BPI 2020": "https://web.archive.org/web/20201001000000/https://informaconnect.com/bioprocessinternational/speakers/",
    "Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance": "https://www.immunogenicitysummit.com/immunogenicity-assessment",
    "Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control": "https://www.immunogenicitysummit.com/immunogenicity-prediction",
    "Immunogenicity & Bioassay Summit - Optimizing Bioassays for Biologics": "https://www.immunogenicitysummit.com/optimizing-bioassays",
    "BPI Europe 2021": "https://web.archive.org/web/20210501000000/https://informaconnect.com/bpieurope/speakers/",
    "Cambridge Healthtech Institute's 11th Annual Cell-Based Immunotherapies": "https://www.pegsummit.com/cell-based",
    "Cambridge Healthtech Institute's 3rd Annual In vivo Cell and Gene Engineering": "https://www.pegsummit.com/in-vivo",
    "Bioprocessing summit 2021 - Cell Culture and Bioproduction": "https://www.bioprocessingsummit.com/cell-culture",
    "Bioprocessing summit 2021 - Analytical Characterisation and Formulation": "https://www.bioprocessingsummit.com/analytical-characterisation",
    "Bioprocessing summit 2020 - Cell Culture to Bioproduction": "https://www.bioprocessingsummit.com/cell-culture",
    "Bioprocessing summit 2020 - Cell Line Development to Protein Expression": "https://www.bioprocessingsummit.com/cell-line",
    "Bioprocessing summit 2020 - Analytical Characterisation": "https://www.bioprocessingsummit.com/analytical",
    "Bioprocessing summit 2020 - Formulation, Stability & Aggregation": "https://www.bioprocessingsummit.com/formulation",
    "Bioprocessing summit 2020 - Continuous Processing for Biopharmaceuticals": "https://www.bioprocessingsummit.com/continuous-processing",
    "Bioprocessing summit 2020 - Cell Therapy CMC and Manufacturing": "https://www.bioprocessingsummit.com/cell-therapy",
    "Bioprocessing summit 2020 - Gene Therapy CMC and Manufacturing": "https://www.bioprocessingsummit.com/gene-therapy",
    "Immunogenicity & Bioassay Summit - Immunology for Biotherapeutics": "https://www.immunogenicitysummit.com/immunology-biotherapeutics",
    "Bioprocessing summit 2020 - Advances in Recovery and Purification": "https://www.bioprocessingsummit.com/recovery-purification",
    "BioProcess International 2024": "https://informaconnect.com/bioprocessinternational/speakers/",
    "Cambridge Healthtech Institute's 8th Annual Next Generation Cell-Based Therapies": "https://www.pegsummit.com/next-generation",
    "PEGS Boston Conference & Expo": "https://www.pegsummit.com/speakers",
    "Immuno-Oncology Europe": "https://www.immuno-oncologyeurope.com/speaker-biographies"
}

def clean_name(name):
    return re.sub(r'(?i)\b(Ph\.?D\.?|M\.?D\.?|MSc|PharmD|MBA|M\.?S\.?)\b', '', str(name)).replace(',', '').strip().lower()

async def get_profile_urls(context, roster_url):
    page = await context.new_page()
    try:
        await page.goto(roster_url, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        links = await page.evaluate('''() => {
            let anchors = document.querySelectorAll('a');
            let urls = [];
            for (let a of anchors) {
                if (a.href && (a.href.includes('/speaker') || a.href.includes('/person') || a.href.includes('/bio'))) {
                    urls.push(a.href);
                }
            }
            return urls;
        }''')
        await page.close()
        return list(set([l for l in links if l.startswith('http')]))
    except Exception as e:
        print(f"Error fetching roster {roster_url}: {e}", flush=True)
        await page.close()
        return []

async def process_profile(context, url, conf_name, missing_speakers_in_conf, df, semaphore):
    async with semaphore:
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(1000)
            raw_text = await page.locator("body").inner_text()
            
            if len(raw_text.strip()) > 50:
                # RUN SYNCHRONOUS AI EXTRACTION IN A THREAD SO IT DOESNT DEADLOCK THE EVENT LOOP
                ai_data = await asyncio.to_thread(extract_speaker_info, raw_text)
                
                if not ai_data or not ai_data.get('name'):
                    await page.close()
                    return
                    
                extracted_name = clean_name(ai_data['name'])
                
                for idx, row in missing_speakers_in_conf.iterrows():
                    db_name = clean_name(row['Speaker Full Name'])
                    
                    if db_name in extracted_name or extracted_name in db_name:
                        print(f"[{conf_name}] Matched {db_name} to {ai_data['name']}! Rescuing data...", flush=True)
                        df.at[idx, 'Speaker Profile'] = url
                        if ai_data.get('name'): df.at[idx, 'Speaker Full Name'] = ai_data['name']
                        if ai_data.get('job_title'): df.at[idx, 'Speaker Job Title'] = ai_data['job_title']
                        if ai_data.get('company'): df.at[idx, 'Speaker Company'] = ai_data['company']
                        if ai_data.get('summary'): df.at[idx, 'Speaker Summary'] = ai_data['summary']
                        break
        except Exception as e:
            pass
        finally:
            await page.close()

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    missing_mask = df['Speaker Profile'].isna() | (df['Speaker Profile'].astype(str).str.strip() == '') | (df['Speaker Profile'].astype(str).str.lower() == 'nan')
    
    semaphore = asyncio.Semaphore(10) # BUMP TO 10 FOR MAX SPEED
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        for conf_name, roster_url in CONF_URLS.items():
            conf_missing = df[missing_mask & (df['Conference Name'] == conf_name)]
            if len(conf_missing) == 0:
                continue
                
            print(f"\nProcessing {conf_name}: {len(conf_missing)} missing profiles...", flush=True)
            profile_urls = await get_profile_urls(context, roster_url)
            print(f"Found {len(profile_urls)} profile links on the roster.", flush=True)
            
            tasks = []
            for url in profile_urls:
                tasks.append(process_profile(context, url, conf_name, conf_missing, df, semaphore))
                
            if tasks:
                await asyncio.gather(*tasks)
                
            # Save after every conference batch finishes
            df.to_excel('conference_data.xlsx', index=False)
            print(f"Saved DB chunk for {conf_name}", flush=True)
                
        await browser.close()
        
    print("Surgical Rescue Complete.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
