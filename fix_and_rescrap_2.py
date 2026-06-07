import pandas as pd
from core.engine import Engine


df = pd.read_excel('conference_data.xlsx')
original_len = len(df)
df = df[df['Topic'] != 'Annual Bioprocessing  Boston 2022']
df.to_excel('conference_data.xlsx', index=False)

e = Engine()
urls_to_scrape = []
for url, vals in e.spider_map.items():
    if 'bioprocessingsummit.com/22/' in url:
        urls_to_scrape.append(url)
    elif 'informaconnect.com/bioprocessinternational/speakers/' in url:
        urls_to_scrape.append(url)
    elif 'bioprocessingeurope.com' in url:
        urls_to_scrape.append(url)
    elif 'immunogenicitysummit' in url: 
        urls_to_scrape.append(url)

print(f"Rescraping {len(urls_to_scrape)} missing/broken URLs...")
e.load_urls(urls_to_scrape)
e.run()
