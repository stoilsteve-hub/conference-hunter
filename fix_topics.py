import pandas as pd
import re

df = pd.read_excel('conference_data.xlsx')

def get_real_topic(url):
    if not isinstance(url, str): return None
    if 'bioprocessingsummit.com' in url:
        match = re.search(r'/([^/]+)$', url)
        if match:
            topic_slug = match.group(1).replace('-', ' ').title()
            return topic_slug
    return None

def update_chi_topics(row):
    if row['Topic'] == 'Annual Bioprocessing  Boston 2022':
        real_topic = get_real_topic(row['URL'])
        if real_topic:
            row['Topic'] = real_topic
    return row

df = df.apply(update_chi_topics, axis=1)
df.to_excel('conference_data.xlsx', index=False)
print("Updated CHI topics.")
