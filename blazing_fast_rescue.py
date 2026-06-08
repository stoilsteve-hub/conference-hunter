import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.ai_extractor import extract_speaker_info
import re

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

def get_links(url):
    try:
        res = requests.get(url, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/speaker' in href or '/person' in href or '/bio' in href:
                if href.startswith('http'):
                    links.append(href)
                elif href.startswith('/'):
                    if 'web.archive.org' in url and href.startswith('/web/'):
                        links.append('https://web.archive.org' + href)
                    elif 'web.archive.org' in url:
                        base = '/'.join(url.split('/')[:5])
                        links.append(base + href)
                    else:
                        domain = '/'.join(url.split('/')[:3])
                        links.append(domain + href)
        return list(set(links))
    except Exception as e:
        return []

def scrape_profile(url, conf_name):
    try:
        res = requests.get(url, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Kill blockers
        for s in soup.select('#wm-ipp-base, #onetrust-consent-sdk, nav, header, footer, .cookie-banner, .gdpr'):
            s.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        if len(text) > 50:
            ai_data = extract_speaker_info(text)
            if ai_data and ai_data.get('name'):
                return url, conf_name, ai_data
    except Exception as e:
        pass
    return None, None, None

def main():
    df = pd.read_excel('conference_data.xlsx')
    
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
    
    all_links = []
    
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(get_links, CONF_URLS[c]): c for c in target_confs}
        for f in as_completed(futs):
            conf_name = futs[f]
            links = f.result()
            print(f"Found {len(links)} profile links for {conf_name}")
            for l in links:
                all_links.append((l, conf_name))
                
    print(f"Total profiles to scrape: {len(all_links)}")
    
    count = 0
    with ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(scrape_profile, l, c): (l, c) for l, c in all_links}
        for f in as_completed(futs):
            count += 1
            if count % 50 == 0:
                print(f"Scraped {count}/{len(all_links)}")
                
            url, conf_name, ai_data = f.result()
            if not ai_data: continue
            
            extracted_name = clean_name(ai_data['name'])
            
            matched_idx = None
            for idx, row in df[df['Conference Name'] == conf_name].iterrows():
                db_name = clean_name(row['Speaker Full Name'])
                if db_name in extracted_name or extracted_name in db_name:
                    matched_idx = idx
                    break
                    
            if matched_idx is not None:
                # Update
                df.at[matched_idx, 'Speaker Profile'] = url
                if ai_data.get('name'): df.at[matched_idx, 'Speaker Full Name'] = ai_data['name']
                if ai_data.get('job_title'): df.at[matched_idx, 'Speaker Job Title'] = ai_data['job_title']
                if ai_data.get('company'): df.at[matched_idx, 'Speaker Company'] = ai_data['company']
                if ai_data.get('summary'): df.at[matched_idx, 'Speaker Summary'] = ai_data['summary']
                print(f"Matched & Updated: {ai_data['name']}!")
            else:
                # Append
                new_row = {
                    'Conference Name': conf_name,
                    'Speaker Full Name': ai_data['name'],
                    'Speaker Job Title': ai_data.get('job_title', ''),
                    'Speaker Company': ai_data.get('company', ''),
                    'Speaker Summary': ai_data.get('summary', ''),
                    'Speaker Profile': url
                }
                df.loc[len(df)] = new_row
                print(f"NEW Speaker Discovered: {ai_data['name']}!")

    df.to_excel('conference_data.xlsx', index=False)
    print("Blazing Fast Rescue Complete.")

if __name__ == "__main__":
    main()
