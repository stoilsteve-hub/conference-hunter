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
    "BPI 2021": "https://web.archive.org/web/20211001000000/https://informaconnect.com/bioprocessinternational/speakers/",
    "BPI 2020": "https://web.archive.org/web/20201001000000/https://informaconnect.com/bioprocessinternational/speakers/",
    "BPI Europe 2023 (Bioprocess International)": "https://informaconnect.com/bpieurope/speakers/",
    "Immunogenicity & Bioassay Summit - Immunogenicity Assessment & Clinical Relevance": "https://www.immunogenicitysummit.com/immunogenicity-assessment",
    "Immunogenicity & Bioassay Summit - Immunogenicity Prediction and Control": "https://www.immunogenicitysummit.com/immunogenicity-prediction",
    "Immuno-Oncology Europe": "https://www.immuno-oncologyeurope.com/speaker-biographies",
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
    "PEGS Boston Conference & Expo": "https://www.pegsummit.com/speakers",
    "Cambridge Healthtech Institute's 8th Annual Next Generation Cell-Based Therapies": "https://www.pegsummit.com/next-generation"
}

def clean_name(name):
    return re.sub(r'(?i)\b(Ph\.?D\.?|M\.?D\.?|MSc|PharmD|MBA|M\.?S\.?)\b', '', str(name)).replace(',', '').strip().lower()

async def kill_blockers(page):
    try:
        await page.evaluate('''() => {
            const killList = [
                '#wm-ipp-base', 
                '#onetrust-consent-sdk',
                'nav',
                'header',
                'footer',
                '.cookie-banner',
                '.gdpr'
            ];
            killList.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => el.remove());
            });
        }''')
    except Exception:
        pass

async def get_profile_urls(context, roster_url):
    for attempt in range(3):
        page = await context.new_page()
        try:
            await page.goto(roster_url, timeout=60000, wait_until="domcontentloaded")
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
            print(f"Error fetching roster {roster_url} (Attempt {attempt+1}): {e}", flush=True)
            await page.close()
            await asyncio.sleep(5)
    return []

async def process_profile(context, url, conf_name, df, semaphore):
    async with semaphore:
        for attempt in range(3):
            page = await context.new_page()
            try:
                # WAIT FOR DOM CONTENT
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                
                # FATAL FIX: Wayback Machine React takes 5-10 seconds to inject the text into the DOM!
                # We MUST wait 10,000ms after the DOM loads before extracting text.
                await page.wait_for_timeout(10000)
                
                await kill_blockers(page)
                
                raw_text = await page.locator("body").inner_text()
                
                if len(raw_text.strip()) > 50:
                    ai_data = await asyncio.to_thread(extract_speaker_info, raw_text)
                    
                    if not ai_data or not ai_data.get('name'):
                        await page.close()
                        return
                        
                    extracted_name = clean_name(ai_data['name'])
                    
                    # BLIND SWEEP: Check if they exist in the DB for this conference
                    matched_idx = None
                    for idx, row in df[df['Conference Name'] == conf_name].iterrows():
                        db_name = clean_name(row['Speaker Full Name'])
                        if db_name in extracted_name or extracted_name in db_name:
                            matched_idx = idx
                            break
                            
                    if matched_idx is not None:
                        # UPDATE EXISTING ROW
                        print(f"[{conf_name}] Blind Sweep Matched: {df.at[matched_idx, 'Speaker Full Name']} to {ai_data['name']}! Updating data...", flush=True)
                        df.at[matched_idx, 'Speaker Profile'] = url
                        if ai_data.get('name'): df.at[matched_idx, 'Speaker Full Name'] = ai_data['name']
                        if ai_data.get('job_title'): df.at[matched_idx, 'Speaker Job Title'] = ai_data['job_title']
                        if ai_data.get('company'): df.at[matched_idx, 'Speaker Company'] = ai_data['company']
                        if ai_data.get('summary'): df.at[matched_idx, 'Speaker Summary'] = ai_data['summary']
                    else:
                        # APPEND COMPLETELY NEW ROW
                        print(f"[{conf_name}] Blind Sweep Discovered NEW Speaker: {ai_data['name']}! Appending to database...", flush=True)
                        new_row = {
                            'Conference Name': conf_name,
                            'Speaker Full Name': ai_data['name'],
                            'Speaker Job Title': ai_data.get('job_title', ''),
                            'Speaker Company': ai_data.get('company', ''),
                            'Speaker Summary': ai_data.get('summary', ''),
                            'Speaker Profile': url
                        }
                        df.loc[len(df)] = new_row
                        
                await page.close()
                break # Success
            except Exception as e:
                print(f"[{conf_name}] Profile error {url}: {e}", flush=True)
                await page.close()
                await asyncio.sleep(3)

async def main():
    df = pd.read_excel('conference_data.xlsx')
    
    semaphore = asyncio.Semaphore(10)
    
    # Prioritize the Archive conferences that have the missing profiles
    target_confs = [
        "BPI Europe 2020",
        "BPI 2022",
        "BPI 2021",
        "BPI 2020",
        "BPI Europe 2021",
        "BPI Europe 2023 (Bioprocess International)",
        "Annual Bioprocessing Summit Boston 2022",
        "Immuno-Oncology Europe"
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        for conf_name in target_confs:
            roster_url = CONF_URLS[conf_name]
                
            print(f"\nEXECUTING BLIND SWEEP ON {conf_name}...", flush=True)
            
            profile_urls = await get_profile_urls(context, roster_url)
            print(f"Found {len(profile_urls)} profile links on the roster. Proceeding with absolute scraping...", flush=True)
            
            tasks = []
            for url in profile_urls:
                tasks.append(process_profile(context, url, conf_name, df, semaphore))
                
            if tasks:
                await asyncio.gather(*tasks)
                
            df.to_excel('conference_data.xlsx', index=False)
            print(f"Saved Blind Sweep DB chunk for {conf_name}", flush=True)
                
        await browser.close()
        
    print("WAYBACK ABSOLUTE RESCUE COMPLETE.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
